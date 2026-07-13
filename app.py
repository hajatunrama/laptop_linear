import time
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Laptop Price Prediction", page_icon="💻", layout="wide")

# =====================================================
# Theme state (Dark / Light toggle)
# =====================================================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

is_dark = st.session_state.theme == "dark"

# Palet warna per tema
if is_dark:
    bg_grad = "radial-gradient(circle at top left, #12151c 0%, #0b0d12 60%)"
    text_main = "#e5e7eb"
    text_sub = "#9ca3af"
    card_bg = "rgba(255,255,255,0.03)"
    card_border = "rgba(255,255,255,0.07)"
    input_bg = "#161a23"
    input_border = "rgba(255,255,255,0.08)"
    label_color = "#b5b9c4"
    footer_color = "#6b7280"
else:
    bg_grad = "radial-gradient(circle at top left, #f8fafc 0%, #eef1f6 60%)"
    text_main = "#1f2937"
    text_sub = "#4b5563"
    card_bg = "rgba(255,255,255,0.75)"
    card_border = "rgba(0,0,0,0.08)"
    input_bg = "#ffffff"
    input_border = "rgba(0,0,0,0.12)"
    label_color = "#374151"
    footer_color = "#6b7280"

# =====================================================
# Custom CSS — mempercantik tampilan tanpa ubah logic
# =====================================================
st.markdown(f"""
<style>
    /* ---------- Global ---------- */
    .stApp {{
        background: {bg_grad};
    }}
    html, body, [class*="css"] {{
        font-family: 'Segoe UI', 'Inter', sans-serif;
    }}
    .block-container {{
        max-width: 1200px;
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }}

    /* ---------- Header ---------- */
    .app-header {{
        text-align: center;
        padding: 1.6rem 1rem 1.2rem 1rem;
        margin-bottom: 1.5rem;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(236,72,153,0.10));
        border: 1px solid {card_border};
    }}
    .app-header h1 {{
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        background: linear-gradient(90deg, #818cf8, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .app-header p {{
        color: {text_sub};
        font-size: 0.95rem;
        margin: 0;
    }}

    /* ---------- Section cards ---------- */
    .section-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 1.3rem 1.4rem 0.6rem 1.4rem;
        margin-bottom: 1.3rem;
    }}
    .section-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {text_main};
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    .brand-icon-tag {{
        display: inline-block;
        font-size: 0.8rem;
        color: {text_sub};
        background: {input_bg};
        border: 1px solid {input_border};
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        margin-top: 0.4rem;
    }}

    /* ---------- Inputs ---------- */
    div[data-baseweb="select"] > div, .stNumberInput input {{
        background-color: {input_bg} !important;
        border-radius: 10px !important;
        border: 1px solid {input_border} !important;
        color: {text_main} !important;
    }}
    label {{
        color: {label_color} !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }}

    /* ---------- Slider ---------- */
    .stSlider [data-baseweb="slider"] {{
        margin-top: 0.4rem;
    }}

    /* ---------- Predict button ---------- */
    div.stButton > button[kind="primary"] {{
        width: 100%;
        background: linear-gradient(90deg, #6366f1, #ec4899);
        color: white;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 0.7rem 0;
        border-radius: 12px;
        border: none;
        box-shadow: 0 6px 20px rgba(99,102,241,0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    div.stButton > button[kind="primary"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgba(236,72,153,0.4);
        color: white;
    }}

    /* ---------- Theme toggle button ---------- */
    div.stButton > button[kind="secondary"] {{
        border-radius: 999px;
        border: 1px solid {input_border};
        background: {input_bg};
        color: {text_main};
        font-size: 0.85rem;
        padding: 0.3rem 0.9rem;
    }}

    /* ---------- Result box ---------- */
    .result-box {{
        text-align: center;
        padding: 1.5rem;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(16,185,129,0.18), rgba(16,185,129,0.06));
        border: 1px solid rgba(16,185,129,0.35);
        margin-top: 1rem;
    }}
    .result-box h2 {{
        color: #34d399;
        font-size: 1.8rem;
        margin: 0;
    }}
    .result-box p {{
        color: {text_sub};
        margin: 0.2rem 0 0 0;
        font-size: 0.85rem;
    }}

    /* ---------- Footer ---------- */
    .app-footer {{
        text-align: center;
        color: {footer_color};
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid {card_border};
    }}
</style>
""", unsafe_allow_html=True)

