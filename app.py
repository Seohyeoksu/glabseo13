import os
from openai import OpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
st.set_page_config(
    page_title="업무 계획서",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="auto",
)

# Custom CSS for an elementary school-themed UI
st.markdown("""
    <style>
        .main {
            background-color: #FFF8E1; /* Light yellow background for a cheerful feel */
        }
        h1 {
            color: #FF5722; /* Bright orange for a playful heading */
            text-align: center;
            font-family: 'Comic Sans MS', cursive, sans-serif; /* Fun, informal font */
        }
        .instructions {
            background-color: #FFECB3; /* Pale yellow for a warm, inviting tone */
            padding: 15px;
            border-radius: 15px;
            border: 2px dashed #FFB74D; /* Dashed orange border for a fun look */
            margin-bottom: 20px;
        }
        .section {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            border-left: 5px solid #FF9800; /* Orange left border to tie into the playful theme */
        }
        .button {
            background-color: #FF9800;
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
            background-color: #F57C00;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            margin-top: 20px;
            color: #757575;
        }
    </style>
""", unsafe_allow_html=True)

# Title of the application with emojis
st.markdown("<h1>📚 업무 계획서 작성 봇 🎒</h1>", unsafe_allow_html=True)

# Instructions for users with card style and emojis
st.markdown("""
<div class="instructions">
    <h3>사용 설명서 ✏️📋</h3>
    <ul>
        <li>📝 <strong><span style="color:#F57C00">계획서 내용</span></strong>: 계획서 작성을 위한 핵심 키워드를 여기에 써주세요.</li>
        <li>🌸 <strong><span style="color:#0288D1">항목 선택</span></strong>: 계획서의 항목을 선택하여 주세요.</li>
        <li>🔍 <strong><span style="color:#8E24AA">분량 선택</span></strong>: 계획서의 분량을 선택하여 주세요.</li>
        <li>🚀 모든 정보를 입력한 후 <strong>'생성하기'</strong> 버튼을 클릭하면, 계획서가 생성됩니다.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# User inputs organized in sections with better layout
st.markdown("<div class='section'>", unsafe_allow_html=True)

topic_keyword = st.text_area("🔤 계획서 내용", height=100, placeholder="계획서 주요 내용을 여기에 입력하여 주세요.")

grade_options = ["🌸 추진배경", "☀️ 목적", "🍂 방침", "❄️ 세부 추진 계획", "🙏 기대효과", "💬 행정사항"]

# Collecting selected checkboxes
selected_grades = []
for grade in grade_options:
    if st.checkbox(grade):
        selected_grades.append(grade)

subject_options = ["📄 A4 1 page", "📢 A4 2 page", "📊 A4 3 page", "📚 A4 4 page"]
subject_keyword = st.selectbox("🎯 분량", subject_options)

st.markdown("</div>", unsafe_allow_html=True)

if st.button('✨ 생성하기', key='generate_button'):
    with st.spinner('생성 중입니다...'):
        # Ensure there are selected grades
        if not selected_grades:
            st.warning("항목을 하나 이상 선택하여 주세요.")
        else:
            # Combine keywords into a single input
            grades_combined = ', '.join(selected_grades)
            keywords_combined = f"계획서 내용: {topic_keyword}, 항목 : {grades_combined}, 분량: {subject_keyword}"           
        # Create a chat completion request to OpenAI API"
        
        chat_completion = client.chat.completions.create(
            
            messages=[
                {
                    "role": "user",
                    "content": keywords_combined,
                },
                {
                    "role": "system",
                    "content": 
                        "당신은 학교의 교육활동을 계획하는 전문가입니다. 입력된 계획서 내용, 항목, 분량을 바탕으로 계획서를 작성해야 한다."
                        "1. 입력된 계획서 내용을 바탕으로 계획서를 작성해야 한다."
                        "2. 입력된 항목만 계획서에 포함시켜야 한다."
                    
                }
            ],
            model="gpt-4o",
        )

        # Extract the generated content
        result = chat_completion.choices[0].message.content

        # Display the result in Streamlit app
        st.write(result)