import streamlit as st
import numpy as np

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sugarcane N Rate Calculator",
    page_icon="🎋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
# Only style non-interactive elements — sidebar inputs are left as Streamlit defaults
# so they always render and function correctly regardless of browser/version
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Main area background ── */
.stApp {
    background-color: #f7f8f6;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Page header ── */
.sc-header {
    padding: 2.2rem 0 1.6rem 0;
    border-bottom: 1px solid #d0d8d0;
    margin-bottom: 2rem;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
}
.sc-header-left h1 {
    font-family: 'DM Mono', monospace;
    font-size: 1.35rem;
    font-weight: 500;
    color: #0e2420;
    margin: 0 0 4px 0;
    letter-spacing: -0.02em;
}
.sc-header-left p {
    font-size: 0.8rem;
    color: #7a9490;
    margin: 0;
    font-weight: 300;
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
.sc-header-right {
    text-align: right;
    font-size: 0.72rem;
    color: #9aada8;
    font-family: 'DM Mono', monospace;
    line-height: 1.8;
}

/* ── Section labels ── */
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

/* ── Data cards ── */
.sc-card {
    background: #ffffff;
    border: 1px solid #dde4dc;
    border-radius: 3px;
    padding: 1rem 1.2rem 0.9rem 1.2rem;
    margin-bottom: 10px;
    position: relative;
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
.sc-card-sub {
    font-size: 0.7rem;
    color: #9aada8;
    margin-top: 5px;
}

/* ── NDVI bar ── */
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

/* ── N recommendation panel ── */
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
.sc-rec-unit {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: #3a7a6e;
    margin-top: 6px;
}
.sc-rec-note {
    font-size: 0.68rem;
    color: #3a7a6e;
    margin-top: 14px;
    line-height: 1.6;
    text-align: left;
    border-top: 1px solid #1e3e38;
    padding-top: 12px;
}

/* ── RI indicator ── */
.sc-ri-card {
    background: #ffffff;
    border: 1px solid #dde4dc;
    border-radius: 3px;
    padding: 1rem 1.2rem;
    margin-bottom: 10px;
}
.sc-ri-bar-track {
    background: #eef2ee;
    border-radius: 1px;
    height: 6px;
    margin: 10px 0 4px 0;
    overflow: hidden;
    position: relative;
}
.sc-ri-bar-fill {
    height: 100%;
    border-radius: 1px;
    transition: width 0.4s;
}

/* ── Interpretation tag ── */
.sc-interp {
    border-radius: 2px;
    padding: 9px 13px;
    font-size: 0.78rem;
    margin-top: 10px;
    border-left: 2px solid;
    line-height: 1.5;
}
.sc-interp-low  { background:#f0f9f6; border-color:#2a8a78; color:#0e3830; }
.sc-interp-mod  { background:#fdf8ee; border-color:#c49a28; color:#5a4200; }
.sc-interp-high { background:#fdf2f2; border-color:#b84848; color:#5a1818; }

/* ── Formula box ── */
.sc-formula {
    background: #f2f6f4;
    border: 1px solid #dde4dc;
    border-radius: 3px;
    padding: 0.9rem 1.1rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #4a6460;
    line-height: 2;
    margin-top: 12px;
}
.sc-formula strong {
    color: #0e2420;
}

/* ── Placeholder ── */
.sc-placeholder {
    margin-top: 1.5rem;
    padding: 2rem;
    background: #ffffff;
    border: 1px dashed #c8d4cc;
    border-radius: 3px;
    text-align: center;
    color: #9aada8;
    font-size: 0.82rem;
}

/* ── Footer ── */
.sc-footer {
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid #dde4dc;
    display: flex;
    justify-content: space-between;
    font-size: 0.66rem;
    color: #aabab6;
    font-family: 'DM Mono', monospace;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar — plain Streamlit widgets, no CSS interference ───────────────────
with st.sidebar:
    st.markdown("### ⚙️ Parameters")
    st.markdown("**NDVI Inputs**")
    ndvi_nrs = st.number_input(
        "NDVI — N Rich Strip (NRS)",
        min_value=0.01, max_value=1.0,
        value=0.87, step=0.01, format="%.2f"
    )
    ndvi_fp = st.number_input(
        "NDVI — Farmer's Practice (FP)",
        min_value=0.01, max_value=1.0,
        value=0.75, step=0.01, format="%.2f"
    )
    st.markdown("---")
    st.markdown("**Crop & Field Settings**")
    max_yield = st.number_input(
        "Maximum Yield (ton/ac)",
        value=80, min_value=20, max_value=200
    )
    pct_n = st.number_input(
        "Stalk N Content (%)",
        value=0.30, min_value=0.10, max_value=1.0,
        step=0.01, format="%.2f",
        help="Default 0.30% — LSU AgCenter sugarcane stalk analysis"
    )
    nue = st.number_input(
        "N Use Efficiency (NUE)",
        value=0.70, min_value=0.10, max_value=1.0,
        step=0.05, format="%.2f",
        help="Typical range: 50–70% for sugarcane in Louisiana"
    )
    st.markdown("---")
    st.caption(
        "Set max yield to ~2× the 5-year field average. "
        "Algorithm: Tubana, Johnson & Viator — LSU AgCenter."
    )


# ── Core model ────────────────────────────────────────────────────────────────
def sugarcane_n_recommendation(ndvi_fp, ndvi_nrs, max_yield, pct_n, nue):
    # Step 1: Yield potential without N (exponential NDVI model)
    yp0 = min(12.07 * np.exp(1.47 * ndvi_fp), max_yield)

    # Step 2: Stalk N uptake without N — ton/ac × %N × 2000 → lb N/ac
    gnup_yp0 = yp0 * (pct_n / 100) * 2000

    # Step 3: Response Index
    ri = 1.94 * (ndvi_nrs / ndvi_fp) - 0.91 if ndvi_fp > 0 else 0

    # Step 4: Yield potential with N, capped at max yield
    ypn = min(yp0 * ri, max_yield)

    # Step 5: Stalk N uptake with N
    gnup_ypn = ypn * (pct_n / 100) * 2000

    # Step 6: Fertilizer N requirement, clamped to 40–180 lb N/ac
    fnr = float(np.clip((gnup_ypn - gnup_yp0) / nue, 40, 180))

    return yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr


# ── Run model ─────────────────────────────────────────────────────────────────
yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr = sugarcane_n_recommendation(
    ndvi_fp, ndvi_nrs, max_yield, pct_n, nue
)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="sc-header">
    <div class="sc-header-left">
        <div class="sc-badge">LSU AgCenter · Sugarcane Research</div>
        <h1>Sugarcane N Rate Calculator</h1>
        <p>Sensor-based · NDVI response index algorithm · Mid-season variable-rate application</p>
    </div>
    <div class="sc-header-right">
        NRS &nbsp;{ndvi_nrs:.2f} &nbsp;/&nbsp; FP &nbsp;{ndvi_fp:.2f}<br>
        Max yield &nbsp;{max_yield} ton/ac &nbsp;· &nbsp;NUE &nbsp;{nue:.0%}
    </div>
</div>
""", unsafe_allow_html=True)


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

    # RI card with visual bar
    ri_pct = int(min(max((ri / 2.0) * 100, 0), 100))
    ri_color = "#b84848" if ri > 1.2 else "#c49a28" if ri > 1.0 else "#2a8a78"
    ri_bg    = "#fdf2f2" if ri > 1.2 else "#fdf8ee" if ri > 1.0 else "#f0f9f6"
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

    # Interpretation
    if ri > 1.2:
        interp_class = "sc-interp-high"
        interp_msg = f"RI of {ri:.3f} indicates a strong crop response to nitrogen. Application is recommended to avoid yield loss."
    elif ri > 1.0:
        interp_class = "sc-interp-mod"
        interp_msg = f"RI of {ri:.3f} suggests a moderate response. Evaluate nitrogen application against the economic threshold."
    else:
        interp_class = "sc-interp-low"
        interp_msg = f"RI of {ri:.3f} indicates low expected response. Additional nitrogen may not be economically justified."

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