# =====================================================
# Brand icon mapping (representasi visual, bukan logo resmi)
# =====================================================
BRAND_ICONS = {
    "Acer": "🟢", "Lenovo": "🔴", "HP": "🔵", "Asus": "⚫",
    "Dell": "🔷", "MSI": "🔺", "Apple": "🍎",
}
CPU_ICONS = {"AMD": "🟠", "Apple": "🍎", "Intel": "🔷"}
GPU_ICONS = {"Intel": "🔷", "AMD": "🟠", "NVIDIA": "🟢"}

# =====================================================
# Theme toggle di pojok kanan atas
# =====================================================
top_l, top_r = st.columns([5, 1])
with top_r:
    st.button(
        "☀️ Light" if is_dark else "🌙 Dark",
        on_click=toggle_theme,
        key="theme_toggle_btn",
        type="secondary",
    )

# =====================================================
# Load model (pipeline sudah termasuk preprocessing)
# =====================================================
@st.cache_resource
def load_model():
    return joblib.load("LaptopPricePrediction.pkl")

model = load_model()

# =====================================================
# Header
# =====================================================
st.markdown("""
<div class="app-header">
    <h1>💻 Laptop Price Prediction</h1>
    <p>Masukkan spesifikasi laptop untuk memprediksi harga (USD)</p>
</div>
""", unsafe_allow_html=True)

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

# =====================================================
# Section 1-3: Spesifikasi Umum, Hardware, Performance Score
# (disusun 3 kolom sejajar agar memanfaatkan layout wide)
# =====================================================
sec1, sec2, sec3 = st.columns(3)

with sec1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧾 Spesifikasi Umum</div>', unsafe_allow_html=True)
    country = st.selectbox("Country", countries)
    brand = st.selectbox("Laptop Brand", brands)
    st.markdown(f'<span class="brand-icon-tag">{BRAND_ICONS.get(brand, "💻")} {brand}</span>', unsafe_allow_html=True)
    model_name = st.selectbox("Laptop Model", models_)
    cpu_brand = st.selectbox("CPU Brand", cpu_brands)
    st.markdown(f'<span class="brand-icon-tag">{CPU_ICONS.get(cpu_brand, "🧠")} {cpu_brand} CPU</span>', unsafe_allow_html=True)
    gpu_brand = st.selectbox("GPU Brand", gpu_brands)
    st.markdown(f'<span class="brand-icon-tag">{GPU_ICONS.get(gpu_brand, "🎮")} {gpu_brand} GPU</span>', unsafe_allow_html=True)
    gpu_model = st.selectbox("GPU Model", gpu_models)
    usage = st.selectbox("Usage Type", usage_types)
    st.markdown('</div>', unsafe_allow_html=True)

with sec2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ Spesifikasi Hardware</div>', unsafe_allow_html=True)
    ram = st.number_input("RAM (GB)", min_value=2, max_value=128, value=16, step=2)
    storage = st.number_input("Storage (GB)", min_value=64, max_value=8000, value=512, step=64)
    cores = st.number_input("CPU Cores", min_value=2, max_value=64, value=8)
    threads = st.number_input("CPU Threads", min_value=2, max_value=128, value=16)
    base_clock = st.number_input("Base Clock (GHz)", min_value=0.5, max_value=6.0, value=2.5, step=0.1)
    boost_clock = st.number_input("Boost Clock (GHz)", min_value=0.5, max_value=6.5, value=4.0, step=0.1)
    tdp = st.number_input("TDP (Watt)", min_value=5, max_value=250, value=65)
    st.markdown('</div>', unsafe_allow_html=True)

with sec3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Performance Score</div>', unsafe_allow_html=True)
    cpu_perf = st.slider("CPU Performance", min_value=0, max_value=200, value=80)
    gpu_perf = st.slider("GPU Performance", min_value=0, max_value=200, value=80)
    total_perf = cpu_perf + gpu_perf
    st.caption(f"Total Performance (otomatis dihitung) = **{total_perf}**")
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# Predict button + hasil
# =====================================================
predict_clicked = st.button("🔮 Predict Price", type="primary")

if predict_clicked:
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
    with st.spinner("🔄 Menghitung estimasi harga..."):
        time.sleep(0.9)  # jeda kecil biar animasi terasa natural
        prediction = model.predict(input_df)[0]

    progress_bar = st.progress(0)
    for pct in range(0, 101, 20):
        progress_bar.progress(pct)
        time.sleep(0.05)
    progress_bar.empty()

    st.markdown(f"""
    <div class="result-box">
        <p>Estimasi Harga Laptop</p>
        <h2>${prediction:,.2f} USD</h2>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# Footer
# =====================================================
st.markdown("""
<div class="app-footer">
    Model: Linear Regression Pipeline (OneHotEncoder + LinearRegression) — Final Project ML, AMIKOM Yogyakarta.
</div>
""", unsafe_allow_html=True)
