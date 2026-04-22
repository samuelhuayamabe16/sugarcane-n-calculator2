import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Sugarcane N Rate Calculator",
    page_icon="🎋",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #e8f0ec; }
#MainMenu, footer, header { visibility: hidden; }

.sc-header {
    padding: 2rem 0 1.4rem 0;
    border-bottom: 1px solid #d0d8d0;
    margin-bottom: 2rem;
}
.sc-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #ffffff;
    background: #1a5c50;
    padding: 4px 10px;
    border-radius: 2px;
    margin-bottom: 8px;
    display: inline-block;
}
.sc-header h1 {
    font-family: 'DM Mono', monospace;
    font-size: 1.35rem;
    font-weight: 500;
    color: #0e2420;
    margin: 0 0 4px 0;
    letter-spacing: -0.02em;
}
.sc-header p {
    font-size: 0.8rem;
    color: #7a9490;
    margin: 0;
    font-weight: 300;
}

.sc-inputs-box {
    background: #ffffff;
    border: 1px solid #c8d8d0;
    border-radius: 4px;
    padding: 1.6rem 1.5rem 1.4rem 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.sc-inputs-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #9aada8;
    font-weight: 500;
    padding-bottom: 10px;
    border-bottom: 1px solid #eef2ee;
    margin-bottom: 1rem;
}
/* Force number inputs to have visible labels and light background */
.stNumberInput > label {
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    color: #2a4a40 !important;
    letter-spacing: 0.02em !important;
    margin-bottom: 4px !important;
}
.stNumberInput input {
    background-color: #f4f8f6 !important;
    border: 1px solid #c0d4cc !important;
    color: #0e2420 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1rem !important;
    border-radius: 3px !important;
}
.stNumberInput input:focus {
    border-color: #1a5c50 !important;
    box-shadow: 0 0 0 2px rgba(26,92,80,0.12) !important;
}

.sc-section {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #9aada8;
    font-weight: 500;
    padding-bottom: 8px;
    border-bottom: 1px solid #dde4dc;
    margin-bottom: 14px;
}

