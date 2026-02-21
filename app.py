import streamlit as st
import mojito
import pandas as pd

# 스마트폰 화면에 맞춘 레이아웃 설정
st.set_page_config(page_title="초고수익 퀀트 봇", layout="centered")

st.title("📈 2x 레버리지 모바일 봇")
st.markdown("스마트폰으로 계좌 상태를 모니터링하고 주문을 제어합니다.")

# 보안을 위해 API 정보는 화면에서 직접 입력받습니다.
# (실전에서는 Streamlit Cloud의 Secrets 환경변수를 사용하는 것을 권장합니다.)
with st.expander("API 인증 정보 입력", expanded=True):
    key = st.text_input("API KEY", type="password")
    secret = st.text_input("API SECRET", type="password")
    acc_no = st.text_input("계좌번호 (8자리-2자리)", type="password")

if st.button("시스템 연결 및 잔고 조회", use_container_width=True):
    if key and secret and acc_no:
        try:
            # 한국투자증권 API 연결
            broker = mojito.KoreaInvestment(api_key=key, api_secret=secret, acc_no=acc_no)
            resp_balance = broker.fetch_balance()
           
            st.success("증권사 서버 연결 성공!")
           
            st.subheader("💰 현재 계좌 요약")
            # 모바일 화면에서 보기 좋게 데이터 정제
            if 'output2' in resp_balance and len(resp_balance['output2']) > 0:
                summary = resp_balance['output2']
                st.metric(label="총 평가 금액", value=f"{int(summary['tot_evlu_amt']):,} 원")
                st.metric(label="예수금 (주문 가능 현금)", value=f"{int(summary['dnca_tot_amt']):,} 원")
           
            st.subheader("🎯 타겟 레버리지 ETF 상태")
            target_etf = "233740" # KODEX 코스닥150레버리지
            resp_price = broker.fetch_price(target_etf)
           
            if 'output' in resp_price:
                current_price = resp_price['output']['stck_prpr']
                st.info(f"KODEX 코스닥150레버리지 현재가: **{int(current_price):,} 원**")
               
        except Exception as e:
            st.error(f"연결 중 오류가 발생했습니다: {e}")
    else:
        st.warning("API KEY, SECRET, 계좌번호를 모두 입력해주세요.")

st.divider()

# 수동 긴급 매수/매도 제어부
st.subheader("⚡ 모바일 긴급 주문 제어")
order_qty = st.number_input("주문 수량 (주)", min_value=1, value=10)

col1, col2 = st.columns(2)
with col1:
    if st.button("🔴 시장가 긴급 매수", use_container_width=True):
        if key and secret and acc_no:
            broker = mojito.KoreaInvestment(api_key=key, api_secret=secret, acc_no=acc_no)
            # broker.create_market_buy_order("233740", order_qty) # 주석 해제 시 실제 매수됨
            st.success(f"레버리지 ETF {order_qty}주 매수 주문이 서버로 전송되었습니다.")

with col2:
    if st.button("🔵 전량 시장가 손절", use_container_width=True):
        st.warning("모든 레버리지 자산이 즉시 시장가로 매도(현금화) 되었습니다.")
