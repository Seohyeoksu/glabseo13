import os
from openai import OpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
st.set_page_config(
    page_title="업무계획서 작성 도우미",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="auto",
)

# Custom CSS for a professional yet approachable UI
st.markdown("""
    <style>
        .main {
            background-color: #F9FAFB;
        }
        h1 {
            color: #007BFF;
            text-align: center;
            font-family: 'Arial', sans-serif;
        }
        .instructions {
            background-color: #EBF5FF;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #90CAF9;
            margin-bottom: 20px;
        }
        .section {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            border-left: 5px solid #007BFF;
        }
        .button {
            background-color: #007BFF;
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            width: 100%;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .footer {
            text-align: left;
            font-size: 14px;
            margin-top: 20px;
            color: #6C757D;
            padding: 20px 0;
            border-top: 1px solid #E0E0E0;
            display: flex;
            align-items: center;
        }
        .footer img {
            width: 80px;
            margin-right: 10px;
            vertical-align: middle;
        }
    </style>
""", unsafe_allow_html=True)

# Title of the application with a matching icon
st.markdown("<h1>📊 업무계획서 작성 도우미 🗂️</h1>", unsafe_allow_html=True)

# Instructions for users with an improved layout and icons
st.markdown("""
<div class="instructions">
    <h3>사용 설명서 📝</h3>
    <ul>
        <li>📝 <strong><span style="color:#007BFF">계획서 내용</span></strong>: 작성할 계획서의 주요 내용을 입력하세요.</li>
        <li>👥 <strong><span style="color:#007BFF">분류 선택</span></strong>: 계획서의 분류(교육활동 계획, 사업 계획, 행사 운영 계획, 지원 계획, 연수 계획)를 선택하세요.</li>
        <li>🗂️ <strong><span style="color:#007BFF">항목 선택</span></strong>: 계획서의 주요 항목을 선택하세요.</li>
        <li>🔍 <strong><span style="color:#007BFF">세부 계획 항목</span></strong>: 세부 추진 계획의 하위 항목을 선택하세요.</li>
        <li>🚀 모든 정보를 입력한 후 <strong>'생성하기'</strong> 버튼을 클릭하면, 계획서가 생성됩니다.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# User inputs organized in sections with better layout
st.markdown("<div class='section'>", unsafe_allow_html=True)

# Main content input
topic_keyword = st.text_area("📝 계획서 내용", height=100, placeholder="작성하고자 하는 계획서 주요 내용을 입력하세요.")

# Audience selection
audience_options = ["교육활동 계획", "사업 계획", "행사 운영 계획", "지원 계획", "연수 계획"]
selected_audience = st.selectbox("👥 분류", audience_options)

# Main sections selection
grade_options = ["추진배경", "목적", "운영 방침", "기본방향", "세부 추진 계획", "기대효과", "행정사항"]

selected_grades = []
show_sub_items = False  # Flag to show or hide sub-items

for grade in grade_options:
    if grade == "세부 추진 계획":
        if st.checkbox(f"🗂️ {grade}"):
            selected_grades.append(grade)
            show_sub_items = True
            # Use an expander to show sub-items directly below "세부 추진 계획"
            with st.expander("🔍 세부 계획 항목 선택"):
                sub_items = ["일정", "대상", "프로그램", "예산계획", "역할 및 업무분장", "행사 시상", "교육활동", "안전교육"]
                selected_sub_items = []
                for item in sub_items:
                    if st.checkbox(f"🔸 {item}"):
                        selected_sub_items.append(item)
    else:
        if st.checkbox(f"🗂️ {grade}"):
            selected_grades.append(grade)

# Document length selection
subject_options = ["1,000자", "2,000자", "3,000자","4,000자", "5,000자"]
subject_keyword = st.selectbox("📏 분량 선택", subject_options)

# Generate the plan on button click
if st.button('🚀 생성하기', key='generate_button'):
    with st.spinner('계획서를 생성 중입니다...'):
        # Ensure there are selected grades
        if not selected_grades:
            st.warning("항목을 하나 이상 선택하세요.")
        else:
            # Combine keywords into a single input
            grades_combined = ' , '.join(selected_grades)
            keywords_combined = f"계획서 내용: {topic_keyword}, 분류: {selected_audience}, 항목: {grades_combined}, 세부항목: {', '.join(selected_sub_items) if show_sub_items else ''}, 분량: {subject_keyword}"      
        
        chat_completion = client.chat.completions.create(
            
            messages=[
                {
                    "role": "user",
                    "content": keywords_combined,
                },
                {
                    "role": "system",
                    "content": 
                        "당신은 학교의 교육 활동을 계획하는 전문가입니다. 계획서 내용, 항목, 세부항목을 바탕으로 계획서를 작성해야 한다."
                        "1. 세부항목만 표와 글이 함께 들어여가 한다. 세부항목은 항목 중 세부 추진 계획의 구체적인 내용이기 때문에 꼭 함께 같이 작성되어야 한다 "
                        "2. 입력된 순서대로 작성해야 한다. 좋겠어."
                        "3. 출력시 항목과 세부항목은 합쳐서 나와야 한다."
                        "2. 입력된 분량에 맞게 계획서를 작성해야 한다."
                        "3. 계획서 내용을 바탕으로 구체적으로 작성하면 좋겠어."
                        "4. 세부항목만 표와 글이 함께 들어가야 한다 그리고 아주 상세하게 작성해야 한다."
                        "5. 항목과 세부항목이 전체의 90% 이상을 차지해야한다."
                        "6. 입력된 항목 중에서만 추진배경, 목적, 방침, 기대효과, 행정사항은 2~3문장으로 짧고 간결하게 작성해야 한다."
                        "7. 입력된 항목은 1,2,3,4 순으로 번호를 매겨야 한다. 항목 내용은 가,나,다 순으로 번호를 매겨야 한다. 그리고 계획서에 아이콘이 있으면 안된다"
                        "8. 문장은 간결해야 한다. "
                        "9. 일정과 프로그램이 입력되었다면 상세하고 구체적으로 작성해야 한다"
                        "10.입력되지 않은 항목은 출력하면 안된다"
                        
                }
            ],
            model="gpt-4o",
        )

        # Extract the generated content
        result = chat_completion.choices[0].message.content

        # Display the result in Streamlit app
        st.write(result)
        
        # Footer with creator information and icon
st.markdown("""
<div class="footer">
    <img src="https://huggingface.co/spaces/powerwarez/gailabicon/resolve/main/gailab06.png" alt="icon"> 제작자: 교사 서혁수
</div>
""", unsafe_allow_html=True)