.sc-card {
    background: #ffffff;
    border: 1px solid #dde4dc;
    border-radius: 3px;
    padding: 1rem 1.2rem 0.9rem 1.2rem;
    margin-bottom: 10px;
}
.sc-card-label {
    font-size: 0.64rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #9aada8;
    font-weight: 500;
    margin-bottom: 5px;
}
.sc-card-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.7rem;
    font-weight: 500;
    color: #0e2420;
    line-height: 1;
}
.sc-card-unit {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #9aada8;
    margin-left: 5px;
}
.sc-card-sub { font-size: 0.7rem; color: #9aada8; margin-top: 5px; }

.sc-bar-track {
    background: #eef2ee;
    border-radius: 1px;
    height: 4px;
    margin: 8px 0 3px 0;
    overflow: hidden;
}
.sc-bar-fill {
    height: 100%;
    border-radius: 1px;
    background: linear-gradient(90deg, #7ac4b8, #1a5c50);
}
.sc-bar-ticks {
    display: flex;
    justify-content: space-between;
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    color: #b0bdb8;
}

.sc-rec {
    background: #0e2420;
    border-radius: 3px;
    padding: 1.8rem 1.5rem;
    text-align: center;
}
.sc-rec-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #3a7a6e;
    margin-bottom: 10px;
}
.sc-rec-value {
    font-family: 'DM Mono', monospace;
    font-size: 3.4rem;
    font-weight: 500;
    color: #7addd0;
    line-height: 1;
}
.sc-rec-unit { font-family: 'DM Mono', monospace; font-size: 0.8rem; color: #3a7a6e; margin-top: 6px; }
.sc-rec-note {
    font-size: 0.68rem; color: #3a7a6e; margin-top: 14px;
    line-height: 1.6; text-align: left;
    border-top: 1px solid #1e3e38; padding-top: 12px;
}

.sc-ri-card {
    background: #ffffff;
    border: 1px solid #dde4dc;
    border-radius: 3px;
    padding: 1rem 1.2rem;
    margin-bottom: 10px;
}
.sc-ri-bar-track {
    background: #eef2ee; border-radius: 1px;
    height: 6px; margin: 10px 0 4px 0; overflow: hidden;
}
.sc-ri-bar-fill { height: 100%; border-radius: 1px; }

.sc-interp {
    border-radius: 2px; padding: 9px 13px;
    font-size: 0.78rem; margin-top: 10px;
    border-left: 2px solid; line-height: 1.5;
}
.sc-interp-low  { background:#f0f9f6; border-color:#2a8a78; color:#0e3830; }
.sc-interp-mod  { background:#fdf8ee; border-color:#c49a28; color:#5a4200; }
.sc-interp-high { background:#fdf2f2; border-color:#b84848; color:#5a1818; }

.sc-formula {
    background: #f2f6f4; border: 1px solid #dde4dc;
    border-radius: 3px; padding: 0.9rem 1.1rem;
    font-family: 'DM Mono', monospace; font-size: 0.72rem;
    color: #4a6460; line-height: 2; margin-top: 12px;
}
.sc-formula strong { color: #0e2420; }

.sc-footer {
    margin-top: 2.5rem; padding-top: 1rem;
    border-top: 1px solid #dde4dc;
    display: flex; justify-content: space-between;
    font-size: 0.66rem; color: #aabab6;
    font-family: 'DM Mono', monospace;
}
</style>
""", unsafe_allow_html=True)


# ── Core model ────────────────────────────────────────────────────────────────
def sugarcane_n_recommendation(ndvi_fp, ndvi_nrs, max_yield, pct_n, nue):
    yp0 = min(12.07 * np.exp(1.47 * ndvi_fp), max_yield)
    gnup_yp0 = yp0 * (pct_n / 100) * 2000
    ri = 1.94 * (ndvi_nrs / ndvi_fp) - 0.91 if ndvi_fp > 0 else 0
    ypn = min(yp0 * ri, max_yield)
    gnup_ypn = ypn * (pct_n / 100) * 2000
    fnr = float(np.clip((gnup_ypn - gnup_yp0) / nue, 40, 180))
    return yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sc-header">
    <div class="sc-badge">LSU AgCenter · Sugarcane Research</div>
    <h1>Sugarcane N Rate Calculator</h1>
    <p>Sensor-based · NDVI response index algorithm · Tubana, Johnson & Viator</p>
</div>
""", unsafe_allow_html=True)


# ── Inputs — all on main page, no sidebar ─────────────────────────────────────
st.markdown('<div class="sc-inputs-box"><div class="sc-inputs-title">Input Parameters</div>', unsafe_allow_html=True)

col_a, col_b, col_c, col_d, col_e = st.columns(5)

with col_a:
    ndvi_nrs = st.number_input(
        "NDVI — N Rich Strip",
        min_value=0.01, max_value=1.0,
        value=0.87, step=0.01, format="%.2f"
    )
with col_b:
    ndvi_fp = st.number_input(
        "NDVI — Farmer's Practice",
        min_value=0.01, max_value=1.0,
        value=0.75, step=0.01, format="%.2f"
    )
with col_c:
    max_yield = st.number_input(
        "Max Yield (ton/ac)",
        value=80, min_value=20, max_value=200
    )
with col_d:
    pct_n = st.number_input(
        "Stalk N Content (%)",
        value=0.30, min_value=0.10, max_value=1.0,
        step=0.01, format="%.2f"
    )
with col_e:
    nue = st.number_input(
        "N Use Efficiency",
        value=0.70, min_value=0.10, max_value=1.0,
        step=0.05, format="%.2f"
    )

st.markdown('</div>', unsafe_allow_html=True)


# ── Run model ─────────────────────────────────────────────────────────────────
yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr = sugarcane_n_recommendation(
    ndvi_fp, ndvi_nrs, max_yield, pct_n, nue
)


# ── NDVI Overview ─────────────────────────────────────────────────────────────
st.markdown('<div class="sc-section">NDVI Overview</div>', unsafe_allow_html=True)

ov1, ov2, ov3 = st.columns(3)

with ov1:
    fill = int((ndvi_nrs - 0.01) / 0.99 * 100)
    st.markdown(f"""
    <div class="sc-card">
        <div class="sc-card-label">N Rich Strip (NRS)</div>
        <div class="sc-card-value">{ndvi_nrs:.2f}</div>
        <div class="sc-bar-track"><div class="sc-bar-fill" style="width:{fill}%"></div></div>
        <div class="sc-bar-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div>
    </div>""", unsafe_allow_html=True)

with ov2:
    fill = int((ndvi_fp - 0.01) / 0.99 * 100)
    st.markdown(f"""
    <div class="sc-card">
        <div class="sc-card-label">Farmer's Practice (FP)</div>
        <div class="sc-card-value">{ndvi_fp:.2f}</div>
        <div class="sc-bar-track"><div class="sc-bar-fill" style="width:{fill}%"></div></div>
        <div class="sc-bar-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div>
    </div>""", unsafe_allow_html=True)

with ov3:
    delta = ndvi_nrs - ndvi_fp
    direction = "above" if delta >= 0 else "below"
    dcolor = "#b84848" if abs(delta) > 0.20 else "#c49a28" if abs(delta) > 0.10 else "#2a8a78"
    st.markdown(f"""
    <div class="sc-card">
        <div class="sc-card-label">NRS − FP Differential</div>
        <div class="sc-card-value" style="color:{dcolor}">{delta:+.2f}</div>
        <div class="sc-card-sub">NRS is {abs(delta):.2f} units {direction} FP</div>
    </div>""", unsafe_allow_html=True)


# ── Results ───────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="sc-section">Model Results</div>', unsafe_allow_html=True)

left, right = st.columns([3, 2], gap="large")

with left:
    r1, r2 = st.columns(2)
    r3, r4 = st.columns(2)

    with r1:
        st.markdown(f"""
        <div class="sc-card">
            <div class="sc-card-label">Yield Potential — No N (YP0)</div>
            <div class="sc-card-value">{yp0:.2f}<span class="sc-card-unit">ton/ac</span></div>
        </div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
        <div class="sc-card">
            <div class="sc-card-label">Yield Potential — With N (YPN)</div>
            <div class="sc-card-value">{ypn:.2f}<span class="sc-card-unit">ton/ac</span></div>
        </div>""", unsafe_allow_html=True)
    with r3:
        st.markdown(f"""
        <div class="sc-card">
            <div class="sc-card-label">Stalk N Uptake — No N (GNUP₀)</div>
            <div class="sc-card-value">{gnup_yp0:.1f}<span class="sc-card-unit">lb N/ac</span></div>
        </div>""", unsafe_allow_html=True)
    with r4:
        st.markdown(f"""
        <div class="sc-card">
            <div class="sc-card-label">Stalk N Uptake — With N (GNUPₙ)</div>
            <div class="sc-card-value">{gnup_ypn:.1f}<span class="sc-card-unit">lb N/ac</span></div>
        </div>""", unsafe_allow_html=True)

    ri_pct = int(min(max((ri / 2.0) * 100, 0), 100))
    ri_color = "#b84848" if ri > 1.2 else "#c49a28" if ri > 1.0 else "#2a8a78"
    st.markdown(f"""
    <div class="sc-ri-card">
        <div class="sc-card-label">Response Index (RI) &nbsp;·&nbsp;
            <span style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#b0bdb8">
                (NDVI_NRS / NDVI_FP) × 1.94 − 0.91
            </span>
        </div>
        <div class="sc-card-value" style="color:{ri_color}">{ri:.4f}</div>
        <div class="sc-ri-bar-track">
            <div class="sc-ri-bar-fill" style="width:{ri_pct}%;background:{ri_color};opacity:0.6"></div>
        </div>
        <div class="sc-bar-ticks"><span>0.0</span><span>1.0</span><span>2.0</span></div>
    </div>""", unsafe_allow_html=True)

    if ri > 1.2:
        interp_class, interp_msg = "sc-interp-high", f"RI of {ri:.3f} indicates a strong crop response to nitrogen. Application is recommended to avoid yield loss."
    elif ri > 1.0:
        interp_class, interp_msg = "sc-interp-mod", f"RI of {ri:.3f} suggests a moderate response. Evaluate nitrogen application against the economic threshold."
    else:
        interp_class, interp_msg = "sc-interp-low", f"RI of {ri:.3f} indicates low expected response. Additional nitrogen may not be economically justified."

    st.markdown(f'<div class="sc-interp {interp_class}">{interp_msg}</div>', unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="sc-rec">
        <div class="sc-rec-label">Fertilizer N Requirement</div>
        <div class="sc-rec-value">{fnr:.0f}</div>
        <div class="sc-rec-unit">lbs N / acre</div>
        <div class="sc-rec-note">
            Bounded 40–180 lb N/ac per LSU AgCenter guidelines.<br>
            Adjust NUE for fertilizer source and timing.
        </div>
    </div>
    <div class="sc-formula">
        <strong>YP0</strong> = 12.07 × e^(NDVI_FP × 1.47)<br>
        <strong>RI</strong> &nbsp;= (NRS / FP) × 1.94 − 0.91<br>
        <strong>YPN</strong> = YP0 × RI<br>
        <strong>GNUP</strong> = Yield × %N × 2000<br>
        <strong>FNR</strong> &nbsp;= (GNUPₙ − GNUP₀) / NUE
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sc-footer">
    <span>LSU AgCenter · Sensor-Based Sugarcane N Algorithm · Tubana, Johnson & Viator</span>
    <span>For research use only · Not a substitute for professional agronomic advice</span>
</div>
""", unsafe_allow_html=True)
