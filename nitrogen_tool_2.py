import streamlit as st
import numpy as np

st.set_page_config(
    page_title="LSU AgCenter · N Rate Calculator",
    page_icon="🌾",
    layout="wide"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=DM+Mono:wght@400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background-color: #f8f5f0;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── Number inputs — always visible regardless of theme ── */
.stNumberInput > label {
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    color: #3a3228 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}
.stNumberInput input {
    background-color: #ffffff !important;
    border: 1.5px solid #d8d0c4 !important;
    color: #1a1410 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1.05rem !important;
    border-radius: 4px !important;
    padding: 8px 12px !important;
}
.stNumberInput input:focus {
    border-color: #8a6a2a !important;
    box-shadow: 0 0 0 3px rgba(138,106,42,0.1) !important;
    outline: none !important;
}

/* ── Page header ── */
.app-header-inner {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 2.4rem 0 1.6rem 0;
    border-bottom: 1px solid #d8d0c4;
    margin-bottom: 1.6rem;
}
.app-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 600;
    color: #1a1410;
    margin: 0 0 4px 0;
    letter-spacing: -0.01em;
    line-height: 1.2;
}
.app-subtitle {
    font-size: 0.78rem;
    color: #8a8078;
    font-weight: 300;
    font-style: italic;
    margin: 0;
}
.app-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #8a8078;
    border: 1px solid #c8c0b4;
    padding: 5px 10px;
    border-radius: 2px;
    white-space: nowrap;
    margin-top: 6px;
}

