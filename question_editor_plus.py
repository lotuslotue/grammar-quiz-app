import streamlit as st
import json
import os
import pandas as pd


FILE_PATH = "questions.json"

# 加载题库
def load_questions():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 保存题库
def save_questions(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="题库管理升级版", page_icon="📚")
st.title("📚 语法选择题题库管理 + 批量导入")

questions = load_questions()

# ==============================
# ✏️ 编辑已有题目 + 删除功能
# ==============================
st.subheader("✏️ 编辑/删除已有题目")

for i, q in enumerate(questions):
    with st.expander(f"题目 {i+1}：{q['sentence']}"):
        q["sentence"] = st.text_input(f"句子 {i+1}", q["sentence"], key=f"sen{i}")
        q["options"][0] = st.text_input(f"选项 A", q["options"][0], key=f"optA{i}")
        q["options"][1] = st.text_input(f"选项 B", q["options"][1], key=f"optB{i}")
        q["options"][2] = st.text_input(f"选项 C", q["options"][2], key=f"optC{i}")
        q["answer"] = st.selectbox("正确答案", q["options"], index=q["options"].index(q["answer"]), key=f"ans{i}")
        q["explanation"] = st.text_area("解释", q["explanation"], key=f"exp{i}")
        q["translation"] = st.text_input("英文翻译", q.get("translation", ""), key=f"tran{i}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"💾 保存第{i+1}题修改", key=f"save{i}"):
                save_questions(questions)
                st.success("✅ 修改已保存！")

        with col2:
            if st.button(f"❌ 删除第{i+1}题", key=f"del{i}"):
                questions.pop(i)
                save_questions(questions)
                st.success("🗑️ 题目已删除！")
                rerun()  # ✅ 使用新版 rerun 方法刷新页面

# ==============================
# ➕ 添加新题目
# ==============================
st.subheader("➕ 手动添加新题目")
with st.form("add_form"):
    sentence = st.text_input("📌 题目句子（用 ___ 表示空格）")
    option1 = st.text_input("选项 A")
    option2 = st.text_input("选项 B")
    option3 = st.text_input("选项 C")
    answer = st.selectbox("✅ 正确答案", [option1, option2, option3])
    explanation = st.text_area("📖 语法解释")
    translation = st.text_input("🌍 英文翻译（可选）")
    submitted = st.form_submit_button("添加题目")
if submitted:
    new_q = {
        "sentence": sentence,
        "options": [option1, option2, option3],
        "answer": answer,
        "explanation": explanation,
        "translation": translation
    }
    questions.append(new_q)
    save_questions(questions)
    st.success("✅ 新题目已添加！")

# ==============================
# 📤 批量导入 Excel 文件
# ==============================
st.subheader("📤 批量导入题目（通过 Excel 文件）")
uploaded_file = st.file_uploader("请上传 Excel 文件（字段包括 sentence, option1, option2, option3, answer, explanation, translation）", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        new_data = []
        for _, row in df.iterrows():
            item = {
                "sentence": row["sentence"],
                "options": [row["option1"], row["option2"], row["option3"]],
                "answer": row["answer"],
                "explanation": row["explanation"],
                "translation": row.get("translation", "")
            }
            new_data.append(item)
        questions.extend(new_data)
        save_questions(questions)
        st.success(f"✅ 成功导入 {len(new_data)} 道题目！请刷新查看")
    except Exception as e:
        st.error(f"❌ 导入失败：{e}")

