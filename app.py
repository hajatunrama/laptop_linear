import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Laptop Price Prediction", page_icon="💻", layout="centered")

# =====================================================
# Load model (pipeline sudah termasuk preprocessing)
# =====================================================
@st.cache_resource
def load_model():
    return joblib.load("LaptopPricePrediction.pkl")

model = load_model()

st.title("💻 Laptop Price Prediction")
st.write("Masukkan spesifikasi laptop untuk memprediksi harga (USD).")

# =====================================================
# NOTE PENTING:
# Pilihan di bawah HARUS sama persis dengan kategori
# yang ada saat training (lihat df[col].unique() di notebook).
# Kalau dataset kamu beda / berubah, update list ini juga.
# =====================================================
countries = ['Brazil', 'Germany', 'Canada', 'UK', 'UAE', 'India', 'Pakistan', 'China', 'USA', 'Japan']
brands = ['Acer', 'Lenovo', 'HP', 'Asus', 'Dell', 'MSI', 'Apple']
models_ = ['Pavilion', 'Inspiron', 'Stealth', 'ROG', 'MacBook', 'Nitro', 'ThinkPad']
cpu_brands = ['AMD', 'Apple', 'Intel']
gpu_brands = ['Intel', 'AMD', 'NVIDIA']
gpu_models = ['Iris Xe', 'RTX 3050', 'RX 6600', 'RTX 3080', 'RX 6700', 'RTX 3060', 'RTX 3070']
usage_types = ['Professional', 'Basic', 'Student', 'High-End Gaming']

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox("Country", countries)
    brand = st.selectbox("Laptop Brand", brands)
    model_name = st.selectbox("Laptop Model", models_)
    cpu_brand = st.selectbox("CPU Brand", cpu_brands)
    gpu_brand = st.selectbox("GPU Brand", gpu_brands)
    gpu_model = st.selectbox("GPU Model", gpu_models)
    usage = st.selectbox("Usage Type", usage_types)

with col2:
    ram = st.number_input("RAM (GB)", min_value=2, max_value=128, value=16, step=2)
    storage = st.number_input("Storage (GB)", min_value=64, max_value=8000, value=512, step=64)
    cores = st.number_input("CPU Cores", min_value=2, max_value=64, value=8)
    threads = st.number_input("CPU Threads", min_value=2, max_value=128, value=16)
    base_clock = st.number_input("Base Clock (GHz)", min_value=0.5, max_value=6.0, value=2.5, step=0.1)
    boost_clock = st.number_input("Boost Clock (GHz)", min_value=0.5, max_value=6.5, value=4.0, step=0.1)
    tdp = st.number_input("TDP (Watt)", min_value=5, max_value=250, value=65)

st.subheader("Performance Score")
cpu_perf = st.slider("CPU Performance", min_value=0, max_value=200, value=80)
gpu_perf = st.slider("GPU Performance", min_value=0, max_value=200, value=80)
total_perf = cpu_perf + gpu_perf
st.caption(f"Total Performance (otomatis dihitung) = {total_perf}")

if st.button("🔮 Predict Price", type="primary"):
    input_df = pd.DataFrame([{
        "Country": country,
        "Laptop_Brand": brand,
        "Laptop_Model": model_name,
        "CPU_Brand": cpu_brand,
        "GPU_Brand": gpu_brand,
        "GPU_Model": gpu_model,
        "RAM_GB": ram,
        "Storage_GB": storage,
        "Cores": cores,
        "Threads": threads,
        "Base_Clock": base_clock,
        "Boost_Clock": boost_clock,
        "TDP": tdp,
        "CPU_Performance": cpu_perf,
        "GPU_Performance": gpu_perf,
        "Total_Performance": total_perf,
        "Usage_Type": usage,
    }])

    prediction = model.predict(input_df)[0]
    st.success(f"### Estimasi Harga: **${prediction:,.2f} USD**")

st.divider()
st.caption("Model: Linear Regression Pipeline (OneHotEncoder + LinearRegression) — Final Project ML, AMIKOM Yogyakarta.")
