import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Rice N Rate Calculator",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #f0f4f8; }
#MainMenu, footer, header { visibility: hidden; }

/* Force number inputs to have visible labels and light background */
.stNumberInput > label {
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    color: #1a3a5c !important;
    letter-spacing: 0.02em !important;
    margin-bottom: 4px !important;
}
.stNumberInput input {
    background-color: #f0f5fa !important;
    border: 1px solid #b0c8e0 !important;
    color: #0e1e30 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1rem !important;
    border-radius: 3px !important;
}
.stNumberInput input:focus {
    border-color: #1a5c8a !important;
    box-shadow: 0 0 0 2px rgba(26,92,138,0.12) !important;
}

.rc-header {
    padding: 2rem 0 1.4rem 0;
    border-bottom: 1px solid #c0ccd8;
    margin-bottom: 2rem;
}
.rc-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #ffffff;
    background: #1a4a7a;
    padding: 4px 10px;
    border-radius: 2px;
    margin-bottom: 8px;
    display: inline-block;
}
.rc-header h1 {
    font-family: 'DM Mono', monospace;
    font-size: 1.35rem;
    font-weight: 500;
    color: #0e1e30;
    margin: 0 0 4px 0;
    letter-spacing: -0.02em;
}
.rc-header p {
    font-size: 0.8rem;
    color: #6a8aaa;
    margin: 0;
    font-weight: 300;
}

.rc-inputs-box {
    background: #ffffff;
    border: 1px solid #b0c8e0;
    border-radius: 4px;
    padding: 1.6rem 1.5rem 1.4rem 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.rc-inputs-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7a9aaa;
    font-weight: 500;
    padding-bottom: 10px;
    border-bottom: 1px solid #e0eaf2;
    margin-bottom: 1rem;
}

.rc-section {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7a9aaa;
    font-weight: 500;
    padding-bottom: 8px;
    border-bottom: 1px solid #ccd8e8;
    margin-bottom: 14px;
}

