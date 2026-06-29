# ──────────────────────────────────────────────────────────────────────────────
# LSU AgCenter — N Rate Calculator
# Combined Sugarcane and Rice Sensor-Based Nitrogen Recommendation Tool
# Authors: Tubana, Johnson & Viator (Sugarcane) · Tubana, Harrell & Walker (Rice)
# ──────────────────────────────────────────────────────────────────────────────

# Import Streamlit — the library that turns this Python script into a web app
import streamlit as st

# Import NumPy — provides math functions like exp() and clip()
import numpy as np


# ── PAGE CONFIGURATION ────────────────────────────────────────────────────────
# Must be the FIRST Streamlit command in the file
# Sets the browser tab title, icon, and page width
st.set_page_config(
    page_title="LSU AgCenter · N Rate Calculator",  # text shown in the browser tab
    page_icon="🌾",                                  # icon shown in the browser tab
    layout="wide"                                    # use the full browser width
)


# ── CSS STYLING ───────────────────────────────────────────────────────────────
# CSS controls how everything looks: colors, fonts, sizes, spacing, borders
# We inject it using st.markdown() — unsafe_allow_html=True lets HTML/CSS render
st.markdown("""
<style>

/* Load three fonts from Google Fonts:
   Playfair Display — elegant serif for the main title
   DM Mono         — monospace for numbers and code-style labels
   DM Sans         — clean modern font for all regular text */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=DM+Mono:wght@400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

/* Apply DM Sans as the default font for everything on the page */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Warm off-white page background — softer than pure white */
.stApp {
    background-color: #f8f5f0;
}

/* Hide Streamlit's default top menu bar, footer, and header */
#MainMenu, footer, header { visibility: hidden; }

/* ── NUMBER INPUT LABELS ──
   The label above each number input box.
   Without these overrides, labels can be invisible in some browser themes. */
.stNumberInput > label {
    font-size: 0.7rem !important;         /* small text */
    font-weight: 500 !important;           /* medium weight */
    color: #3a3228 !important;             /* dark brown — always readable */
    letter-spacing: 0.04em !important;    /* slightly spaced letters */
    text-transform: uppercase !important;  /* ALL CAPS label style */
}

/* ── NUMBER INPUT BOX ──
   The white box where the user types a value. */
.stNumberInput input {
    background-color: #ffffff !important;    /* white background */
    border: 1.5px solid #d8d0c4 !important;  /* warm gray border */
    color: #1a1410 !important;               /* near-black text so numbers are readable */
    font-family: 'DM Mono', monospace !important; /* monospace keeps digits aligned */
    font-size: 1.05rem !important;
    border-radius: 4px !important;           /* slightly rounded corners */
    padding: 8px 12px !important;            /* comfortable inner spacing */
}

/* Gold glow when user clicks into an input box */
.stNumberInput input:focus {
    border-color: #8a6a2a !important;
    box-shadow: 0 0 0 3px rgba(138,106,42,0.1) !important;
    outline: none !important;
}

/* ── PAGE HEADER ──
   The top strip with the title on the left and the badge on the right */
.app-header-inner {
    display: flex;                     /* side-by-side layout */
    align-items: flex-start;           /* align items to the top */
    justify-content: space-between;    /* push title left, badge right */
    padding: 2.4rem 0 1.6rem 0;
    border-bottom: 1px solid #d8d0c4; /* thin divider line under the header */
    margin-bottom: 1.6rem;
}

/* Main serif title "N Rate Calculator" */
.app-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 600;
    color: #1a1410;
    margin: 0 0 4px 0;
    letter-spacing: -0.01em;
    line-height: 1.2;
}

/* Italic subtitle below the title */
.app-subtitle {
    font-size: 0.78rem;
    color: #8a8078;
    font-weight: 300;
    font-style: italic;
    margin: 0;
}

/* Small bordered badge in the top-right corner */
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

/* ── INPUT PANEL ──
   The colored box containing all input fields for each crop */
.input-panel {
    border-radius: 6px;
    padding: 1.6rem 1.8rem 1.4rem 1.8rem;
    margin-bottom: 2rem;
    border: 1px solid;   /* border color set per crop below */
}
/* Sugarcane panel: warm amber gradient */
.input-panel-sc {
    background: linear-gradient(135deg, #fffbf4 0%, #fff8ec 100%);
    border-color: #e8d4a8;
}
/* Rice panel: cool blue gradient */
.input-panel-rc {
    background: linear-gradient(135deg, #f4f8ff 0%, #edf4fc 100%);
    border-color: #b8d0e8;
}

/* Small uppercase label at the top of each input panel */
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
/* Sugarcane title: amber */
.input-panel-title-sc { color: #a87830; border-bottom-color: #e8d4a8; }
/* Rice title: blue */
.input-panel-title-rc { color: #2a6a9a; border-bottom-color: #b8d0e8; }

/* ── SECTION LABEL ──
   Thin uppercase dividers between content groups */
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

/* ── DATA CARDS ──
   White boxes used to display each individual result value */
.d-card {
    background: #ffffff;
    border: 1px solid #e0d8cc;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin-bottom: 10px;
}
/* Small uppercase label above the number */
.d-card-label {
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #a09080;
    font-weight: 500;
    margin-bottom: 6px;
}
/* The large number value */
.d-card-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.65rem;
    font-weight: 500;
    color: #1a1410;
    line-height: 1;
}
/* Small unit text after the number (e.g. "ton/ac") */
.d-card-unit {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #a09080;
    margin-left: 5px;
}
/* Optional small descriptive text below the value */
.d-card-sub { font-size: 0.68rem; color: #a09080; margin-top: 5px; }

/* ── NDVI PROGRESS BAR ──
   Thin colored bar showing the NDVI value visually on a 0–1 scale */
.ndvi-track {
    height: 4px;
    border-radius: 1px;
    margin: 9px 0 4px 0;
    overflow: hidden;      /* clips the fill inside the track */
    background: #ede8e0;   /* light gray unfilled portion */
}
/* Sugarcane bar: amber/gold gradient */
.ndvi-fill-sc { height:100%; border-radius:1px; background: linear-gradient(90deg, #e8c878, #a87830); }
/* Rice bar: blue gradient */
.ndvi-fill-rc { height:100%; border-radius:1px; background: linear-gradient(90deg, #7ab4d8, #1a4a7a); }
/* Axis labels below the bar: 0.0, 0.5, 1.0 */
.ndvi-ticks { display:flex; justify-content:space-between; font-family:'DM Mono',monospace; font-size:0.56rem; color:#c0b8a8; }

/* ── RESPONSE INDEX CARD ──
   Same structure as .d-card, used for the RI display row */
.ri-card {
    background: #ffffff;
    border: 1px solid #e0d8cc;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin-bottom: 10px;
}
/* Track inside the RI card — slightly taller than the NDVI bar */
.ri-track { height:5px; border-radius:1px; margin:10px 0 4px 0; overflow:hidden; background:#ede8e0; }
/* Fill color is set dynamically in Python based on the RI value */
.ri-fill { height:100%; border-radius:1px; opacity:0.7; }

/* ── INTERPRETATION BAR ──
   Colored message explaining what the RI value means agronomically */
.interp {
    border-radius: 3px;
    padding: 10px 14px;
    font-size: 0.77rem;
    margin-top: 10px;
    border-left: 2px solid;  /* colored accent bar on the left edge */
    line-height: 1.55;
}
/* Green: RI < 1.0 — low response */
.interp-low  { background:#f4fcf8; border-color:#3a8a60; color:#1a3a28; }
/* Amber: RI 1.0–1.2 — moderate response */
.interp-mod  { background:#fdf8ee; border-color:#c49a28; color:#5a4200; }
/* Red: RI > 1.2 — strong response, application recommended */
.interp-high { background:#fdf2f0; border-color:#b84848; color:#5a1818; }

/* ── RECOMMENDATION BOX — SUGARCANE ──
   Dark brown box showing the final N rate in large gold numbers */
.rec-box-sc {
    background: linear-gradient(160deg, #2a1e0e 0%, #1a1208 100%);
    border-radius: 5px;
    padding: 2rem 1.6rem;
    text-align: center;
    border: 1px solid #4a3618;
}
.rec-label-sc { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.18em; text-transform:uppercase; color:#7a5a2a; margin-bottom:10px; }
/* Large gold number */
.rec-value-sc { font-family:'DM Mono',monospace; font-size:3.6rem; font-weight:500; color:#e8b840; line-height:1; }
.rec-unit-sc { font-family:'DM Mono',monospace; font-size:0.78rem; color:#7a5a2a; margin-top:6px; }
/* Disclaimer note at the bottom of the box */
.rec-note-sc { font-size:0.66rem; color:#7a5a2a; margin-top:14px; line-height:1.7; text-align:left; border-top:1px solid #3a2818; padding-top:12px; }

/* ── RECOMMENDATION BOX — RICE ──
   Same structure as sugarcane but dark blue with cyan numbers */
.rec-box-rc {
    background: linear-gradient(160deg, #0e1e2e 0%, #081420 100%);
    border-radius: 5px;
    padding: 2rem 1.6rem;
    text-align: center;
    border: 1px solid #1a3a5a;
}
.rec-label-rc { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.18em; text-transform:uppercase; color:#2a5a8a; margin-bottom:10px; }
/* Large sky-blue number */
.rec-value-rc { font-family:'DM Mono',monospace; font-size:3.6rem; font-weight:500; color:#60c0f0; line-height:1; }
.rec-unit-rc { font-family:'DM Mono',monospace; font-size:0.78rem; color:#2a5a8a; margin-top:6px; }
.rec-note-rc { font-size:0.66rem; color:#2a5a8a; margin-top:14px; line-height:1.7; text-align:left; border-top:1px solid #1a3050; padding-top:12px; }

/* ── FORMULA REFERENCE BOX ──
   Warm beige box showing the algorithm equations next to the recommendation */
.formula-box {
    background: #f2ede8;
    border: 1px solid #ddd5c8;
    border-radius: 4px;
    padding: 0.9rem 1.1rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #6a5a48;
    line-height: 2.1;     /* generous line spacing for readability */
    margin-top: 12px;
}
/* Bold variable names inside the formula box */
.formula-box strong { color: #3a2818; }

/* ── TAB BUTTONS ──
   The crop selector buttons at the top of the page */
div[data-testid="stHorizontalBlock"] button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    border-radius: 4px !important;
    padding: 10px 0 !important;
    transition: all 0.15s !important;  /* smooth color change on click */
}

/* ── PAGE FOOTER ──
   Small two-sided bar at the bottom: attribution left, disclaimer right */
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
""", unsafe_allow_html=True)  # unsafe_allow_html=True is required for raw HTML and CSS to render


