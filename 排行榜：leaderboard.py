import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="成绩排行榜", page_icon="🏆", layout="centered")

st.title("🏆 语法练习成绩排行榜")

score_file = "scores.xlsx"

if not os.path.exists(score_file):
    st.warning("❗ 尚未有任何学生提交成绩，暂无排行榜数据。")
    st.stop()

try:
    df = pd.read_excel(score_file, sheet_name="成绩")

    # 排序并显示
    df_sorted = df.sort_values(by=["得分", "提交时间"], ascending=[False, True])
    df_sorted.reset_index(drop=True, inplace=True)

    st.success(f"📊 当前共有 {len(df_sorted)} 位学生提交过成绩")
    st.dataframe(df_sorted, use_container_width=True)

except Exception as e:
    st.error(f"读取排行榜失败：{e}")
