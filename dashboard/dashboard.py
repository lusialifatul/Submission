import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# df = pd.read_csv("https://github.com/lusialifatul/Submission/releases/download/v1.0.0/main_data.csv")
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

# kategori produk paling diminati dan paling tidak diminati
st.subheader("🏷️ Kategori Produk Paling dan Paling Tidak Diminati")
category_counts = filtered_df["product_category_name"].value_counts().dropna()
most_popular = category_counts.head(5)
least_popular = category_counts.iloc[-5:]

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
sns.barplot(x=most_popular.values, y=most_popular.index, ax=axes[0], palette="Blues_r")
axes[0].set_title("5 Kategori Produk Paling Diminati")
axes[0].set_xlabel("Jumlah Terjual")
axes[0].set_ylabel("Kategori Produk")

sns.barplot(x=least_popular.values, y=least_popular.index, ax=axes[1], palette="Reds_r")
axes[1].set_title("5 Kategori Produk Paling Tidak Diminati")
axes[1].set_xlabel("Jumlah Terjual")
axes[1].set_ylabel("Kategori Produk")

plt.tight_layout()
st.pyplot(fig)

# distribusi pelanggan berdasarkan state
st.subheader("🌍 Distribusi Pelanggan Berdasarkan State")
state_counts = filtered_df["customer_state"].value_counts()
st.bar_chart(state_counts)

# frekuensi transaksi pelanggan
st.subheader("📦 Frekuensi Transaksi Pelanggan")
customer_frequency = df["customer_id"].value_counts()
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(customer_frequency, bins=30, kde=True, color="purple", ax=ax)
ax.set_xlabel("Jumlah Transaksi")
ax.set_ylabel("Jumlah Pelanggan")
ax.set_title("Distribusi Frekuensi Transaksi Pelanggan")
st.pyplot(fig)

# metode pembayaran paling banyak digunakan
st.subheader("💳 Metode Pembayaran Favorit")
payment_counts = filtered_df["payment_type"].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=payment_counts.index, y=payment_counts.values, palette="coolwarm", ax=ax)
ax.set_xlabel("Metode Pembayaran")
ax.set_ylabel("Jumlah Transaksi")
ax.set_title("Metode Pembayaran Paling Sering Digunakan")
st.pyplot(fig)

# tren ulasan dan rating pelanggan
st.header("⭐ Distribusi Rating Pelanggan")
rating_counts = df["review_score"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=rating_counts.index, y=rating_counts.values, palette="magma", ax=ax)
ax.set_xlabel("Rating")
ax.set_ylabel("Jumlah Ulasan")
ax.set_title("Distribusi Rating Pelanggan")
st.pyplot(fig)

# hubungan antara jumlah transaksi dan total pembayaran pelanggan
customer_transactions = filtered_df["customer_id"].value_counts().reset_index()
customer_transactions.columns = ["customer_id", "total_transactions"]

customer_spending = filtered_df.groupby("customer_id")["payment_value"].sum().reset_index()
customer_analysis = customer_transactions.merge(customer_spending, on="customer_id", how="left").fillna(0)

st.subheader("📌 Hubungan Jumlah Transaksi dan Total Pembayaran")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=customer_analysis, 
    x="total_transactions", 
    y="payment_value", 
    alpha=0.5, 
    color="royalblue",
    ax=ax
)
ax.set_xlabel("Jumlah Transaksi")
ax.set_ylabel("Total Pembayaran (IDR)")
ax.set_title("Hubungan Jumlah Transaksi dan Total Pembayaran")
ax.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)

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