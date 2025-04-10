import streamlit as st
import json
import pandas as pd
from datetime import datetime
import os

# 页面设置
st.set_page_config(page_title="语法选择题练习", page_icon="📘", layout="centered")

# 初始化状态
if "questions" not in st.session_state:
    with open("questions.json", "r", encoding="utf-8") as f:
        st.session_state.questions = json.load(f)

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

questions = st.session_state.questions
total = len(questions)

st.title("📘 助词语法选择题练习")

# ✅ 学生姓名输入，防止按钮重复 key
if not st.session_state.student_name:
    name = st.text_input("🧑‍🎓 请输入你的姓名：")
    if st.button("开始练习", key="start_button") and name.strip():
        st.session_state.student_name = name.strip()
        st.rerun()
    elif st.button("开始练习", key="start_button_warn"):
        st.warning("⚠️ 请填写你的姓名后再开始")
    st.stop()

# ✅ 每题一个页面
if not st.session_state.submitted and st.session_state.current_question < total:
    i = st.session_state.current_question
    q = questions[i]

    st.markdown(f"👤 学生：{st.session_state.student_name}")
    st.markdown(f"**第 {i + 1} 题 / 共 {total} 题**")
    st.markdown(f"**句子：** {q['sentence']}")

    selected = st.radio("请选择一个答案：", q["options"], index=None, key=f"q_{i}")

    if st.button("✅ 提交并进入下一题", key=f"next_button_{i}"):
        if selected is None:
            st.warning("⚠️ 请先选择一个答案！")
        else:
            st.session_state.user_answers[i] = selected
            st.session_state.current_question += 1
            st.rerun()

# ✅ 所有题目完成，标记提交
elif not st.session_state.submitted and st.session_state.current_question >= total:
    st.session_state.submitted = True
    st.rerun()

# ✅ 提交后显示结果 + 保存成绩
elif st.session_state.submitted:
    st.subheader("📊 答题结果")
    score = 0
    records = []

    for i, q in enumerate(questions):
        user_ans = st.session_state.user_answers.get(i, "")
        correct = user_ans == q["answer"]
        if correct:
            st.success(f"第 {i+1} 题：正确 ✅")
            score += 1
        else:
            st.error(f"第 {i+1} 题：错误 ❌ 正确答案是：{q['answer']}")

        st.markdown(f"📖 语法解释：{q['explanation']}")
        if q.get("translation"):
            st.markdown(f"🌍 翻译：{q['translation']}")
        st.markdown("---")

        records.append({
            "姓名": st.session_state.student_name,
            "题号": i + 1,
            "句子": q["sentence"],
            "选择答案": user_ans,
            "正确答案": q["answer"],
            "是否正确": "✅" if correct else "❌"
        })

    st.subheader(f"🎯 总得分：{score} / {len(questions)}")

    # ✅ 保存成绩
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = {
        "姓名": st.session_state.student_name,
        "得分": score,
        "总题数": len(questions),
        "提交时间": timestamp
    }

    summary_df = pd.DataFrame([summary])
    detail_df = pd.DataFrame(records)
    file_path = "scores.xlsx"

    if os.path.exists(file_path):
        with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="overlay", engine="openpyxl") as writer:
            start_row = pd.read_excel(file_path, sheet_name="成绩").shape[0] + 1
            summary_df.to_excel(writer, sheet_name="成绩", index=False, header=False, startrow=start_row)
            detail_df.to_excel(writer, sheet_name=st.session_state.student_name, index=False)
    else:
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            summary_df.to_excel(writer, sheet_name="成绩", index=False)
            detail_df.to_excel(writer, sheet_name=st.session_state.student_name, index=False)

    st.success("✅ 成绩已保存！")

# ✅ 重新开始按钮（防冲突）
if st.button("🔁 重新开始练习", key="reset_button"):
    for key in ["submitted", "current_question", "user_answers", "questions", "student_name"]:
        st.session_state.pop(key, None)
    st.rerun()