# ── ALGORITHM FUNCTIONS ───────────────────────────────────────────────────────
# Pure math — completely separate from the display code.
# Inputs go in, all intermediate values come out.

def sugarcane_calc(ndvi_fp, ndvi_nrs, max_yield, pct_n, nue, high_n_cultivar=False):
    """
    LSU AgCenter Sugarcane N Rate Algorithm
    Tubana, Johnson & Viator

    Parameters:
      ndvi_fp         — NDVI of the farmer's practice field (no extra N applied)
      ndvi_nrs        — NDVI of the N-Rich reference strip (well fertilized)
      max_yield       — yield ceiling in ton/ac (typically 2x the 5-year average)
      pct_n           — nitrogen content of sugarcane stalk as a percentage (default 0.30%)
      nue             — N use efficiency: fraction of applied N actually absorbed by the crop
      high_n_cultivar — if True, raises the FNR ceiling from 140 to 200 lbs N/ac.
                        Added for the HoCP14-885 cultivar, which sometimes requires
                        a higher midseason N rate than the standard algorithm allows.

    Returns: yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr
    """

    # Step 1: Predict yield potential WITHOUT additional nitrogen
    # Exponential regression calibrated from LSU AgCenter field trials
    # min() caps the result at the regional maximum yield ceiling
    yp0 = min(12.07 * np.exp(1.47 * ndvi_fp), max_yield)

    # Step 2: Stalk N uptake at YP0 (no added N)
    # Yield (ton/ac) × 2000 converts to lbs/ac
    # × (pct_n / 100) converts the percentage to a decimal
    # Formula verified exactly against LSU AgCenter Excel: GNUP = yield × 2000 lbs/ton × (%N / 100)
    gnup_yp0 = yp0 * 2000 * (pct_n / 100)

    # Step 3: Response Index (RI)
    # Measures how much better the N-Rich strip looks vs the field
    # RI > 1.2 → strong N response; RI 1.0-1.2 → moderate; RI < 1.0 → low
    # Verified exactly against the LSU AgCenter "Formulas" sheet (the live, linked calculation)
    ri = ((ndvi_nrs / ndvi_fp) * 1.94 - 0.91) if ndvi_fp > 0 else 0

    # Step 4: Yield potential WITH nitrogen applied (uncapped)
    # Multiply no-N yield by RI to estimate the yield gain from fertilization
    ypn_uncap = yp0 * ri

    # Capped version of YPN, used for display only
    ypn = min(ypn_uncap, max_yield)

    # Step 5: Stalk N uptake at YPN (with added N)
    # IMPORTANT: this uses the UNCAPPED YPN, exactly as in the LSU AgCenter Excel (cell I17 = G18*2000*0.003)
    gnup_ypn = ypn_uncap * 2000 * (pct_n / 100)

    # Step 6: Fertilizer N requirement
    # The N uptake gap (gnup_ypn - gnup_yp0) divided by efficiency
    raw_fnr = (gnup_ypn - gnup_yp0) / nue

    # Excel's actual rule is NOT a simple clip — verified directly from the Formulas sheet:
    #   J8 = IF(J18 > 120, 140, J18)   -- if raw FNR exceeds 120, force it to exactly 140
    #   J9 = IF(J8 < 40, 40, J8)       -- floor at 40
    # For the HoCP14-885 cultivar, the same >120 trigger applies but the ceiling
    # is raised to 200 lbs N/ac instead of 140, since this cultivar sometimes
    # needs a higher midseason N rate than the standard algorithm allows.
    ceiling = 200.0 if high_n_cultivar else 140.0
    fnr = ceiling if raw_fnr > 120 else raw_fnr
    fnr = 40.0 if fnr < 40 else fnr

    # Return all six values so every step can be displayed in the app
    return yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr


