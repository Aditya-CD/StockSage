import numpy as np
import pandas as pd
import yfinance as yf
from keras.models import load_model
import streamlit as st
import matplotlib.pyplot as plt

model = load_model("C:/Users/user/OneDrive/Desktop/StockSage/StockSage.keras")

st.header("Stock Price Prediction")

stock = st.text_input("Enter Stock Ticker", "GOOG")
start = '2012-01-01'
end = '2025-07-01'

data = yf.download(stock, start=start, end=end)

st.subheader(f"Stock Data for {stock}")
st.write(data)

data_train = pd.DataFrame(data.Close[0: int(len(data)*0.80)])
data_test = pd.DataFrame(data.Close[int(len(data)*.80): len(data)])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

past_100 = data_train.tail(100)
data_test = pd.concat([past_100, data_test], ignore_index = True)
data_test_scaler = scaler.fit_transform(data_test)

st.subheader("OG Price vs MA50")
ma_50 = data.Close.rolling(50).mean()
fig1 = plt.figure(figsize=(10, 8))
plt.plot(data.Close, label='Close Price', color='orange')
plt.plot(ma_50, label='MA50', color='green')
plt.title(f'MA50 for {stock}')
plt.legend()
st.pyplot(fig1)

st.subheader("OG Price vs MA50 vs MA100")
ma_50 = data.Close.rolling(50).mean()
ma_100 = data.Close.rolling(100).mean()
fig2 = plt.figure(figsize=(10, 8))
plt.plot(data.Close, label='Close Price', color='orange')
plt.plot(ma_50, label='MA50', color='green')
plt.plot(ma_100, label='MA100', color='blue')
plt.title(f'MA50 and MA100 for {stock}')
plt.legend()
st.pyplot(fig2)

st.subheader("OG Price vs MA100 vs MA200")
ma_200 = data.Close.rolling(200).mean()
fig3 = plt.figure(figsize=(10, 8))
plt.plot(data.Close, label='Close Price', color='orange')
plt.plot(ma_100, label='MA100', color='blue')
plt.plot(ma_200, label='MA200', color='purple')
plt.title(f'MA100 and MA200 for {stock}')
plt.legend()
st.pyplot(fig3)

x=[]
y=[]

for i in range(100, data_test_scaler.shape[0]):
    x.append(data_test_scaler[i-100:i])
    y.append(data_test_scaler[i,0])

x, y = np.array(x), np.array(y)

predict = model.predict(x)

scale = 1/scaler.scale_[0]
predict = predict * scale
y = y * scale

st.subheader("Predicted vs Actual Price")
fig4 = plt.figure(figsize=(10, 8))
plt.plot(y, label='Actual Price', color='blue')
plt.plot(predict, label='Predicted Price', color='orange')
plt.title(f'Predicted vs Actual Price for {stock}')
plt.legend()
st.pyplot(fig4)

st.subheader("Predicted vs Actual Price (Zoomed In)")
fig5 = plt.figure(figsize=(10, 8))
plt.plot(y[-100:], label='Actual Price', color='blue')
plt.plot(predict[-100:], label='Predicted Price', color='orange')
plt.title(f'Predicted vs Actual Price (Zoomed In) for {stock}')
plt.legend()
st.pyplot(fig5)