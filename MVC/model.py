import random
import json  # เพิ่มการนำเข้าโมดูล json

class QuestionModel:
    def __init__(self):
        with open('questions.json', 'r', encoding='utf-8') as f:
            self.questions = json.load(f)

        self.previous_category = None
        self.previous_emotion = None
        self.emotion_log = []

    def get_random_question_by_category(self, category):
        # กรองคำถามตามหมวดหมู่
        questions_by_category = [q for q in self.questions if q['category'] == category]
        
        if not questions_by_category:
            raise ValueError(f"No questions found for category: {category}")
        
        return random.choice(questions_by_category)

    def calculate_emotion(self, category):
        # คำนวณอารมณ์ตามหมวดหมู่
        emotion = 50  # ค่าเริ่มต้นอารมณ์
        if category == 'วิทยาศาสตร์':
            if self.previous_category == 'เชิงอารมณ์' and self.previous_emotion < 30:
                emotion = random.randint(10, 40)
            else:
                emotion = random.randint(50, 80)
        
        elif category == 'ความรู้ทั่วไป':
            if self.previous_category == 'วิทยาศาสตร์' and self.previous_emotion < 60:
                emotion = random.randint(30, 60)
            else:
                emotion = random.randint(70, 100)
        
        elif category == 'เชิงอารมณ์':
            # หากเป็นหมวด "เชิงอารมณ์" และไม่มีหมวดก่อนหน้า
            if self.previous_category is None:
                emotion = 100  # กำหนดอารมณ์เริ่มต้นเป็น 100
            else:
                # คำนวณอารมณ์ใน "เชิงอารมณ์" ตามอารมณ์ก่อนหน้า
                if self.previous_category == 'เชิงอารมณ์' and self.previous_emotion >= 30:
                    emotion = random.randint(20, 50)
                else:
                    emotion = random.randint(self.previous_emotion - 10, self.previous_emotion + 10)

        # อัปเดตค่า previous_category และ previous_emotion
        self.previous_category = category
        self.previous_emotion = emotion

        return emotion

    def log_emotion(self, category, emotion):
        # บันทึกอารมณ์ลงใน log
        self.emotion_log.append({'category': category, 'emotion': emotion})

    def calculate_average_emotion(self):
        # คำนวณค่าเฉลี่ยอารมณ์ทั้งหมด
        total_emotion = sum([entry['emotion'] for entry in self.emotion_log])
        total_count = len(self.emotion_log)
        
        avg_emotion_science = self.calculate_category_average('วิทยาศาสตร์')
        avg_emotion_general_knowledge = self.calculate_category_average('ความรู้ทั่วไป')
        avg_emotion_emotion = self.calculate_category_average('เชิงอารมณ์')

        return {
            'total_average': total_emotion / total_count if total_count > 0 else 0,
            'science_average': avg_emotion_science,
            'general_knowledge_average': avg_emotion_general_knowledge,
            'emotion_average': avg_emotion_emotion
        }

    def calculate_category_average(self, category):
        # คำนวณค่าเฉลี่ยอารมณ์สำหรับหมวดหมู่ที่ระบุ
        category_emotions = [entry['emotion'] for entry in self.emotion_log if entry['category'] == category]
        return sum(category_emotions) / len(category_emotions) if category_emotions else 0