.rc-card {
    background: #ffffff;
    border: 1px solid #ccd8e8;
    border-radius: 3px;
    padding: 1rem 1.2rem 0.9rem 1.2rem;
    margin-bottom: 10px;
}
.rc-card-label {
    font-size: 0.64rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7a9aaa;
    font-weight: 500;
    margin-bottom: 5px;
}
.rc-card-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.7rem;
    font-weight: 500;
    color: #0e1e30;
    line-height: 1;
}
.rc-card-unit {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #7a9aaa;
    margin-left: 5px;
}
.rc-card-sub { font-size: 0.7rem; color: #7a9aaa; margin-top: 5px; }

.rc-bar-track {
    background: #e0eaf2;
    border-radius: 1px;
    height: 4px;
    margin: 8px 0 3px 0;
    overflow: hidden;
}
.rc-bar-fill {
    height: 100%;
    border-radius: 1px;
    background: linear-gradient(90deg, #7ab4d8, #1a4a7a);
}
.rc-bar-ticks {
    display: flex;
    justify-content: space-between;
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    color: #a0b8cc;
}

.rc-rec {
    background: #0e1e30;
    border-radius: 3px;
    padding: 1.8rem 1.5rem;
    text-align: center;
}
.rc-rec-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #3a6a9a;
    margin-bottom: 10px;
}
.rc-rec-value {
    font-family: 'DM Mono', monospace;
    font-size: 3.4rem;
    font-weight: 500;
    color: #7ac4f0;
    line-height: 1;
}
.rc-rec-unit { font-family: 'DM Mono', monospace; font-size: 0.8rem; color: #3a6a9a; margin-top: 6px; }
.rc-rec-note {
    font-size: 0.68rem; color: #3a6a9a; margin-top: 14px;
    line-height: 1.6; text-align: left;
    border-top: 1px solid #1e3e58; padding-top: 12px;
}

.rc-ri-card {
    background: #ffffff;
    border: 1px solid #ccd8e8;
    border-radius: 3px;
    padding: 1rem 1.2rem;
    margin-bottom: 10px;
}
.rc-ri-bar-track {
    background: #e0eaf2; border-radius: 1px;
    height: 6px; margin: 10px 0 4px 0; overflow: hidden;
}
.rc-ri-bar-fill { height: 100%; border-radius: 1px; }

.rc-interp {
    border-radius: 2px; padding: 9px 13px;
    font-size: 0.78rem; margin-top: 10px;
    border-left: 2px solid; line-height: 1.5;
}
.rc-interp-low  { background:#f0f6fc; border-color:#2a6a9a; color:#0e2038; }
.rc-interp-mod  { background:#fdf8ee; border-color:#c49a28; color:#5a4200; }
.rc-interp-high { background:#fdf2f2; border-color:#b84848; color:#5a1818; }

.rc-formula {
    background: #f0f5fa; border: 1px solid #ccd8e8;
    border-radius: 3px; padding: 0.9rem 1.1rem;
    font-family: 'DM Mono', monospace; font-size: 0.72rem;
    color: #3a5a7a; line-height: 2; margin-top: 12px;
}
.rc-formula strong { color: #0e1e30; }

.rc-footer {
    margin-top: 2.5rem; padding-top: 1rem;
    border-top: 1px solid #ccd8e8;
    display: flex; justify-content: space-between;
    font-size: 0.66rem; color: #8aaac0;
    font-family: 'DM Mono', monospace;
}
</style>
""", unsafe_allow_html=True)


# ── Core model ────────────────────────────────────────────────────────────────
def rice_n_recommendation(ndvi_fp, ndvi_nrs, max_yield, pct_n, nue):
    # Step 1: Yield potential without N — power function specific to rice
    yp0 = min(12088 * (ndvi_fp ** 0.72), max_yield)

    # Step 2: Grain N uptake without N — yield (bu/ac) × lbs/bu × %N / 100
    # Rice: 45 lbs per bushel, 1.2% grain N
    gnup_yp0 = yp0 * 45 * (pct_n / 100)

    # Step 3: Response Index — rice-specific RI formula from LSU AgCenter/MSU
    ri = ((ndvi_nrs / ndvi_fp) * 1.0077 + 0.19727) * 0.94 if ndvi_fp > 0 else 0

    # Step 4: Yield potential with N applied, capped at max yield
    ypn = min(yp0 * ri, max_yield)

    # Step 5: Grain N uptake with N applied
    gnup_ypn = ypn * 45 * (pct_n / 100)

    # Step 6: Fertilizer N requirement, clamped to agronomic bounds for rice
    fnr = float(np.clip((gnup_ypn - gnup_yp0) / nue, 0, 150))

    return yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rc-header">
    <div class="rc-badge">LSU AgCenter · MSU · Rice Research</div>
    <h1>Rice Midseason N Rate Calculator</h1>
    <p>Sensor-based · NDVI response index algorithm · Tubana, Harrell & Walker</p>
</div>
""", unsafe_allow_html=True)


# ── Inputs ────────────────────────────────────────────────────────────────────
st.markdown('<div class="rc-inputs-box"><div class="rc-inputs-title">Input Parameters</div>', unsafe_allow_html=True)

col_a, col_b, col_c, col_d, col_e = st.columns(5)

with col_a:
    ndvi_nrs = st.number_input(
        "NDVI — N Rich Strip",
        min_value=0.01, max_value=1.0,
        value=0.94, step=0.01, format="%.2f",
        help="NDVI from the well-fertilized reference strip"
    )
with col_b:
    ndvi_fp = st.number_input(
        "NDVI — Farmer's Practice",
        min_value=0.01, max_value=1.0,
        value=0.94, step=0.01, format="%.2f",
        help="NDVI from the target field (no midseason N applied)"
    )
with col_c:
    max_yield = st.number_input(
        "Max Yield (bu/ac)",
        value=320, min_value=50, max_value=600,
        help="Set to ~2× the 5-year average yield"
    )
with col_d:
    pct_n = st.number_input(
        "Grain N Content (%)",
        value=1.20, min_value=0.50, max_value=3.0,
        step=0.01, format="%.2f",
        help="Default 1.2% — rice grain N per LSU AgCenter"
    )
with col_e:
    nue = st.number_input(
        "N Use Efficiency",
        value=0.75, min_value=0.10, max_value=1.0,
        step=0.05, format="%.2f",
        help="Default 75% for midseason rice application"
    )

st.markdown('</div>', unsafe_allow_html=True)


# ── Run model ─────────────────────────────────────────────────────────────────
yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr = rice_n_recommendation(
    ndvi_fp, ndvi_nrs, max_yield, pct_n, nue
)


# ── NDVI Overview ─────────────────────────────────────────────────────────────
st.markdown('<div class="rc-section">NDVI Overview</div>', unsafe_allow_html=True)

ov1, ov2, ov3 = st.columns(3)

with ov1:
    fill = int((ndvi_nrs - 0.01) / 0.99 * 100)
    st.markdown(f"""
    <div class="rc-card">
        <div class="rc-card-label">N Rich Strip (NRS)</div>
        <div class="rc-card-value">{ndvi_nrs:.2f}</div>
        <div class="rc-bar-track"><div class="rc-bar-fill" style="width:{fill}%"></div></div>
        <div class="rc-bar-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div>
    </div>""", unsafe_allow_html=True)

with ov2:
    fill = int((ndvi_fp - 0.01) / 0.99 * 100)
    st.markdown(f"""
    <div class="rc-card">
        <div class="rc-card-label">Farmer's Practice (FP)</div>
        <div class="rc-card-value">{ndvi_fp:.2f}</div>
        <div class="rc-bar-track"><div class="rc-bar-fill" style="width:{fill}%"></div></div>
        <div class="rc-bar-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div>
    </div>""", unsafe_allow_html=True)

with ov3:
    delta = ndvi_nrs - ndvi_fp
    direction = "above" if delta >= 0 else "below"
    dcolor = "#b84848" if abs(delta) > 0.20 else "#c49a28" if abs(delta) > 0.10 else "#2a6a9a"
    st.markdown(f"""
    <div class="rc-card">
        <div class="rc-card-label">NRS − FP Differential</div>
        <div class="rc-card-value" style="color:{dcolor}">{delta:+.2f}</div>
        <div class="rc-card-sub">NRS is {abs(delta):.2f} units {direction} FP</div>
    </div>""", unsafe_allow_html=True)


# ── Results ───────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="rc-section">Model Results</div>', unsafe_allow_html=True)

left, right = st.columns([3, 2], gap="large")

with left:
    r1, r2 = st.columns(2)
    r3, r4 = st.columns(2)

    with r1:
        st.markdown(f"""
        <div class="rc-card">
            <div class="rc-card-label">Yield Potential — No N (YP0)</div>
            <div class="rc-card-value">{yp0:.1f}<span class="rc-card-unit">bu/ac</span></div>
        </div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
        <div class="rc-card">
            <div class="rc-card-label">Yield Potential — With N (YPN)</div>
            <div class="rc-card-value">{ypn:.1f}<span class="rc-card-unit">bu/ac</span></div>
        </div>""", unsafe_allow_html=True)
    with r3:
        st.markdown(f"""
        <div class="rc-card">
            <div class="rc-card-label">Grain N Uptake — No N (GNUP₀)</div>
            <div class="rc-card-value">{gnup_yp0:.1f}<span class="rc-card-unit">lb N/ac</span></div>
        </div>""", unsafe_allow_html=True)
    with r4:
        st.markdown(f"""
        <div class="rc-card">
            <div class="rc-card-label">Grain N Uptake — With N (GNUPₙ)</div>
            <div class="rc-card-value">{gnup_ypn:.1f}<span class="rc-card-unit">lb N/ac</span></div>
        </div>""", unsafe_allow_html=True)

    # RI card
    ri_pct = int(min(max((ri / 2.0) * 100, 0), 100))
    ri_color = "#b84848" if ri > 1.2 else "#c49a28" if ri > 1.0 else "#2a6a9a"
    st.markdown(f"""
    <div class="rc-ri-card">
        <div class="rc-card-label">Response Index (RI) &nbsp;·&nbsp;
            <span style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#a0b8cc">
                ((NRS / FP) × 1.0077 + 0.19727) × 0.94
            </span>
        </div>
        <div class="rc-card-value" style="color:{ri_color}">{ri:.4f}</div>
        <div class="rc-ri-bar-track">
            <div class="rc-ri-bar-fill" style="width:{ri_pct}%;background:{ri_color};opacity:0.6"></div>
        </div>
        <div class="rc-bar-ticks"><span>0.0</span><span>1.0</span><span>2.0</span></div>
    </div>""", unsafe_allow_html=True)

    if ri > 1.2:
        interp_class = "rc-interp-high"
        interp_msg = f"RI of {ri:.3f} indicates a strong crop response to nitrogen. Midseason application is recommended."
    elif ri > 1.0:
        interp_class = "rc-interp-mod"
        interp_msg = f"RI of {ri:.3f} suggests a moderate response. Evaluate application against economic threshold."
    else:
        interp_class = "rc-interp-low"
        interp_msg = f"RI of {ri:.3f} indicates low expected response. Midseason nitrogen may not be economically justified."

    st.markdown(f'<div class="rc-interp {interp_class}">{interp_msg}</div>', unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="rc-rec">
        <div class="rc-rec-label">Midseason N Requirement</div>
        <div class="rc-rec-value">{fnr:.0f}</div>
        <div class="rc-rec-unit">lbs N / acre</div>
        <div class="rc-rec-note">
            Bounded 0–150 lb N/ac per LSU AgCenter rice guidelines.<br>
            Adjust NUE for fertilizer source and flood conditions.
        </div>
    </div>
    <div class="rc-formula">
        <strong>YP0</strong> = 12088 × NDVI_FP^0.72<br>
        <strong>RI</strong> &nbsp;= ((NRS/FP) × 1.0077 + 0.19727) × 0.94<br>
        <strong>YPN</strong> = YP0 × RI<br>
        <strong>GNUP</strong> = Yield × 45 lbs/bu × %N<br>
        <strong>FNR</strong> &nbsp;= (GNUPₙ − GNUP₀) / NUE
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rc-footer">
    <span>LSU AgCenter · MSU · Sensor-Based Rice N Algorithm · Tubana, Harrell & Walker</span>
    <span>For research use only · Not a substitute for professional agronomic advice</span>
</div>
""", unsafe_allow_html=True)
