import streamlit as st
import pandas as pd
from datetime import date
import os

# ページの設定
st.set_page_config(page_title="Health Tracker", page_icon="🌡️")

st.title("🌡️ 体調管理アプリ health")

# 入力フォーム
with st.form("input_form"):
    st.subheader("今日の記録")
    
    d = st.date_input("日付", date.today())
    
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.number_input("睡眠時間 (h)", 0.0, 24.0, 7.0, step=0.5)
        weight = st.number_input("体重 (kg)", 30.0, 150.0, 50.0, step=0.1)
    with col2:
        condition = st.select_slider("体調", ["悪い", "やや悪い", "普通", "良い", "最高"], value="普通")
        mood = st.select_slider("気分", ["悪い", "やや悪い", "普通", "良い", "最高"], value="普通")

    sensory = st.select_slider("感覚（触覚の過敏さ）", ["過敏", "やや過敏", "普通", "鈍感"], value="普通")
    pain = st.text_input("痛む場所（なければ「なし」）", "なし")
    
    col3, col4 = st.columns(2)
    with col3:
        period = st.checkbox("生理")
    with col4:
        meds = st.checkbox("薬を飲んだ")

    meal = st.text_area("食事・メモ")
    
    submitted = st.form_submit_button("記録を保存する")

# 保存処理
if submitted:
    new_data = {
        "日付": d, "睡眠": sleep, "体調": condition, "気分": mood, 
        "感覚": sensory, "痛み": pain, "生理": period, "薬": meds, 
        "食事": meal, "体重": weight
    }
    df = pd.DataFrame([new_data])
    df.to_csv("data.csv", mode='a', index=False, header=not os.path.exists("data.csv"))
    st.success("1日目の記録完了！まずは3日間続けてみましょう！")
