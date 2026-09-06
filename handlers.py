# handlers.py
from telebot import types
from config import *
from keyboards import *
from test_data import QUESTIONS, get_recommendations, PROFESSIONS_DB
from database import Database

class BotHandlers:
    
    def __init__(self, bot):
        self.bot = bot
        self.user_answers = {}
        self.user_state = {}
    
    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            self.handle_start(message)
        
        @self.bot.message_handler(func=lambda message: message.text == BUTTONS["start_test"])
        def start_test_button(message):
            self.start_test(message)
        
        @self.bot.message_handler(func=lambda message: message.text == BUTTONS["restart_test"])
        def restart_test_button(message):
            self.start_test(message)
        
        @self.bot.message_handler(func=lambda message: message.text == BUTTONS["help"])
        def help_button(message):
            self.show_help(message)
        
        @self.bot.message_handler(func=lambda message: message.text == BUTTONS["about"])
        def about_button(message):
            self.show_about(message)
        
        @self.bot.message_handler(func=lambda message: message.text == BUTTONS["back"])
        def back_button(message):
            self.go_back(message)
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_text(message):
            self.handle_text_message(message)
        
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback(call):
            self.handle_inline_callback(call)
    
    def handle_start(self, message):
        user_id = message.from_user.id

        Database.save_user(
            user_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )
        self.bot.send_message(
            chat_id=user_id,
            text=WELCOME_TEXT,
            reply_markup=main_menu()
        )
    
    def start_test(self, message):
        user_id = message.from_user.id
        Database.clear_test_progress(user_id)
        self.user_answers[user_id] = {}
        self.send_question(user_id, 0)
    
    def send_question(self, user_id, question_index):
        if question_index >= len(QUESTIONS):
            self.show_results(user_id)
            return
        
        question = QUESTIONS[question_index]
        question_text = f"Вопрос {question_index + 1} из {len(QUESTIONS)}:\n\n{question['text']}"
        

        if question.get('type') == 'choice':
            keyboard = choice_keyboard(question.get('options', []))
        else:
            keyboard = test_keyboard()
        
        self.bot.send_message(
            chat_id=user_id,
            text=question_text,
            reply_markup=keyboard
        )

        self.user_state[user_id] = {
            'current_question': question_index,
            'question_type': question.get('type', 'yesno')
        }

        Database.save_test_progress(
            user_id=user_id,
            question_id=question_index,
            answers=self.user_answers.get(user_id, {})
        )
    
    def handle_text_message(self, message):
        user_id = message.from_user.id
        text = message.text

        if user_id in self.user_state:
            state = self.user_state[user_id]
            current_q = state['current_question']
            question_type = state.get('question_type', 'yesno')
            
            if text == BUTTONS["back"]:
                self.go_back(message)
                return
            
            if question_type == 'choice':
                question = QUESTIONS[current_q]
                if text in question.get('options', []):
                    if user_id not in self.user_answers:
                        self.user_answers[user_id] = {}
                    self.user_answers[user_id][current_q + 1] = text

                    self.send_question(user_id, current_q + 1)
                else:
                    self.bot.send_message(
                        chat_id=user_id,
                        text="Пожалуйста, выбери один из вариантов! 👆",
                        reply_markup=choice_keyboard(question.get('options', []))
                    )
            else:
                if text in ["✅Да", "❌Нет", "🤔Не знаю"]:
                    answer_map = {
                        "✅Да": "yes",
                        "❌Нет": "no",
                        "🤔Не знаю": "maybe"
                    }
                    
                    if user_id not in self.user_answers:
                        self.user_answers[user_id] = {}
                    
                    self.user_answers[user_id][current_q + 1] = answer_map[text]
                    self.send_question(user_id, current_q + 1)
                else:
                    self.bot.send_message(
                        chat_id=user_id,
                        text="Пожалуйста, используй кнопки для ответа! 👆",
                        reply_markup=test_keyboard()
                    )
        else:
            if text in PROFESSIONS_DB:
                self.show_profession_info(user_id, text)
            else:
                self.bot.send_message(
                    chat_id=user_id,
                    text="Используй кнопки меню для навигации! 👇",
                    reply_markup=main_menu()
                )
    
    def show_profession_info(self, user_id, prof_name):
        prof_data = PROFESSIONS_DB.get(prof_name, {})
        
        info_text = f"""
📌 **{prof_name}**

{prof_data.get('description', '')}

💰 **Зарплата:** {prof_data.get('salary', '')}
📊 **Востребованность:** {prof_data.get('demand', '')}
🎓 **Образование:** {prof_data.get('education', '')}

Хочешь узнать о другой профессии? Напиши её название!
        """
        
        self.bot.send_message(
            chat_id=user_id,
            text=info_text,
            parse_mode='Markdown',
            reply_markup=main_menu()
        )
    
    def show_results(self, user_id):
        answers = self.user_answers.get(user_id, {})
        
        if not answers:
            self.bot.send_message(
                chat_id=user_id,
                text="Что-то пошло не так. Давай попробуем сначала!",
                reply_markup=main_menu()
            )
            return

        recommendations = get_recommendations(answers)

        Database.save_test_result(user_id, answers, recommendations)

        Database.clear_test_progress(user_id)
        self.user_state.pop(user_id, None)
        self.user_answers.pop(user_id, None)

        result_text = "🎉 Твои топ-3 профессии:\n\n"
        
        for i, prof in enumerate(recommendations, 1):
            prof_data = PROFESSIONS_DB.get(prof, {})
            result_text += f"{i}. {prof}\n"
            result_text += f"   {prof_data.get('description', '')}\n"
            result_text += f"   💰 Зарплата: {prof_data.get('salary', '')}\n"
            result_text += f"   📊 Востребованность: {prof_data.get('demand', '')}\n"
            result_text += f"   🎓 Образование: {prof_data.get('education', '')}\n\n"
        
        result_text += "\nПодробнее о профессии можешь спросить, написав её название!"

        self.bot.send_message(
            chat_id=user_id,
            text=result_text,
            reply_markup=result_keyboard()
        )
    
    def show_help(self, message):
        help_text = """
❓ **Помощь по боту**

Я - карьерный советчик! Вот что я умею:

1️⃣ **Начать тест** - пройди опрос из 10 вопросов
2️⃣ **Получить рекомендации** - я подберу 3 профессии для тебя
3️⃣ **Узнать о профессии** - напиши название, я расскажу подробнее

Команды:
/start - начать заново

Если у тебя есть вопросы - просто напиши мне! 😊
        """
        
        self.bot.send_message(
            chat_id=message.from_user.id,
            text=help_text,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
    
    def show_about(self, message):
        about_text = """
ℹ️ **О боте**

Я - твой персональный помощник в выборе профессии!

🤖 Создан, чтобы помочь подросткам и взрослым найти свое призвание.

🧠 Использую психологические методики и анализ навыков.

🚀 Постоянно развиваюсь и учусь новому!

Версия: 1.0.0
        """
        
        self.bot.send_message(
            chat_id=message.from_user.id,
            text=about_text,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
    
    def go_back(self, message):
        user_id = message.from_user.id

        Database.clear_test_progress(user_id)
        self.user_state.pop(user_id, None)
        self.user_answers.pop(user_id, None)
        
        self.bot.send_message(
            chat_id=user_id,
            text="Возвращаемся в главное меню 🔙",
            reply_markup=main_menu()
        )
    
    def handle_inline_callback(self, call):

        user_id = call.from_user.id
        
        if call.data.startswith('prof_'):
            prof_name = call.data.replace('prof_', '')
            prof_data = PROFESSIONS_DB.get(prof_name, {})
            
            info_text = f"""
📌 **{prof_name}**

{prof_data.get('description', '')}

💰 **Зарплата:** {prof_data.get('salary', '')}
📊 **Востребованность:** {prof_data.get('demand', '')}
🎓 **Образование:** {prof_data.get('education', '')}

Хочешь узнать о другой профессии? Напиши её название!
            """
            
            self.bot.send_message(
                chat_id=user_id,
                text=info_text,
                parse_mode='Markdown'
            )

        self.bot.answer_callback_query(call.id)