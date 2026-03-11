import streamlit as st
import yfinance as yf
import pandas as pd

# 設定網頁標題
st.set_page_config(page_title="台/美股價查詢工具", layout="centered")

st.title("📊 簡易台/美股價查詢工具")
st.write("請在下方輸入資訊進行查詢")

# 1. 建立側邊欄或主頁面的輸入欄位
with st.container():
    stock_id = st.text_input("請輸入股票代號", value="2330.TW", help="美股如 AAPL, 台股如 2330.TW")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("開始日期", value=pd.to_datetime("2024-01-01"))
    with col2:
        end_date = st.date_input("結束日期", value=pd.to_datetime("today"))

    query_button = st.button("🔍 開始查詢")

# 2. 執行查詢邏輯
if query_button:
    try:
        with st.spinner('正在抓取資料中...'):
            data = yf.download(stock_id, start=start_date, end=end_date)
        
        if data.empty:
            st.warning(f"⚠️ 找不到 '{stock_id}' 的資料。請檢查代號是否正確。")
        else:
            st.success(f"✅ 已成功抓取 {stock_id} 的數據！")
            
            # 顯示統計數據
            col_a, col_b = st.columns(2)
            col_a.metric("期間最高價", f"{data['High'].max().item():.2f}")
            col_b.metric("期間最低價", f"{data['Low'].min().item():.2f}")
            
            # 顯示數據表格
            st.subheader("數據預覽 (最後五筆)")
            st.dataframe(data.tail())
            
            # 下載 CSV 按鈕
            csv = data.to_csv().encode('utf-8')
            st.download_button(
                label="📥 下載資料為 CSV",
                data=csv,
                file_name=f"{stock_id}_price.csv",
                mime='text/csv',
            )
            
            # 畫個簡單的折線圖
            st.subheader("股價走勢圖")
            st.line_chart(data['Close'])

    except Exception as e:
        st.error(f"💥 發生錯誤: {e}")

st.divider()
st.caption("數據來源：Yahoo Finance")
