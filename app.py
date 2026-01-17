import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="Health Tracker", page_icon="🌡️")
st.title("🌡️ 体調管理アプリ health")

# --- 過去のデータを読み込んでアドバイスを表示 ---
if os.path.exists("data.csv"):
    df_history = pd.read_csv("data.csv")
    
    if len(df_history) >= 1:
        # 直近3日間の平均睡眠時間を計算（データが1つでもあれば計算します）
        avg_sleep = df_history["睡眠"].tail(3).mean()
        
        st.sidebar.header("📊 あなたへのアドバイス")
        if avg_sleep < 6.0:
            st.sidebar.warning(f"⚠️ 直近の平均睡眠が {avg_sleep:.1f}時間 と短めです。")
            st.sidebar.info("今日は22時までに布団に入り、8時間睡眠を目指しましょう！")
        else:
            st.sidebar.success(f"✅ 平均 {avg_sleep:.1f}時間 眠れています。この調子です！")

# --- 入力フォーム ---
with st.form("input_form"):
    st.subheader("今日の記録を入力")
    d = st.date_input("日付", date.today())
    
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.number_input("昨夜の睡眠時間 (h)", 0.0, 24.0, 7.0, step=0.5)
        weight = st.number_input("体重 (kg)", 30.0, 150.0, 50.0, step=0.1)
    with col2:
        condition = st.select_slider("今の体調", ["悪い", "やや悪い", "普通", "良い", "最高"], value="普通")
        mood = st.select_slider("今の気分", ["悪い", "やや悪い", "普通", "良い", "最高"], value="普通")

    sensory = st.select_slider("感覚の過敏さ", ["過敏", "やや過敏", "普通", "鈍感"], value="普通")
    pain = st.text_input("痛む場所", "なし")
    
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
    st.success("記録を保存しました！画面を更新するとアドバイスが更新されます。")