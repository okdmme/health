import streamlit as st
import pandas as pd
import os
from datetime import date  # これが抜けているとエラーになります
import google.generativeai as genai

# --- AIの設定 ---
# 先ほど取得したAPIキーをここに入れます
# ※ GitHubに上げる際は、このキーを消すか .env を使うようにしましょう
genai.configure(api_key="あなたのAPIキーをここに貼り付け")
model = genai.GenerativeModel('gemini-1.5-flash')

# ページ全体の初期設定（一番最初に書く必要があります）
st.set_page_config(page_title="Health Tracker", page_icon="🌡️")
st.title("🌡️ 体調管理アプリ health")

# --- AIアドバイス機能（サイドバー） ---
if os.path.exists("data.csv"):
    df_history = pd.read_csv("data.csv")
    if len(df_history) >= 3:
        st.sidebar.header("🤖 AI健康診断")
        if st.sidebar.button("AIにアドバイスをもらう"):
            # データをテキスト化
            recent_data = df_history.tail(7).to_string(index=False)
            
            # 指示を短くして「考える時間」を減らす
            prompt = f"以下の健康データを簡潔に分析し、1行でアドバイスをください：\n{recent_data}"
            
            with st.sidebar:
                with st.spinner("AIが思考中..."):
                    try:
                        # stream=True で逐次生成
                        response = model.generate_content(prompt, stream=True)
                        # 文字が生成された順にリアルタイム表示
                        st.write_stream(response)
                    except Exception as e:
                        st.error(f"AIエラー: {e}")

# --- 過去の統計アドバイス（サイドバー） ---
if os.path.exists("data.csv"):
    if len(df_history) >= 1:
        avg_sleep = df_history["睡眠"].tail(3).mean()
        st.sidebar.header("📊 統計アドバイス")
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
    st.success("記録を保存しました！画面を更新（F5）するとアドバイスが反映されます。")