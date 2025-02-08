from model import QuestionModel

model = QuestionModel()

previous_category = None
previous_emotion = None

def handle_question_request(category):
    global previous_category, previous_emotion

    # เลือกคำถามตามประเภทที่เลือก
    try:
        question = model.get_random_question_by_category(category)
    except ValueError as e:
        return {'error': str(e)}  # ถ้าหากไม่พบคำถามในหมวดหมู่

    # คำนวณอารมณ์
    emotion = model.calculate_emotion(category)

    # บันทึกข้อมูลอารมณ์
    model.log_emotion(category, emotion)

    # อัปเดตค่าหมวดหมู่และอารมณ์ก่อนหน้า
    previous_category = category
    previous_emotion = emotion

    # คำนวณค่าเฉลี่ยอารมณ์
    average_emotions = model.calculate_average_emotion()

    # ส่งกลับคำตอบแทนคำถาม
    return {
        'question': question['question'],  # ส่งคำถาม
        'answer': question['answer'],      # ส่งคำตอบ
        'emotion': emotion,                # ส่งอารมณ์ที่คำนวณได้
        'average_emotions': average_emotions  # ส่งค่าเฉลี่ยอารมณ์
    }
