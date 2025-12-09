import streamlit as st
import yfinance as yf
import pandas as pd

# 設定頁面標題
st.set_page_config(page_title="即時倉位計算器", page_icon="⚡", layout="centered")

st.title("⚡ 交易倉位計算器")
st.markdown("連線 Yahoo Finance 自動抓取「匯率」與「今日開盤價」")

# --- 核心邏輯資料庫 ---
instruments = {
    "GER40 (DAX)": {
        "currency": "EUR", 
        "sizes": {"零售標準 (1點=1歐)": 1, "期貨規格 (1點=25歐)": 25, "迷你規格 (1點=10歐)": 10},
        "ticker": "EURUSD=X",     
        "index_ticker": "^GDAXI"  
    },
    "UK100 (FTSE)": {
        "currency": "GBP", 
        "sizes": {"零售標準 (1點=1鎊)": 1, "大合約 (1點=10鎊)": 10},
        "ticker": "GBPUSD=X",
        "index_ticker": "^FTSE"
    },
    "US30 (Dow Jones)": {
        "currency": "USD", 
        "sizes": {"零售標準 (1點=1鎂)": 1, "大合約 (1點=10鎂)": 10, "特殊規格 (1點=5鎂)": 5},
        "ticker": "USD",
        "index_ticker": "^DJI"
    },
    "EU50 (Stoxx 50)": {
        "currency": "EUR", 
        "sizes": {"零售標準 (1點=1歐)": 1, "期貨規格 (1點=10歐)": 10},
        "ticker": "EURUSD=X",
        "index_ticker": "^STOXX50E"
    },
    "AUS200 (ASX 200)": {
        "currency": "AUD",
        "sizes": {"零售標準 (1點=1澳)": 1, "期貨規格 (1點=25澳)": 25},
        "ticker": "AUDUSD=X",
        "index_ticker": "^AXJO"
    },
    "Custom (自訂)": {
        "currency": "Custom",
        "sizes": {"自訂合約": 1},
        "ticker": "Manual",
        "index_ticker": None
    }
}

# --- 版面配置：左 3 右 1 ---
col_left, col_right = st.columns(2)

# === 左欄：輸入設定 (順序：商品 -> 規格 -> 金額) ===
with col_left:
    # 1. 選擇商品
    symbol = st.selectbox("1️⃣ 選擇交易商品", list(instruments.keys()))
    selected_inst = instruments[symbol]
    
    # 2. 選擇規格
    size_options = list(selected_inst["sizes"].keys())
    size_choice = st.selectbox("2️⃣ 合約規格", size_options)
    contract_size = selected_inst["sizes"][size_choice]
    
    if symbol == "Custom (自訂)":
        contract_size = st.number_input("手動輸入每點價值", value=1.0)
        
    # 3. 設定虧損
    max_risk = st.number_input("3️⃣ 最大虧損金額 (USD)", value=3000.0, step=100.0)

# === 資料抓取邏輯 (匯率 + 開盤價) ===
exchange_rate = 1.0
rate_msg = ""
default_open_price = 0.0
rate_color = "blue" # 裝飾用顏色

# 抓匯率
if selected_inst["ticker"] == "USD":
    exchange_rate = 1.0
    rate_msg = "1.0 (USD)"
    rate_color = "gray"
elif selected_inst["ticker"] == "Manual":
    rate_msg = "手動輸入"
else:
    try:
        ticker_data = yf.Ticker(selected_inst["ticker"])
        data = ticker_data.history(period="1d", interval="1m")
        if not data.empty:
            exchange_rate = data['Close'].iloc[-1]
            last_time = data.index[-1].strftime('%H:%M')
            rate_msg = f"{exchange_rate:.4f} (更新: {last_time})"
            rate_color = "green"
        else:
            data_daily = ticker_data.history(period="1d")
            if not data_daily.empty:
                exchange_rate = data_daily['Close'].iloc[-1]
                rate_msg = f"{exchange_rate:.4f} (收盤價)"
                rate_color = "orange"
            else:
                rate_msg = "無法抓取"
                rate_color = "red"
    except:
        rate_msg = "連線錯誤"
        rate_color = "red"

# 抓開盤價 (預設進場價)
if selected_inst["index_ticker"]:
    try:
        index_data = yf.Ticker(selected_inst["index_ticker"]).history(period="1d")
        if not index_data.empty:
            default_open_price = index_data['Open'].iloc[-1]
    except:
        default_open_price = 0.0

# === 右欄：顯示匯率 ===
with col_right:
    st.markdown(f"**參考匯率 ({selected_inst['currency']}/USD)**")
    
    if selected_inst["ticker"] == "Manual":
        exchange_rate = st.number_input("輸入匯率", value=1.0, format="%.4f")
    else:
        if rate_color == "green":
            st.success(f"✅ {rate_msg}")
        elif rate_color == "gray":
            st.info(f"🇺🇸 {rate_msg}")
        else:
            st.warning(f"⚠️ {rate_msg}")
            
    if st.button("🔄 刷新匯率"):
        st.rerun()

st.markdown("---")

# --- 下方區塊：價格輸入 (兩個都預填開盤價) ---
price_col1, price_col2 = st.columns(2)

with price_col1:
    entry_price = st.number_input(
        "🚀 進場價格", 
        value=float(default_open_price), 
        format="%.2f",
        key=f"entry_{symbol}" # 切換商品時重置
    )

with price_col2:
    # 修改處：止損價格現在也會自動填入 default_open_price
    stop_loss = st.number_input(
        "🛑 止損價格", 
        value=float(default_open_price), 
        format="%.2f",
        key=f"sl_{symbol}" # 加上 key 確保切換商品時會更新
    )

st.markdown("<br>", unsafe_allow_html=True) 

# --- 按鈕與計算 ---
if st.button("🚀 開始計算 (Calculate)", type="primary", use_container_width=True):
    
    if entry_price > 0 and stop_loss > 0:
        distance = abs(entry_price - stop_loss)
        value_per_point_usd = contract_size * exchange_rate
        risk_per_lot_usd = distance * value_per_point_usd
        
        if risk_per_lot_usd > 0:
            recommended_lots = max_risk / risk_per_lot_usd
        else:
            recommended_lots = 0

        # --- 結果顯示 ---
        st.markdown("### 📊 建議倉位")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("止損距離", f"{distance:.1f} 點")
        res_col2.metric("每手波動價值 (USD)", f"${value_per_point_usd:.2f}")
        res_col3.metric("建議下單手數", f"{recommended_lots:.2f} Lots")

        with st.expander("查看詳細計算過程", expanded=True):
            # 修復：修正了原本的粗體顯示問題
            st.markdown(f"""
            1. **匯率換算**: {selected_inst['currency']} 兌 USD 匯率為 **{exchange_rate:.4f}**
            2. **合約價值**: 選定規格為 **{contract_size}** {selected_inst['currency']}/點 
               → 換算為 **${value_per_point_usd:.2f} USD/點**
            3. **風險承受**: 總風險 **{max_risk}** / 單手風險 **{risk_per_lot_usd:.2f}** = **{recommended_lots:.4f} 手**
            """)
            
        if recommended_lots > 50:
            st.error("⚠️ 手數異常大，請檢查是否選錯合約規格！")
    
    else:
        st.warning("⚠️ 請輸入大於 0 的進場與止損價格")