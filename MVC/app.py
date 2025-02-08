from flask import Flask, render_template, request, jsonify
from controller import handle_question_request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    category = request.form['category']  # รับค่า category จากฟอร์มที่ส่งมา
    result = handle_question_request(category)

    # ตรวจสอบว่า 'answer' และ 'question' มีค่าหรือไม่
    print(f"Question: {result['question']}, Answer: {result['answer']}")  # เพิ่มการ print เพื่อดูค่าที่ส่งกลับ

    # ส่งผลลัพธ์กลับไปยังหน้าเว็บในรูปแบบ JSON
    return jsonify({
        'question': result['question'],  # ส่งคำถาม
        'answer': result['answer'],      # ส่งคำตอบ
        'emotion': result['emotion'],    # ส่งอารมณ์ที่คำนวณได้
        'average_emotions': result['average_emotions']  # ส่งค่าเฉลี่ยอารมณ์
    })

if __name__ == '__main__':
    app.run(debug=True)