def rice_calc(ndvi_fp, ndvi_nrs, max_yield, pct_n, nue):
    """
    LSU AgCenter / MSU Rice Midseason N Rate Algorithm
    Tubana, Harrell & Walker

    Parameters:
      ndvi_fp    — NDVI of the farmer's practice field
      ndvi_nrs   — NDVI of the N-Rich reference strip
      max_yield  — yield ceiling in bu/ac
      pct_n      — grain N content as a percentage (default 1.2%)
      nue        — N use efficiency

    Returns: yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr
    """

    # Step 1: Yield potential WITHOUT nitrogen using a power function of raw NDVI
    # Verified exactly against the LSU AgCenter/MSU Excel "Formulas" sheet (cell D15):
    #   YP0 = (12088 × NDVI_FP^0.72) ÷ 1.12 ÷ 45
    # The /1.12/45 factors are part of the live formula, not arbitrary — they convert
    # the original regression (in different units) into bu/ac.
    # Result capped at max_yield
    yp0_uncap = (12088 * (ndvi_fp ** 0.72)) / 1.12 / 45
    yp0 = min(yp0_uncap, max_yield)

    # Step 2: Grain N uptake at YP0 (no added N)
    # Excel uses a fixed 1.2% grain N (0.012), not the pct_n parameter — kept here as pct_n
    # so the UI input still works, but defaults to 1.2 to match the verified Excel exactly
    gnup_yp0 = yp0 * (pct_n / 100) * 45

    # Step 3: Response Index — rice-specific formula, with a safety override for extreme ratios
    # Verified exactly against Excel cell H5:
    #   IF (NRS/FP) > 2.09938  →  RI = 2.298 × NDVI_FP   (caps RI for unrealistic NDVI gaps)
    #   ELSE                    →  RI = ((NRS/FP) × 1.0077 + 0.19727) × 0.94
    if ndvi_fp > 0:
        ratio = ndvi_nrs / ndvi_fp
        if ratio > 2.09938:
            ri = 2.298 * ndvi_fp
        else:
            ri = (ratio * 1.0077 + 0.19727) * 0.94
    else:
        ri = 0

    # Step 4: Yield potential WITH nitrogen, capped at max yield
    # IMPORTANT: unlike sugarcane, rice's GNUP_YPN uses the CAPPED YPN (verified Excel cell I15 = H15*...)
    ypn_uncap = yp0 * ri
    ypn = min(ypn_uncap, max_yield)

    # Step 5: Grain N uptake at YPN (with added N) — uses capped YPN
    gnup_ypn = ypn * (pct_n / 100) * 45

    # Step 6: Fertilizer N requirement
    # Verified Excel rule (cell H8): floor at 0 only — no upper cap in the live formula
    raw_fnr = (gnup_ypn - gnup_yp0) / nue
    fnr = 0.0 if raw_fnr < 0 else float(raw_fnr)

    return yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr


