QUESTIONS = [
    {
        "id": 1,
        "text": "Тебе нравится работать с людьми?",
        "category": "interests",
        "type": "yesno"  # Добавляем тип вопроса
    },
    {
        "id": 2,
        "text": "Тебе интересно разбираться в технике и технологиях?",
        "category": "interests",
        "type": "yesno"
    },
    {
        "id": 3,
        "text": "Где ты предпочитаешь работать?",
        "category": "work_style",
        "type": "choice",
        "options": ["🏢 В офисе", "🏠 Удаленно", "🔄 Смешанный формат"]
    },
    {
        "id": 4,
        "text": "Тебе нравится творческая работа (рисование, музыка, дизайн)?",
        "category": "interests",
        "type": "yesno"
    },
    {
        "id": 5,
        "text": "Ты готов учиться новому каждый день?",
        "category": "skills",
        "type": "yesno"
    },
    {
        "id": 6,
        "text": "Тебе важна стабильность в работе?",
        "category": "preferences",
        "type": "yesno"
    },
    {
        "id": 7,
        "text": "Ты любишь решать сложные задачи?",
        "category": "skills",
        "type": "yesno"
    },
    {
        "id": 8,
        "text": "Тебе нравится работать в команде?",
        "category": "work_style",
        "type": "yesno"
    },
    {
        "id": 9,
        "text": "Ты хочешь иметь свободный график работы?",
        "category": "preferences",
        "type": "yesno"
    },
    {
        "id": 10,
        "text": "Ты готов открыть свой бизнес в будущем?",
        "category": "preferences",
        "type": "yesno"
    }
]



PROFESSIONS_DB = {
    "Программист": {
        "tags": ["техника", "логика", "обучение", "решение задач"],
        "description": "💻 Создаешь сайты, приложения и программы. Работаешь за компьютером, решаешь интересные задачи.",
        "salary": "от 100 000 ₽",
        "demand": "🔥 Очень востребовано",
        "education": "Высшее или курсы"
    },

    "Дизайнер": {
        "tags": ["творчество", "визуал", "креатив", "рисование"],
        "description": "🎨 Создаешь красивые интерфейсы, логотипы, рисуешь иллюстрации. Воплощаешь идеи в визуал.",
        "salary": "от 80 000 ₽",
        "demand": "🔥 Высокий спрос",
        "education": "Курсы или самообучение"
    },

    "Менеджер проектов": {
        "tags": ["люди", "команда", "организация", "общение"],
        "description": "📋 Управляешь командами, следишь за сроками, общаешься с клиентами. Организуешь работу других.",
        "salary": "от 120 000 ₽",
        "demand": "🔥 Очень востребовано",
        "education": "Высшее + курсы"
    },

    "Маркетолог": {
        "tags": ["люди", "творчество", "аналитика", "общение"],
        "description": "📊 Продвигаешь продукты, анализируешь рынок, создаешь рекламные кампании.",
        "salary": "от 90 000 ₽",
        "demand": "🔥 Высокий спрос",
        "education": "Высшее или курсы"
    },

    "Аналитик данных": {
        "tags": ["логика", "аналитика", "техника", "решение задач"],
        "description": "📈 Собираешь и анализируешь данные, делаешь выводы, помогаешь бизнесу принимать решения.",
        "salary": "от 130 000 ₽",
        "demand": "🔥 Очень востребовано",
        "education": "Высшее (математика/статистика)"
    },

    "Преподаватель": {
        "tags": ["люди", "обучение", "общение", "стабильность"],
        "description": "👨‍🏫 Обучаешь других, передаешь знания, помогаешь людям расти.",
        "salary": "от 50 000 ₽",
        "demand": "📊 Стабильный спрос",
        "education": "Высшее педагогическое"
    },

    "Предприниматель": {
        "tags": ["лидерство", "решение задач", "самостоятельность", "риск"],
        "description": "🚀 Создаешь свой бизнес, управляешь процессами, берешь ответственность.",
        "salary": "от 0 до бесконечности",
        "demand": "📈 Зависит от идеи",
        "education": "Опыт и знания"
    }
}

def get_recommendations(answers):
    scores = {prof: 0 for prof in PROFESSIONS_DB}

    for q_id, answer in answers.items():
        question = QUESTIONS[q_id - 1]
        category = question["category"]
        
        if answer == "yes":
            for prof, data in PROFESSIONS_DB.items():
                if category == "interests" and any(tag in data["tags"] for tag in ["творчество", "техника", "логика"]):
                    scores[prof] += 1
                elif category == "work_style" and any(tag in data["tags"] for tag in ["команда", "самостоятельность"]):
                    scores[prof] += 1
                elif category == "skills" and any(tag in data["tags"] for tag in ["обучение", "решение задач", "аналитика"]):
                    scores[prof] += 1
                elif category == "preferences" and any(tag in data["tags"] for tag in ["стабильность", "свобода", "риск"]):
                    scores[prof] += 1
        elif answer == "no":
            pass
    
    sorted_profs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_profs[:3]
    
    return [prof[0] for prof in top_3]