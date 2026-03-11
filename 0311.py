import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="台/美股價查詢工具", layout="wide")

st.title("📊 完整版股價查詢工具")

# 側邊欄設定
with st.sidebar:
    st.header("查詢參數")
    stock_id = st.text_input("股票代號", value="2330.TW")
    start_date = st.date_input("開始日期", value=pd.to_datetime("2024-01-01"))
    end_date = st.date_input("結束日期", value=pd.to_datetime("today"))
    show_all = st.checkbox("顯示完整數據表格", value=False)
    query_button = st.button("🚀 執行查詢")

if query_button:
    try:
        # 下載數據
        data = yf.download(stock_id, start=start_date, end=end_date)
        
        if data.empty:
            st.error("❌ 找不到資料，請確認代號或日期。")
        else:
            # 確保索引是日期格式
            data.index = pd.to_datetime(data.index)
            
            # 1. 數據摘要 (Metrics)
            col1, col2, col3 = st.columns(3)
            latest_price = data['Close'].iloc[-1].item()
            max_price = data['High'].max().item()
            min_price = data['Low'].min().item()
            
            col1.metric("最新收盤價", f"{latest_price:.2f}")
            col2.metric("期間最高價", f"{max_price:.2f}")
            col3.metric("期間最低價", f"{min_price:.2f}")

            # 2. 股價走勢圖 (強制繪製)
            st.subheader("📈 股價走勢圖 (收盤價)")
            # 這裡我們只取 Close 欄位來畫圖
            st.line_chart(data['Close'])

            # 3. 數據表格
            st.subheader("📅 數據清單")
            if show_all:
                st.dataframe(data) # 顯示全部
            else:
                st.write("目前顯示最後 10 筆數據 (勾選左側可看全部)：")
                st.dataframe(data.tail(10))

            # 4. 下載功能
            csv = data.to_csv().encode('utf-8')
            st.download_button("📥 下載完整 CSV 報表", csv, f"{stock_id}.csv", "text/csv")

    except Exception as e:
        if "Too Many Requests" in str(e):
            st.error("⚠️ 請求太頻繁了！Yahoo Finance 暫時拒絕連線，請等幾分鐘再試。")
        else:
            st.error(f"發生錯誤: {e}")
