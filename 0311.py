import yfinance as yf
import pandas as pd
from datetime import datetime

def validate_date(date_text):
    """檢查日期格式是否為 YYYY-MM-DD"""
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def run_stock_query():
    print("="*30)
    print("📊 簡易台/美股價查詢工具")
    print("="*30)
    
    # 1. 取得使用者輸入
    ticker = input("請輸入股票代號 (美股如 AAPL, 台股如 2330.TW): ").strip().upper()
    start_date = input("請輸入開始日期 (YYYY-MM-DD): ").strip()
    end_date = input("請輸入結束日期 (YYYY-MM-DD): ").strip()

    # 2. 驗證日期格式
    if not (validate_date(start_date) and validate_date(end_date)):
        print("\n❌ 錯誤：日期格式不正確，請使用 YYYY-MM-DD (例如 2024-01-01)")
        return

    # 3. 下載數據
    print(f"\n🚀 正在從 Yahoo Finance 抓取 {ticker} 的資料...")
    try:
        # auto_adjust=True 會自動處理除權息後的調整股價
        data = yf.download(ticker, start=start_date, end=end_date)

        if data.empty:
            print(f"⚠️ 找不到 '{ticker}' 的資料。請檢查代號是否正確，或該時段是否為交易日。")
        else:
            # 4. 格式化輸出
            print("\n" + "查詢結果摘要".center(40, "-"))
            # 顯示最後五筆資料，讓使用者看到最新動態
            print(data.tail()) 
            print("-" * 46)
            
            # 計算簡單統計
            low_price = data['Low'].min()
            high_price = data['High'].max()
            print(f"📈 期間最高價: {high_price:.2f}")
            print(f"📉 期間最低價: {low_price:.2f}")
            
            # 問使用者是否要存檔
            save_csv = input("\n是否要將結果存為 CSV 檔案？(y/n): ").lower()
            if save_csv == 'y':
                filename = f"{ticker}_{start_date}_to_{end_date}.csv"
                data.to_csv(filename)
                print(f"✅ 檔案已儲存為: {filename}")

    except Exception as e:
        print(f"💥 發生未知錯誤: {e}")

if __name__ == "__main__":
    run_stock_query()
    print("\n查詢結束，謝謝使用！")