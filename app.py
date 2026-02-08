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
    
    [출력 지침]
    1. '오늘의 사주 분석'과 '오늘의 행운 컬러' 섹션은 <details><summary>[보기] 클릭하여 펼치기</summary>...</details> 태그를 사용해 접어두세요.
    2. '추천 코디'와 '오늘의 마음가짐'은 바로 보이도록 일반 HTML 태그로 작성하세요.
    3. 전체적인 서술은 품격 있는 '본명조' 서체에 어울리도록 차분하고 고급스럽게 작성하세요.
    
    [구성]
    <details>
        <summary>🔍 오늘의 사주 분석 [보기]</summary>
        (여기에 일주 분석 및 오늘 운세 서술)
    </details>
    
    <details>
        <summary>🎨 오늘의 행운 컬러 [보기]</summary>
        (여기에 컬러 추천 및 이유 서술)
    </details>
    
    <h3>👕 추천 코디 스타일ing</h3>
    (구체적인 코디 제안)
    
    <h3>🍀 오늘의 마음가짐</h3>
    (위트 있고 따뜻한 조언)
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