# ── PAGE HEADER ───────────────────────────────────────────────────────────────
# Render the title block using HTML for precise styling
st.markdown("""
<div class="app-header-inner">
    <div>
        <div class="app-title">N Rate Calculator</div>
        <p class="app-subtitle">Sensor-based midseason nitrogen recommendation · LSU AgCenter</p>
    </div>
    <div class="app-badge">LSU AgCenter · Tubana et al. · Research Use Only</div>
</div>
""", unsafe_allow_html=True)


# ── TAB STATE ─────────────────────────────────────────────────────────────────
# Streamlit reruns the entire script every time a widget changes.
# st.session_state persists between reruns — without it the crop would reset on every click.

# Set "sugarcane" as the default crop only on the very first load
if "crop" not in st.session_state:
    st.session_state.crop = "sugarcane"

# Two narrow button columns plus a wide spacer column
tab_col1, tab_col2, tab_spacer = st.columns([1, 1, 5])

with tab_col1:
    # type="primary" fills the button with color when it is the active tab
    if st.button(
        "🎋  Sugarcane",
        use_container_width=True,  # button stretches to fill its column
        type="primary" if st.session_state.crop == "sugarcane" else "secondary"
    ):
        st.session_state.crop = "sugarcane"  # save the selection
        st.rerun()                            # rerun immediately to show sugarcane UI

with tab_col2:
    if st.button(
        "🌾  Rice",
        use_container_width=True,
        type="primary" if st.session_state.crop == "rice" else "secondary"
    ):
        st.session_state.crop = "rice"
        st.rerun()

# Inject CSS to color each button in its crop-specific theme
# This reruns every render to keep the active button highlighted
if st.session_state.crop == "sugarcane":
    st.markdown("""<style>
    /* Sugarcane button: filled amber/gold */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background:#c87a20 !important; border-color:#c87a20 !important;
        color:#fff !important; font-weight:600 !important;
    }
    /* Rice button: unfilled / muted */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background:#f8f5f0 !important; border-color:#d8d0c4 !important;
        color:#8a8078 !important;
    }
    </style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>
    /* Sugarcane button: unfilled / muted */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background:#f8f5f0 !important; border-color:#d8d0c4 !important;
        color:#8a8078 !important;
    }
    /* Rice button: filled blue */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background:#2a6a9a !important; border-color:#2a6a9a !important;
        color:#fff !important; font-weight:600 !important;
    }
    </style>""", unsafe_allow_html=True)