/* ── Input panel ── */
.input-panel {
    border-radius: 6px;
    padding: 1.6rem 1.8rem 1.4rem 1.8rem;
    margin-bottom: 2rem;
    border: 1px solid;
}
.input-panel-sc {
    background: linear-gradient(135deg, #fffbf4 0%, #fff8ec 100%);
    border-color: #e8d4a8;
}
.input-panel-rc {
    background: linear-gradient(135deg, #f4f8ff 0%, #edf4fc 100%);
    border-color: #b8d0e8;
}
.input-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-weight: 500;
    padding-bottom: 12px;
    margin-bottom: 16px;
    border-bottom: 1px solid;
}
.input-panel-title-sc { color: #a87830; border-bottom-color: #e8d4a8; }
.input-panel-title-rc { color: #2a6a9a; border-bottom-color: #b8d0e8; }

/* ── Section label ── */
.sec-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-weight: 500;
    color: #a09080;
    padding-bottom: 8px;
    border-bottom: 1px solid #e0d8cc;
    margin-bottom: 14px;
}

/* ── Data cards ── */
.d-card {
    background: #ffffff;
    border: 1px solid #e0d8cc;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin-bottom: 10px;
}
.d-card-label {
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #a09080;
    font-weight: 500;
    margin-bottom: 6px;
}
.d-card-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.65rem;
    font-weight: 500;
    color: #1a1410;
    line-height: 1;
}
.d-card-unit {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #a09080;
    margin-left: 5px;
}
.d-card-sub { font-size: 0.68rem; color: #a09080; margin-top: 5px; }

/* ── NDVI bar ── */
.ndvi-track {
    height: 4px;
    border-radius: 1px;
    margin: 9px 0 4px 0;
    overflow: hidden;
    background: #ede8e0;
}
.ndvi-fill-sc { height:100%; border-radius:1px; background: linear-gradient(90deg, #e8c878, #a87830); }
.ndvi-fill-rc { height:100%; border-radius:1px; background: linear-gradient(90deg, #7ab4d8, #1a4a7a); }
.ndvi-ticks { display:flex; justify-content:space-between; font-family:'DM Mono',monospace; font-size:0.56rem; color:#c0b8a8; }

/* ── RI card ── */
.ri-card {
    background: #ffffff;
    border: 1px solid #e0d8cc;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin-bottom: 10px;
}
.ri-track { height:5px; border-radius:1px; margin:10px 0 4px 0; overflow:hidden; background:#ede8e0; }
.ri-fill { height:100%; border-radius:1px; opacity:0.7; }

/* ── Interpretation bar ── */
.interp {
    border-radius: 3px;
    padding: 10px 14px;
    font-size: 0.77rem;
    margin-top: 10px;
    border-left: 2px solid;
    line-height: 1.55;
}
.interp-low  { background:#f4fcf8; border-color:#3a8a60; color:#1a3a28; }
.interp-mod  { background:#fdf8ee; border-color:#c49a28; color:#5a4200; }
.interp-high { background:#fdf2f0; border-color:#b84848; color:#5a1818; }

/* ── Recommendation boxes ── */
.rec-box-sc {
    background: linear-gradient(160deg, #2a1e0e 0%, #1a1208 100%);
    border-radius: 5px;
    padding: 2rem 1.6rem;
    text-align: center;
    border: 1px solid #4a3618;
}
.rec-box-rc {
    background: linear-gradient(160deg, #0e1e2e 0%, #081420 100%);
    border-radius: 5px;
    padding: 2rem 1.6rem;
    text-align: center;
    border: 1px solid #1a3a5a;
}
.rec-label-sc { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.18em; text-transform:uppercase; color:#7a5a2a; margin-bottom:10px; }
.rec-label-rc { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.18em; text-transform:uppercase; color:#2a5a8a; margin-bottom:10px; }
.rec-value-sc { font-family:'DM Mono',monospace; font-size:3.6rem; font-weight:500; color:#e8b840; line-height:1; }
.rec-value-rc { font-family:'DM Mono',monospace; font-size:3.6rem; font-weight:500; color:#60c0f0; line-height:1; }
.rec-unit-sc { font-family:'DM Mono',monospace; font-size:0.78rem; color:#7a5a2a; margin-top:6px; }
.rec-unit-rc { font-family:'DM Mono',monospace; font-size:0.78rem; color:#2a5a8a; margin-top:6px; }
.rec-note-sc { font-size:0.66rem; color:#7a5a2a; margin-top:14px; line-height:1.7; text-align:left; border-top:1px solid #3a2818; padding-top:12px; }
.rec-note-rc { font-size:0.66rem; color:#2a5a8a; margin-top:14px; line-height:1.7; text-align:left; border-top:1px solid #1a3050; padding-top:12px; }

/* ── Formula box ── */
.formula-box {
    background: #f2ede8;
    border: 1px solid #ddd5c8;
    border-radius: 4px;
    padding: 0.9rem 1.1rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #6a5a48;
    line-height: 2.1;
    margin-top: 12px;
}
.formula-box strong { color: #3a2818; }

/* ── Tab buttons ── */
div[data-testid="stHorizontalBlock"] button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    border-radius: 4px !important;
    padding: 10px 0 !important;
    transition: all 0.15s !important;
}

/* ── Footer ── */
.app-footer {
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid #ddd5c8;
    display: flex;
    justify-content: space-between;
    font-size: 0.64rem;
    color: #b0a898;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.02em;
}
</style>
""", unsafe_allow_html=True)


# ── Algorithm functions ───────────────────────────────────────────────────────
def sugarcane_calc(ndvi_fp, ndvi_nrs, max_yield, pct_n, nue):
    yp0      = min(12.07 * np.exp(1.47 * ndvi_fp), max_yield)
    gnup_yp0 = yp0 * (pct_n / 100) * 2000
    ri       = ((ndvi_nrs / ndvi_fp) * 1.94 - 0.91) if ndvi_fp > 0 else 0
    ypn      = min(yp0 * ri, max_yield)
    gnup_ypn = ypn * (pct_n / 100) * 2000
    fnr      = float(np.clip((gnup_ypn - gnup_yp0) / nue, 40, 180))
    return yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr

def rice_calc(ndvi_fp, ndvi_nrs, days, max_yield, pct_n, nue):
    insey    = ndvi_fp / days
    yp0      = min(5948.45 * (insey ** 0.72), max_yield)
    gnup_yp0 = yp0 * 45 * (pct_n / 100)
    ri       = ((ndvi_nrs / ndvi_fp) * 1.0077 + 0.19727) * 0.94 if ndvi_fp > 0 else 0
    ypn      = min(yp0 * ri, max_yield)
    gnup_ypn = ypn * 45 * (pct_n / 100)
    fnr      = float(np.clip((gnup_ypn - gnup_yp0) / nue, 0, 150))
    return yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr


# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header-inner">
    <div>
        <div class="app-title">N Rate Calculator</div>
        <p class="app-subtitle">Sensor-based midseason nitrogen recommendation · LSU AgCenter</p>
    </div>
    <div class="app-badge">LSU AgCenter · Tubana et al. · Research Use Only</div>
</div>
""", unsafe_allow_html=True)


# ── Tab switcher using session state ─────────────────────────────────────────
if "crop" not in st.session_state:
    st.session_state.crop = "sugarcane"

tab_col1, tab_col2, tab_spacer = st.columns([1, 1, 5])
with tab_col1:
    if st.button("🎋  Sugarcane", use_container_width=True,
                 type="primary" if st.session_state.crop == "sugarcane" else "secondary"):
        st.session_state.crop = "sugarcane"
        st.rerun()
with tab_col2:
    if st.button("🌾  Rice", use_container_width=True,
                 type="primary" if st.session_state.crop == "rice" else "secondary"):
        st.session_state.crop = "rice"
        st.rerun()

# Color the active button to match the crop theme
if st.session_state.crop == "sugarcane":
    st.markdown("""<style>
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background:#c87a20 !important; border-color:#c87a20 !important; color:#fff !important; font-weight:600 !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background:#f8f5f0 !important; border-color:#d8d0c4 !important; color:#8a8078 !important;
    }
    </style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background:#f8f5f0 !important; border-color:#d8d0c4 !important; color:#8a8078 !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background:#2a6a9a !important; border-color:#2a6a9a !important; color:#fff !important; font-weight:600 !important;
    }
    </style>""", unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
crop = st.session_state.crop


# ══════════════════════════════════════════════════════════════════════════════
# SUGARCANE
# ══════════════════════════════════════════════════════════════════════════════
if crop == "sugarcane":

    st.markdown('<div class="input-panel input-panel-sc"><div class="input-panel-title input-panel-title-sc">Sugarcane · Input Parameters</div>', unsafe_allow_html=True)
    i1, i2, i3, i4, i5 = st.columns(5)
    with i1:
        sc_nrs = st.number_input("NDVI — N Rich Strip", 0.01, 1.0, 0.87, 0.01, "%.2f", key="sc_nrs")
    with i2:
        sc_fp  = st.number_input("NDVI — Farmer's Practice", 0.01, 1.0, 0.75, 0.01, "%.2f", key="sc_fp")
    with i3:
        sc_yield = st.number_input("Max Yield (ton/ac)", 20, 200, 80, key="sc_yield")
    with i4:
        sc_pct = st.number_input("Stalk N Content (%)", 0.10, 1.0, 0.30, 0.01, "%.2f", key="sc_pct", help="Default 0.30%")
    with i5:
        sc_nue = st.number_input("N Use Efficiency", 0.10, 1.0, 0.70, 0.05, "%.2f", key="sc_nue")
    st.markdown('</div>', unsafe_allow_html=True)

    yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr = sugarcane_calc(sc_fp, sc_nrs, sc_yield, sc_pct, sc_nue)

    st.markdown('<div class="sec-label">NDVI Overview</div>', unsafe_allow_html=True)
    ov1, ov2, ov3 = st.columns(3)
    with ov1:
        f = int((sc_nrs-0.01)/0.99*100)
        st.markdown(f'<div class="d-card"><div class="d-card-label">N Rich Strip (NRS)</div><div class="d-card-value">{sc_nrs:.2f}</div><div class="ndvi-track"><div class="ndvi-fill-sc" style="width:{f}%"></div></div><div class="ndvi-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div></div>', unsafe_allow_html=True)
    with ov2:
        f = int((sc_fp-0.01)/0.99*100)
        st.markdown(f'<div class="d-card"><div class="d-card-label">Farmer\'s Practice (FP)</div><div class="d-card-value">{sc_fp:.2f}</div><div class="ndvi-track"><div class="ndvi-fill-sc" style="width:{f}%"></div></div><div class="ndvi-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div></div>', unsafe_allow_html=True)
    with ov3:
        d = sc_nrs - sc_fp
        dc = "#b84848" if abs(d)>0.20 else "#c49a28" if abs(d)>0.10 else "#a87830"
        st.markdown(f'<div class="d-card"><div class="d-card-label">NRS − FP Differential</div><div class="d-card-value" style="color:{dc}">{d:+.2f}</div><div class="d-card-sub">NRS is {abs(d):.2f} units {"above" if d>=0 else "below"} FP</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Model Results</div>', unsafe_allow_html=True)
    left, right = st.columns([3, 2], gap="large")

    with left:
        r1, r2 = st.columns(2)
        r3, r4 = st.columns(2)
        with r1:
            st.markdown(f'<div class="d-card"><div class="d-card-label">Yield Potential — No N (YP0)</div><div class="d-card-value">{yp0:.2f}<span class="d-card-unit">ton/ac</span></div></div>', unsafe_allow_html=True)
        with r2:
            st.markdown(f'<div class="d-card"><div class="d-card-label">Yield Potential — With N (YPN)</div><div class="d-card-value">{ypn:.2f}<span class="d-card-unit">ton/ac</span></div></div>', unsafe_allow_html=True)
        with r3:
            st.markdown(f'<div class="d-card"><div class="d-card-label">Stalk N Uptake — No N (GNUP₀)</div><div class="d-card-value">{gnup_yp0:.1f}<span class="d-card-unit">lb N/ac</span></div></div>', unsafe_allow_html=True)
        with r4:
            st.markdown(f'<div class="d-card"><div class="d-card-label">Stalk N Uptake — With N (GNUPₙ)</div><div class="d-card-value">{gnup_ypn:.1f}<span class="d-card-unit">lb N/ac</span></div></div>', unsafe_allow_html=True)

        rp = int(min(max((ri/2.0)*100,0),100))
        rc = "#b84848" if ri>1.2 else "#c49a28" if ri>1.0 else "#a87830"
        st.markdown(f'<div class="ri-card"><div class="d-card-label">Response Index (RI) &nbsp;·&nbsp;<span style="font-family:\'DM Mono\',monospace;font-size:0.58rem;color:#c0b0a0">(NDVI_NRS / NDVI_FP) × 1.94 − 0.91</span></div><div class="d-card-value" style="color:{rc}">{ri:.4f}</div><div class="ri-track"><div class="ri-fill" style="width:{rp}%;background:{rc}"></div></div><div class="ndvi-ticks"><span>0.0</span><span>1.0</span><span>2.0</span></div></div>', unsafe_allow_html=True)

        if ri>1.2: ic,im = "interp-high", f"RI of {ri:.3f} indicates a strong crop response to nitrogen. Application is recommended to avoid yield loss."
        elif ri>1.0: ic,im = "interp-mod", f"RI of {ri:.3f} suggests a moderate response. Evaluate application against economic threshold."
        else: ic,im = "interp-low", f"RI of {ri:.3f} indicates low expected response. Additional nitrogen may not be economically justified."
        st.markdown(f'<div class="interp {ic}">{im}</div>', unsafe_allow_html=True)

    with right:
        st.markdown(f"""<div class="rec-box-sc">
            <div class="rec-label-sc">Fertilizer N Requirement</div>
            <div class="rec-value-sc">{fnr:.0f}</div>
            <div class="rec-unit-sc">lbs N / acre</div>
            <div class="rec-note-sc">Bounded 40–180 lb N/ac per LSU AgCenter sugarcane guidelines.<br>Adjust NUE to reflect fertilizer source, timing, and soil conditions.</div>
        </div>
        <div class="formula-box">
            <strong>YP0</strong> &nbsp;= 12.07 × e^(NDVI_FP × 1.47)<br>
            <strong>RI</strong> &nbsp;&nbsp;= (NRS / FP) × 1.94 − 0.91<br>
            <strong>YPN</strong> &nbsp;= YP0 × RI &nbsp;[capped at max yield]<br>
            <strong>GNUP</strong> = Yield × %N × 2000<br>
            <strong>FNR</strong> &nbsp;&nbsp;= (GNUPₙ − GNUP₀) / NUE
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RICE
# ══════════════════════════════════════════════════════════════════════════════
else:

    st.markdown('<div class="input-panel input-panel-rc"><div class="input-panel-title input-panel-title-rc">Rice · Input Parameters</div>', unsafe_allow_html=True)
    i1, i2, i3, i4, i5, i6 = st.columns(6)
    with i1:
        rc_nrs = st.number_input("NDVI — N Rich Strip", 0.01, 1.0, 0.80, 0.01, "%.2f", key="rc_nrs")
    with i2:
        rc_fp  = st.number_input("NDVI — Farmer's Practice", 0.01, 1.0, 0.77, 0.01, "%.2f", key="rc_fp")
    with i3:
        rc_days = st.number_input("Days — Planting to Sensing", 1, 180, 71, key="rc_days", help="Days from planting to NDVI sensing")
    with i4:
        rc_yield = st.number_input("Max Yield (bu/ac)", 50, 600, 320, key="rc_yield")
    with i5:
        rc_pct = st.number_input("Grain N Content (%)", 0.50, 3.0, 1.20, 0.01, "%.2f", key="rc_pct", help="Default 1.2%")
    with i6:
        rc_nue = st.number_input("N Use Efficiency", 0.10, 1.0, 0.75, 0.05, "%.2f", key="rc_nue")
    st.markdown('</div>', unsafe_allow_html=True)

    yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr = rice_calc(rc_fp, rc_nrs, rc_days, rc_yield, rc_pct, rc_nue)

    st.markdown('<div class="sec-label">NDVI Overview</div>', unsafe_allow_html=True)
    ov1, ov2, ov3 = st.columns(3)
    with ov1:
        f = int((rc_nrs-0.01)/0.99*100)
        st.markdown(f'<div class="d-card"><div class="d-card-label">N Rich Strip (NRS)</div><div class="d-card-value">{rc_nrs:.2f}</div><div class="ndvi-track"><div class="ndvi-fill-rc" style="width:{f}%"></div></div><div class="ndvi-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div></div>', unsafe_allow_html=True)
    with ov2:
        f = int((rc_fp-0.01)/0.99*100)
        st.markdown(f'<div class="d-card"><div class="d-card-label">Farmer\'s Practice (FP)</div><div class="d-card-value">{rc_fp:.2f}</div><div class="ndvi-track"><div class="ndvi-fill-rc" style="width:{f}%"></div></div><div class="ndvi-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div></div>', unsafe_allow_html=True)
    with ov3:
        d = rc_nrs - rc_fp
        dc = "#b84848" if abs(d)>0.20 else "#c49a28" if abs(d)>0.10 else "#2a6a9a"
        st.markdown(f'<div class="d-card"><div class="d-card-label">NRS − FP Differential</div><div class="d-card-value" style="color:{dc}">{d:+.2f}</div><div class="d-card-sub">NRS is {abs(d):.2f} units {"above" if d>=0 else "below"} FP</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Model Results</div>', unsafe_allow_html=True)
    left, right = st.columns([3, 2], gap="large")

    with left:
        r1, r2 = st.columns(2)
        r3, r4 = st.columns(2)
        with r1:
            st.markdown(f'<div class="d-card"><div class="d-card-label">Yield Potential — No N (YP0)</div><div class="d-card-value">{yp0:.1f}<span class="d-card-unit">bu/ac</span></div></div>', unsafe_allow_html=True)
        with r2:
            st.markdown(f'<div class="d-card"><div class="d-card-label">Yield Potential — With N (YPN)</div><div class="d-card-value">{ypn:.1f}<span class="d-card-unit">bu/ac</span></div></div>', unsafe_allow_html=True)
        with r3:
            st.markdown(f'<div class="d-card"><div class="d-card-label">Grain N Uptake — No N (GNUP₀)</div><div class="d-card-value">{gnup_yp0:.1f}<span class="d-card-unit">lb N/ac</span></div></div>', unsafe_allow_html=True)
        with r4:
            st.markdown(f'<div class="d-card"><div class="d-card-label">Grain N Uptake — With N (GNUPₙ)</div><div class="d-card-value">{gnup_ypn:.1f}<span class="d-card-unit">lb N/ac</span></div></div>', unsafe_allow_html=True)

        rp = int(min(max((ri/2.0)*100,0),100))
        rc_col = "#b84848" if ri>1.2 else "#c49a28" if ri>1.0 else "#2a6a9a"
        st.markdown(f'<div class="ri-card"><div class="d-card-label">Response Index (RI) &nbsp;·&nbsp;<span style="font-family:\'DM Mono\',monospace;font-size:0.58rem;color:#c0b0a0">((NRS/FP) × 1.0077 + 0.19727) × 0.94</span></div><div class="d-card-value" style="color:{rc_col}">{ri:.4f}</div><div class="ri-track"><div class="ri-fill" style="width:{rp}%;background:{rc_col}"></div></div><div class="ndvi-ticks"><span>0.0</span><span>1.0</span><span>2.0</span></div></div>', unsafe_allow_html=True)

        if ri>1.2: ic,im = "interp-high", f"RI of {ri:.3f} indicates a strong crop response to nitrogen. Midseason application is recommended."
        elif ri>1.0: ic,im = "interp-mod", f"RI of {ri:.3f} suggests a moderate response. Evaluate application against economic threshold."
        else: ic,im = "interp-low", f"RI of {ri:.3f} indicates low expected response. Midseason nitrogen may not be economically justified."
        st.markdown(f'<div class="interp {ic}">{im}</div>', unsafe_allow_html=True)

    with right:
        st.markdown(f"""<div class="rec-box-rc">
            <div class="rec-label-rc">Midseason N Requirement</div>
            <div class="rec-value-rc">{fnr:.0f}</div>
            <div class="rec-unit-rc">lbs N / acre</div>
            <div class="rec-note-rc">Bounded 0–150 lb N/ac per LSU AgCenter rice guidelines.<br>Adjust NUE for fertilizer source and flood conditions.</div>
        </div>
        <div class="formula-box">
            <strong>INSEY</strong> = NDVI_FP / days from planting<br>
            <strong>YP0</strong> &nbsp;&nbsp;= 5948.45 × INSEY^0.72<br>
            <strong>RI</strong> &nbsp;&nbsp;&nbsp;= ((NRS/FP) × 1.0077 + 0.19727) × 0.94<br>
            <strong>YPN</strong> &nbsp;&nbsp;= YP0 × RI &nbsp;[capped at max yield]<br>
            <strong>GNUP</strong> &nbsp;= Yield × 45 lbs/bu × %N<br>
            <strong>FNR</strong> &nbsp;&nbsp;&nbsp;= (GNUPₙ − GNUP₀) / NUE
        </div>""", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <span>LSU AgCenter · Tubana, Johnson & Viator (Sugarcane) · Tubana, Harrell & Walker (Rice)</span>
    <span>For research use only · Not a substitute for professional agronomic advice</span>
</div>
""", unsafe_allow_html=True)
