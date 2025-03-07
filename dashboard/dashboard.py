import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load dataset (pastikan ukuran file sudah diperkecil sebelumnya)
df = pd.read_csv("main_data.csv")

# konversi tanggal order ke format datetime
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

# sidebar
st.sidebar.image("https://cdn.pixabay.com/photo/2024/06/13/17/33/graph-8828099_1280.png")
selected_state = st.sidebar.multiselect("Pilih State Pelanggan", df["customer_state"].unique())

# fungsi untuk filter berdasarkan state pelanggan
def filter_data(df, states):
    if states:
        return df[df["customer_state"].isin(states)]
    return df

filtered_df = filter_data(df, selected_state)

# dashboard title
st.header("📊 E-Commerce Dashboard")

# overview metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Transaksi", filtered_df["order_id"].nunique())
col2.metric("Total Pendapatan", f"${filtered_df['price'].sum():,.2f}")
col3.metric("Jumlah Pelanggan", filtered_df["customer_id"].nunique())

# tren transaksi bulanan
st.subheader("📈 Tren Transaksi Pelanggan")
monthly_orders = filtered_df.groupby(filtered_df["order_purchase_timestamp"].dt.to_period("M")).size()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=monthly_orders.index.astype(str), y=monthly_orders.values, marker='o', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Order")
ax.set_title("Tren Jumlah Order Per Bulan")
plt.xticks(rotation=45)
st.pyplot(fig)

# kategori produk paling diminati
st.subheader("🏷️ Kategori Produk Paling Populer")
top_categories = filtered_df["product_category_name"].value_counts().head(10)
st.bar_chart(top_categories)

# metode pembayaran paling banyak digunakan
st.subheader("💳 Metode Pembayaran Favorit")
payment_counts = filtered_df["payment_type"].value_counts()
st.bar_chart(payment_counts)

# distribusi pelanggan berdasarkan state
st.subheader("🌍 Distribusi Pelanggan Berdasarkan State")
state_counts = filtered_df["customer_state"].value_counts()
st.bar_chart(state_counts)

# best customers (RFM Analysis)
st.subheader("👑 Best Customers (RFM Analysis)")
rfm_df = filtered_df.groupby("customer_id").agg({
    "order_purchase_timestamp": "max",  
    "order_id": "count",  
    "price": "sum"  
})
rfm_df.columns = ["last_purchase", "frequency", "monetary"]
rfm_df["last_purchase"] = pd.to_datetime(rfm_df["last_purchase"])
rfm_df["recency"] = (df["order_purchase_timestamp"].max() - rfm_df["last_purchase"]).dt.days

# pelanggan terbaik berdasarkan recency, frequency, monetary
best_customers = rfm_df.sort_values(by=["recency", "frequency", "monetary"], ascending=[True, False, False]).head(5)
st.write(best_customers)

st.caption('Copyright (c) 2025')