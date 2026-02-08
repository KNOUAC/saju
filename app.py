import os
from flask import Flask, render_template, request, jsonify
from google import genai  # 최신 라이브러리 임포트
from datetime import datetime

app = Flask(__name__)

# 최신 SDK 방식의 클라이언트 설정
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    birth_info = f"{data['year']}년 {data['month']}월 {data['day']}일 {data['time']}"
    
    prompt = f"""
    당신은 트렌디한 'AI 사주 패션 디렉터'입니다. 
    사용자 정보: {birth_info}
    오늘 날짜: 2026-02-08
    
    미션: 사용자의 일주를 분석하고, 오늘 일진에 맞는 '행운의 컬러', '코디 스타일', '마음가짐'을 
    HTML 형식(<h2>, <ul> 등 사용)으로 아주 매력적으로 제안하세요.
    """

    try:
        # 공식 가이드에 따른 최신 호출 방식
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        return jsonify({'result': response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'result': f"연결 실패: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
