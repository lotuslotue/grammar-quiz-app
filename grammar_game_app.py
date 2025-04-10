import streamlit as st
import json
import random

# 页面设置
st.set_page_config(page_title="语法选择题练习", page_icon="📘", layout="centered")

# 初始化状态
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# 加载题库
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()
random.shuffle(questions)

st.title("📘 助词语法选择题练习")

user_answers = {}

# 答题界面
if not st.session_state.submitted:
    with st.form("quiz_form"):
        for i, q in enumerate(questions):
            st.markdown(f"**第 {i+1} 题：** {q['sentence']}")
            user_answers[i] = st.radio("请选择一个答案：", q["options"], key=f"q_{i}")
            st.markdown("---")

        submitted = st.form_submit_button("✅ 提交答案")
        if submitted:
            st.session_state.submitted = True
            st.session_state.user_answers = user_answers
            st.rerun()

# 提交后显示结果
elif st.session_state.submitted:
    st.subheader("📊 答题结果")
    score = 0
    user_answers = st.session_state.user_answers

    for i, q in enumerate(questions):
        user_ans = user_answers.get(i, "")
        if user_ans == q["answer"]:
            st.success(f"第 {i+1} 题：正确 ✅")
            score += 1
        else:
            st.error(f"第 {i+1} 题：错误 ❌ 正确答案是：{q['answer']}")

        st.markdown(f"📖 语法解释：{q['explanation']}")
        if q.get("translation"):
            st.markdown(f"🌍 翻译：{q['translation']}")
        st.markdown("---")

    st.subheader(f"🎯 总得分：{score} / {len(questions)}")
    if score == len(questions):
        st.balloons()
        st.success("🎉 全对！太棒了！")
    elif score >= len(questions) * 0.7:
        st.info("👍 不错，继续加油！")
    else:
        st.warning("📚 可以再练练，慢慢来！")

# 重新开始
if st.button("🔁 重新开始练习"):
    st.session_state.clear()
    st.rerun()
