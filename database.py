import sqlite3
import json
from datetime import datetime

class Database:
    
    @staticmethod
    def get_connection():
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def create_tables():
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                age INTEGER,
                current_job TEXT,
                registration_date TIMESTAMP,
                last_active TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                test_date TIMESTAMP,
                interests TEXT,
                skills TEXT,
                work_style TEXT,
                recommendations TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_progress (
                user_id INTEGER PRIMARY KEY,
                current_question INTEGER,
                answers TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def save_user(user_id, username, first_name, age=None, current_job=None):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            (user_id, username, first_name, age, current_job, registration_date, last_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            username,
            first_name,
            age,
            current_job,
            datetime.now(),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def save_test_result(user_id, answers, recommendations):
        conn = Database.get_connection()
        cursor = conn.cursor()

        answers_json = json.dumps(answers)
        recommendations_json = json.dumps(recommendations)
        
        cursor.execute('''
            INSERT INTO test_results (user_id, test_date, interests, skills, work_style, recommendations)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            datetime.now(),
            "",
            "",
            "", 
            recommendations_json
        ))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def save_test_progress(user_id, question_id, answers):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        answers_json = json.dumps(answers)
        
        cursor.execute('''
            INSERT OR REPLACE INTO test_progress (user_id, current_question, answers)
            VALUES (?, ?, ?)
        ''', (user_id, question_id, answers_json))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_test_progress(user_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT current_question, answers FROM test_progress WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'current_question': result['current_question'],
                'answers': json.loads(result['answers'])
            }
        return None
    
    @staticmethod
    def clear_test_progress(user_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM test_progress WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