# Small vertical gap between buttons and the input panel
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# Read the active crop into a simple variable for use in the if/else below
crop = st.session_state.crop


# ══════════════════════════════════════════════════════════════════════════════
# SUGARCANE CALCULATOR
# Runs only when the Sugarcane tab is active
# ══════════════════════════════════════════════════════════════════════════════
if crop == "sugarcane":

    # Open the amber input panel and render its title label
    st.markdown(
        '<div class="input-panel input-panel-sc">'
        '<div class="input-panel-title input-panel-title-sc">Sugarcane · Input Parameters</div>',
        unsafe_allow_html=True
    )

    # Five equal columns — one per input field
    i1, i2, i3, i4, i5 = st.columns(5)

    with i1:
        # NDVI from the well-fertilized N-Rich reference strip
        # key="sc_nrs" keeps this widget independent from the rice tab's widgets
        sc_nrs = st.number_input(
            "NDVI — N Rich Strip",
            min_value=0.01, max_value=1.0, value=0.87, step=0.01, format="%.2f",
            key="sc_nrs"
        )

    with i2:
        # NDVI from the target field the farmer wants to fertilize
        sc_fp = st.number_input(
            "NDVI — Farmer's Practice",
            min_value=0.01, max_value=1.0, value=0.75, step=0.01, format="%.2f",
            key="sc_fp"
        )

    with i3:
        # Regional maximum yield — caps the model so predictions stay realistic
        # Typically set to 2× the 5-year average yield for the farm
        sc_yield = st.number_input(
            "Max Yield (ton/ac)",
            min_value=20, max_value=200, value=80,
            key="sc_yield"
        )

    with i4:
        # Percentage of nitrogen in the dry matter of the sugarcane stalk
        # LSU AgCenter default is 0.30% for shredded sugarcane stalk
        sc_pct = st.number_input(
            "Stalk N Content (%)",
            min_value=0.01, max_value=1.0, value=0.30, step=0.01, format="%.2f",
            key="sc_pct", help="Default 0.30% — LSU AgCenter"
        )

    with i5:
        # Fraction of applied fertilizer N that the crop actually absorbs
        # The remainder is lost to leaching, volatilization, or runoff
        sc_nue = st.number_input(
            "N Use Efficiency",
            min_value=0.10, max_value=1.0, value=0.70, step=0.05, format="%.2f",
            key="sc_nue"
        )

    # Close the input panel HTML div
    st.markdown('</div>', unsafe_allow_html=True)

    # Special cultivar question — HoCP14-885 sometimes needs a higher midseason N rate
    # than the standard algorithm's 140 lb/ac ceiling allows
    # Two columns: narrow one for the text input, wide one for the explanatory caption
    cb_col, cb_text_col = st.columns([1, 6])
    with cb_col:
        sc_cultivar_input = st.text_input("HoCP14-885?", value="No")
    with cb_text_col:
        st.caption(
            "This cultivar sometimes requires higher N recommendations. "
            "Type \"Yes\" to raise the fertilizer N ceiling from 140 to 200 lbs N/ac, "
            "or \"No\" to keep the standard ceiling."
        )

    # Convert the typed answer into a boolean — accepts Yes/No in any capitalization
    sc_high_n = sc_cultivar_input.strip().lower() == "yes"

    # ── RUN THE ALGORITHM ─────────────────────────────────────────────────────
    # Pass all inputs to the function; unpack the 6 returned values
    yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr = sugarcane_calc(
        sc_fp,      # NDVI farmer's practice
        sc_nrs,     # NDVI N-Rich strip
        sc_yield,   # maximum yield ceiling
        sc_pct,     # stalk N content %
        sc_nue,     # N use efficiency
        sc_high_n   # HoCP14-885 high-N cultivar override
    )

    # ── NDVI OVERVIEW ─────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">NDVI Overview</div>', unsafe_allow_html=True)

    ov1, ov2, ov3 = st.columns(3)

    with ov1:
        # Convert NDVI (0.01–1.0) to a 0–100% fill for the visual progress bar
        f = int((sc_nrs - 0.01) / 0.99 * 100)
        # f-string embeds the Python value directly into the HTML
        st.markdown(f"""
        <div class="d-card">
            <div class="d-card-label">N Rich Strip (NRS)</div>
            <div class="d-card-value">{sc_nrs:.2f}</div>
            <div class="ndvi-track"><div class="ndvi-fill-sc" style="width:{f}%"></div></div>
            <div class="ndvi-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div>
        </div>""", unsafe_allow_html=True)

    with ov2:
        # Same bar for the farmer's practice NDVI
        f = int((sc_fp - 0.01) / 0.99 * 100)
        st.markdown(f"""
        <div class="d-card">
            <div class="d-card-label">Farmer's Practice (FP)</div>
            <div class="d-card-value">{sc_fp:.2f}</div>
            <div class="ndvi-track"><div class="ndvi-fill-sc" style="width:{f}%"></div></div>
            <div class="ndvi-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div>
        </div>""", unsafe_allow_html=True)

    with ov3:
        # Difference between NRS and FP readings
        d = sc_nrs - sc_fp
        # Color: red if gap > 0.20, amber if gap > 0.10, gold if small gap
        dc = "#b84848" if abs(d) > 0.20 else "#c49a28" if abs(d) > 0.10 else "#a87830"
        st.markdown(f"""
        <div class="d-card">
            <div class="d-card-label">NRS − FP Differential</div>
            <div class="d-card-value" style="color:{dc}">{d:+.2f}</div>
            <div class="d-card-sub">NRS is {abs(d):.2f} units {"above" if d >= 0 else "below"} FP</div>
        </div>""", unsafe_allow_html=True)

    # Small vertical spacer between sections
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── MODEL RESULTS ─────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Model Results</div>', unsafe_allow_html=True)

    # Left column gets 3/5 of the width (metric cards); right gets 2/5 (N rate box)
    left, right = st.columns([3, 2], gap="large")

    with left:
        r1, r2 = st.columns(2)   # first row: yield potentials
        r3, r4 = st.columns(2)   # second row: N uptake values

        with r1:
            # Yield the crop is currently on track for with no additional N
            st.markdown(f"""
            <div class="d-card">
                <div class="d-card-label">Yield Potential — No N (YP0)</div>
                <div class="d-card-value">{yp0:.2f}<span class="d-card-unit">ton/ac</span></div>
            </div>""", unsafe_allow_html=True)

        with r2:
            # Yield the crop could achieve if nitrogen is applied
            st.markdown(f"""
            <div class="d-card">
                <div class="d-card-label">Yield Potential — With N (YPN)</div>
                <div class="d-card-value">{ypn:.2f}<span class="d-card-unit">ton/ac</span></div>
            </div>""", unsafe_allow_html=True)

        with r3:
            # Lbs of N in the stalk dry matter at YP0 — no added N scenario
            st.markdown(f"""
            <div class="d-card">
                <div class="d-card-label">Stalk N Uptake — No N (GNUP₀)</div>
                <div class="d-card-value">{gnup_yp0:.1f}<span class="d-card-unit">lb N/ac</span></div>
            </div>""", unsafe_allow_html=True)

        with r4:
            # Lbs of N in the stalk dry matter at YPN — with added N scenario
            st.markdown(f"""
            <div class="d-card">
                <div class="d-card-label">Stalk N Uptake — With N (GNUPₙ)</div>
                <div class="d-card-value">{gnup_ypn:.1f}<span class="d-card-unit">lb N/ac</span></div>
            </div>""", unsafe_allow_html=True)

        # RI card with a visual bar showing position on the 0–2 scale
        rp = int(min(max((ri / 2.0) * 100, 0), 100))   # convert RI to 0-100% bar width
        rc = "#b84848" if ri > 1.2 else "#c49a28" if ri > 1.0 else "#a87830"
        st.markdown(f"""
        <div class="ri-card">
            <div class="d-card-label">Response Index (RI) &nbsp;·&nbsp;
                <span style="font-family:'DM Mono',monospace;font-size:0.58rem;color:#c0b0a0">
                    (NDVI_NRS / NDVI_FP) × 1.94 − 0.91
                </span>
            </div>
            <div class="d-card-value" style="color:{rc}">{ri:.4f}</div>
            <div class="ri-track">
                <div class="ri-fill" style="width:{rp}%;background:{rc}"></div>
            </div>
            <div class="ndvi-ticks"><span>0.0</span><span>1.0</span><span>2.0</span></div>
        </div>""", unsafe_allow_html=True)

        # Select the interpretation message based on RI value
        if ri > 1.2:
            # Strong response — applying N is agronomically justified
            ic, im = "interp-high", f"RI of {ri:.3f} indicates a strong crop response to nitrogen. Application is recommended to avoid yield loss."
        elif ri > 1.0:
            # Moderate response — evaluate against economic return
            ic, im = "interp-mod", f"RI of {ri:.3f} suggests a moderate response. Evaluate application against economic threshold."
        else:
            # Low response — crop is likely well-supplied already
            ic, im = "interp-low", f"RI of {ri:.3f} indicates low expected response. Additional nitrogen may not be economically justified."

        # Render the colored interpretation bar with the selected message
        st.markdown(f'<div class="interp {ic}">{im}</div>', unsafe_allow_html=True)

    with right:
        # Dynamic ceiling note and formula text depending on the cultivar checkbox
        ceiling_display = 200 if sc_high_n else 140
        cultivar_note = (
            ' · HoCP14-885 ceiling active'
            if sc_high_n else ''
        )

        # Dark recommendation box with the final N rate in large gold digits
        # {fnr:.0f} formats fnr as a whole number (no decimal places)
        st.markdown(f"""
        <div class="rec-box-sc">
            <div class="rec-label-sc">Fertilizer N Requirement</div>
            <div class="rec-value-sc">{fnr:.0f}</div>
            <div class="rec-unit-sc">lbs N / acre</div>
            <div class="rec-note-sc">
                Bounded 40–{ceiling_display} lb N/ac per LSU AgCenter sugarcane guidelines{cultivar_note}.<br>
                Adjust NUE to reflect fertilizer source, timing, and soil conditions.
            </div>
        </div>
        <div class="formula-box">
            <strong>YP0</strong> &nbsp;= 12.07 × e^(NDVI_FP × 1.47)<br>
            <strong>RI</strong> &nbsp;&nbsp;= (NRS / FP) × 1.94 − 0.91<br>
            <strong>YPN</strong> &nbsp;= YP0 × RI &nbsp;[uncapped for GNUPₙ]<br>
            <strong>GNUP</strong> = Yield × 2000 × %N<br>
            <strong>FNR</strong> &nbsp;&nbsp;= {ceiling_display} if raw &gt; 120, else raw &nbsp;[floor 40]
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RICE CALCULATOR
# Runs only when the Rice tab is active
# ══════════════════════════════════════════════════════════════════════════════
else:

    # Open the blue input panel and render its title label
    st.markdown(
        '<div class="input-panel input-panel-rc">'
        '<div class="input-panel-title input-panel-title-rc">Rice · Input Parameters</div>',
        unsafe_allow_html=True
    )

    # Five equal columns — rice now matches sugarcane's input structure
    i1, i2, i3, i4, i5 = st.columns(5)

    with i1:
        # NDVI of the N-Rich reference strip
        rc_nrs = st.number_input(
            "NDVI — N Rich Strip",
            min_value=0.01, max_value=1.0, value=0.94, step=0.01, format="%.2f",
            key="rc_nrs"
        )

    with i2:
        # NDVI of the farmer's practice field
        rc_fp = st.number_input(
            "NDVI — Farmer's Practice",
            min_value=0.01, max_value=1.0, value=0.94, step=0.01, format="%.2f",
            key="rc_fp"
        )

    with i3:
        # Maximum achievable yield — caps the model output
        rc_yield = st.number_input(
            "Max Yield (bu/ac)",
            min_value=50, max_value=600, value=320,
            key="rc_yield"
        )

    with i4:
        # Nitrogen content of rice grain — default 1.2% per LSU AgCenter
        # Rice grain is measured at dry weight so no moisture correction needed
        rc_pct = st.number_input(
            "Grain N Content (%)",
            min_value=0.50, max_value=3.0, value=1.20, step=0.01, format="%.2f",
            key="rc_pct", help="Default 1.2% — LSU AgCenter rice grain N"
        )

    with i5:
        # Fraction of applied N absorbed by the rice crop
        rc_nue = st.number_input(
            "N Use Efficiency",
            min_value=0.10, max_value=1.0, value=0.75, step=0.05, format="%.2f",
            key="rc_nue"
        )

    # Close the input panel HTML div
    st.markdown('</div>', unsafe_allow_html=True)

    # ── RUN THE ALGORITHM ─────────────────────────────────────────────────────
    # Pass all 5 inputs to the rice function
    yp0, gnup_yp0, ri, ypn, gnup_ypn, fnr = rice_calc(
        rc_fp,      # NDVI farmer's practice
        rc_nrs,     # NDVI N-Rich strip
        rc_yield,   # maximum yield ceiling
        rc_pct,     # grain N content %
        rc_nue      # N use efficiency
    )

    # ── NDVI OVERVIEW ─────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">NDVI Overview</div>', unsafe_allow_html=True)

    ov1, ov2, ov3 = st.columns(3)

    with ov1:
        # Progress bar uses the blue rice fill color
        f = int((rc_nrs - 0.01) / 0.99 * 100)
        st.markdown(f"""
        <div class="d-card">
            <div class="d-card-label">N Rich Strip (NRS)</div>
            <div class="d-card-value">{rc_nrs:.2f}</div>
            <div class="ndvi-track"><div class="ndvi-fill-rc" style="width:{f}%"></div></div>
            <div class="ndvi-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div>
        </div>""", unsafe_allow_html=True)

    with ov2:
        f = int((rc_fp - 0.01) / 0.99 * 100)
        st.markdown(f"""
        <div class="d-card">
            <div class="d-card-label">Farmer's Practice (FP)</div>
            <div class="d-card-value">{rc_fp:.2f}</div>
            <div class="ndvi-track"><div class="ndvi-fill-rc" style="width:{f}%"></div></div>
            <div class="ndvi-ticks"><span>0.0</span><span>0.5</span><span>1.0</span></div>
        </div>""", unsafe_allow_html=True)

    with ov3:
        # Differential uses blue accent color instead of gold
        d = rc_nrs - rc_fp
        dc = "#b84848" if abs(d) > 0.20 else "#c49a28" if abs(d) > 0.10 else "#2a6a9a"
        st.markdown(f"""
        <div class="d-card">
            <div class="d-card-label">NRS − FP Differential</div>
            <div class="d-card-value" style="color:{dc}">{d:+.2f}</div>
            <div class="d-card-sub">NRS is {abs(d):.2f} units {"above" if d >= 0 else "below"} FP</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── MODEL RESULTS ─────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Model Results</div>', unsafe_allow_html=True)

    # Same 3:2 layout as sugarcane
    left, right = st.columns([3, 2], gap="large")

    with left:
        r1, r2 = st.columns(2)
        r3, r4 = st.columns(2)

        with r1:
            # Rice yield is in bu/ac, not ton/ac like sugarcane
            st.markdown(f"""
            <div class="d-card">
                <div class="d-card-label">Yield Potential — No N (YP0)</div>
                <div class="d-card-value">{yp0:.1f}<span class="d-card-unit">bu/ac</span></div>
            </div>""", unsafe_allow_html=True)

        with r2:
            st.markdown(f"""
            <div class="d-card">
                <div class="d-card-label">Yield Potential — With N (YPN)</div>
                <div class="d-card-value">{ypn:.1f}<span class="d-card-unit">bu/ac</span></div>
            </div>""", unsafe_allow_html=True)

        with r3:
            # Rice uses "Grain N Uptake" — N in the harvested grain, not the stalk
            st.markdown(f"""
            <div class="d-card">
                <div class="d-card-label">Grain N Uptake — No N (GNUP₀)</div>
                <div class="d-card-value">{gnup_yp0:.1f}<span class="d-card-unit">lb N/ac</span></div>
            </div>""", unsafe_allow_html=True)

        with r4:
            st.markdown(f"""
            <div class="d-card">
                <div class="d-card-label">Grain N Uptake — With N (GNUPₙ)</div>
                <div class="d-card-value">{gnup_ypn:.1f}<span class="d-card-unit">lb N/ac</span></div>
            </div>""", unsafe_allow_html=True)

        # RI card — shows the rice-specific RI formula in the label
        rp = int(min(max((ri / 2.0) * 100, 0), 100))
        rc_col = "#b84848" if ri > 1.2 else "#c49a28" if ri > 1.0 else "#2a6a9a"
        st.markdown(f"""
        <div class="ri-card">
            <div class="d-card-label">Response Index (RI) &nbsp;·&nbsp;
                <span style="font-family:'DM Mono',monospace;font-size:0.58rem;color:#c0b0a0">
                    ((NRS/FP) × 1.0077 + 0.19727) × 0.94
                </span>
            </div>
            <div class="d-card-value" style="color:{rc_col}">{ri:.4f}</div>
            <div class="ri-track">
                <div class="ri-fill" style="width:{rp}%;background:{rc_col}"></div>
            </div>
            <div class="ndvi-ticks"><span>0.0</span><span>1.0</span><span>2.0</span></div>
        </div>""", unsafe_allow_html=True)

        # Same RI thresholds as sugarcane
        if ri > 1.2:
            ic, im = "interp-high", f"RI of {ri:.3f} indicates a strong crop response to nitrogen. Midseason application is recommended."
        elif ri > 1.0:
            ic, im = "interp-mod", f"RI of {ri:.3f} suggests a moderate response. Evaluate application against economic threshold."
        else:
            ic, im = "interp-low", f"RI of {ri:.3f} indicates low expected response. Midseason nitrogen may not be economically justified."

        st.markdown(f'<div class="interp {ic}">{im}</div>', unsafe_allow_html=True)

    with right:
        # Dark blue recommendation box with the final N rate in large cyan digits
        st.markdown(f"""
        <div class="rec-box-rc">
            <div class="rec-label-rc">Midseason N Requirement</div>
            <div class="rec-value-rc">{fnr:.0f}</div>
            <div class="rec-unit-rc">lbs N / acre</div>
            <div class="rec-note-rc">
                Floored at 0 lb N/ac per LSU AgCenter rice guidelines.<br>
                Adjust NUE for fertilizer source and flood conditions.
            </div>
        </div>
        <div class="formula-box">
            <strong>YP0</strong> &nbsp;= (12088 × NDVI_FP^0.72) ÷ 1.12 ÷ 45<br>
            <strong>RI</strong> &nbsp;&nbsp;= ((NRS/FP) × 1.0077 + 0.19727) × 0.94<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[RI = 2.298 × FP if NRS/FP &gt; 2.099]<br>
            <strong>YPN</strong> &nbsp;= YP0 × RI &nbsp;[capped at max yield]<br>
            <strong>GNUP</strong> = Yield × 45 lbs/bu × %N<br>
            <strong>FNR</strong> &nbsp;&nbsp;= (GNUPₙ − GNUP₀) / NUE &nbsp;[floor 0]
        </div>""", unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
# Attribution on the left, research disclaimer on the right
st.markdown("""
<div class="app-footer">
    <span>LSU AgCenter · Tubana, Johnson & Viator (Sugarcane) · Tubana, Harrell & Walker (Rice)</span>
    <span>For research use only · Not a substitute for professional agronomic advice</span>
</div>
""", unsafe_allow_html=True)
