
import streamlit as st
from io import BytesIO
import pandas as pd
from src.config.logger import logger
from main import (
    run_search,
    track_price,
    send_price_email
)
if "tracking_result" not in st.session_state:
    st.session_state["tracking_result"] = None
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Daraz Price Tracker",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS — PREMIUM DASHBOARD THEME
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

    :root {
        --bg:        #0b0f19;
        --surface:   rgba(20, 27, 45, 0.72);
        --surface-solid: #141b2d;
        --border:    rgba(255, 255, 255, 0.08);
        --border-hover: rgba(255, 107, 74, 0.45);
        --text:      #f4f6fb;
        --text-muted:#8993a8;
        --accent-1:  #ff6b4a;
        --accent-2:  #ff3d71;
        --mint:      #00d9a3;
        --shadow:    0 20px 50px rgba(0, 0, 0, 0.35);
    }

    * { font-family: 'Inter', sans-serif; }

    h1, h2, h3, .hero h1, .section-title {
        font-family: 'Sora', sans-serif !important;
    }

    /* Static gradient background on the app itself — no pseudo-element,
       no fixed positioning, minimal risk of layout/stacking issues. */
    .stApp {
        background:
            radial-gradient(38% 38% at 15% 20%, rgba(255, 107, 74, 0.16) 0%, transparent 70%),
            radial-gradient(32% 32% at 85% 15%, rgba(255, 61, 113, 0.12) 0%, transparent 70%),
            radial-gradient(45% 45% at 50% 90%, rgba(0, 217, 163, 0.07) 0%, transparent 70%),
            var(--bg);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- Fade-up entrance ---------- */

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .fade-in { animation: fadeUp 0.6s cubic-bezier(0.22, 1, 0.36, 1) both; }
    .fade-in-1 { animation-delay: 0.05s; }
    .fade-in-2 { animation-delay: 0.15s; }
    .fade-in-3 { animation-delay: 0.25s; }

    /* ---------- Header / Hero ---------- */

    .hero {
        background: linear-gradient(135deg, var(--accent-1) 0%, var(--accent-2) 100%);
        padding: 2.75rem 2.75rem 2.5rem;
        border-radius: 26px;
        color: white;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 25px 60px rgba(255, 61, 113, 0.28);
    }

    .hero-top {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        margin-bottom: 0.5rem;
    }

    .pulse-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #00ffb2;
        box-shadow: 0 0 0 0 rgba(0, 255, 178, 0.7);
        animation: pulse 1.8s infinite;
        flex-shrink: 0;
    }

    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(0, 255, 178, 0.6); }
        70%  { box-shadow: 0 0 0 10px rgba(0, 255, 178, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 178, 0); }
    }

    .live-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.92);
        background: rgba(255,255,255,0.16);
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
    }

    .hero h1 {
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.02em;
    }

    .hero p {
        font-size: 1.05rem;
        opacity: 0.94;
        margin-bottom: 0;
        max-width: 640px;
        font-weight: 400;
    }

    /* ---------- Section ---------- */

    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text);
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        letter-spacing: -0.01em;
    }

    /* ---------- Streamlit widget label fix (invisible-text bug) ---------- */

    label, .stTextInput label, .stNumberInput label, .stRadio label,
    div[data-testid="stWidgetLabel"] p {
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.01em;
    }

    /* ---------- Inputs ---------- */

    .stTextInput input, .stNumberInput input {
        background: var(--surface-solid) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.95rem !important;
        transition: all 0.25s ease;
        padding: 0.7rem 0.9rem !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: var(--accent-1) !important;
        box-shadow: 0 0 0 4px rgba(255, 107, 74, 0.15) !important;
    }

    .stTextInput input::placeholder {
        color: #4d566e !important;
    }

    .stNumberInput button {
        background: var(--surface-solid) !important;
        border: 1.5px solid var(--border) !important;
        color: var(--text) !important;
        transition: all 0.2s ease;
    }

    .stNumberInput button:hover {
        border-color: var(--accent-1) !important;
        color: var(--accent-1) !important;
    }

    /* ---------- Radio buttons ---------- */

    .stRadio [role="radiogroup"] label {
        background: var(--surface-solid);
        border: 1.5px solid var(--border);
        border-radius: 12px;
        padding: 0.55rem 1rem !important;
        margin-right: 0.6rem;
        transition: all 0.22s ease;
        cursor: pointer;
    }

    .stRadio [role="radiogroup"] label:hover {
        border-color: var(--border-hover);
        transform: translateY(-1px);
    }

    .stRadio [role="radiogroup"] p {
        color: var(--text) !important;
        font-weight: 500 !important;
    }

    /* ---------- Metric Cards ---------- */

    .metric-card {
        background: var(--surface);
        backdrop-filter: blur(14px);
        padding: 1.35rem;
        border-radius: 18px;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        text-align: center;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        border-color: var(--border-hover);
    }

    .metric-label {
        color: var(--text-muted);
        font-size: 0.82rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-value {
        color: var(--text);
        font-size: 1.75rem;
        font-weight: 700;
        margin-top: 0.3rem;
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ---------- Result Box ---------- */

    .result-box {
        background: var(--surface);
        backdrop-filter: blur(14px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.6rem 1.8rem;
        margin-top: 1.5rem;
        box-shadow: var(--shadow);
        color: var(--text);
    }

    .result-box h3 {
        margin-top: 0;
        font-size: 1.1rem;
        color: var(--text);
    }

    .result-box p {
        color: var(--text-muted);
        margin-bottom: 0;
        line-height: 1.5;
    }

    /* ---------- Skeleton shimmer ---------- */

    .skeleton {
        border-radius: 14px;
        background: linear-gradient(
            100deg,
            rgba(255,255,255,0.04) 30%,
            rgba(255,255,255,0.10) 50%,
            rgba(255,255,255,0.04) 70%
        );
        background-size: 200% 100%;
        animation: shimmer 1.3s ease-in-out infinite;
        border: 1px solid var(--border);
    }

    @keyframes shimmer {
        0%   { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    .skeleton-card { height: 88px; margin-bottom: 0; }
    .skeleton-block { height: 110px; margin-top: 1.5rem; }

    /* ---------- Buttons ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
        font-family: 'Sora', sans-serif;
        min-height: 46px;
        border: none;
        transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1);
        letter-spacing: 0.01em;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent-1), var(--accent-2)) !important;
        color: white !important;
        box-shadow: 0 10px 26px rgba(255, 61, 113, 0.3);
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 34px rgba(255, 61, 113, 0.45);
        filter: brightness(1.06);
    }

    .stButton > button[kind="primary"]:active {
        transform: translateY(0px) scale(0.98);
    }

    .stButton > button:not([kind="primary"]) {
        background: var(--surface-solid) !important;
        color: var(--text) !important;
        border: 1.5px solid var(--border) !important;
    }

    .stButton > button:not([kind="primary"]):hover:not(:disabled) {
        border-color: var(--border-hover) !important;
        color: var(--accent-1) !important;
        transform: translateY(-2px);
    }

    .stButton > button:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }

    /* ---------- Alerts restyle to match theme ---------- */

    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid var(--border);
        backdrop-filter: blur(10px);
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.85rem;
        margin-top: 3.5rem;
        letter-spacing: 0.02em;
    }

    .footer::before {
        content: "";
        display: block;
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
        margin: 0 auto 1rem;
        border-radius: 2px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero fade-in">
        <div class="hero-top">
            <span class="pulse-dot"></span>
            <span class="live-tag">Live Monitoring</span>
        </div>
        <h1>🛒 Daraz Price Tracker</h1>
        <p>
            Search products, filter by price and brand,
            generate reports, and track price changes.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SEARCH CONFIGURATION
# ============================================================

st.markdown(
    '<div class="section-title fade-in fade-in-1">🔎 Product Search</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input(
        "Product Name",
        placeholder="e.g. Laptop",
    )

with col2:
    target_price = st.number_input(
        "Target Price (PKR)",
        min_value=0,
        value=50000,
        step=1000,
    )


# ============================================================
# PRICE CONDITION
# ============================================================

condition = st.radio(
    "Price Condition",
    options=[
        "Below Target Price",
        "Above Target Price",
    ],
    horizontal=True,
)


# ============================================================
# BRAND
# ============================================================

brand = st.text_input(
    "Target Brand (optional)",
    placeholder="e.g. HP, Dell, Lenovo",
)


# ============================================================
# SEARCH BUTTON
# ============================================================

st.markdown("")

search_clicked = st.button(
    "🔎 Search Products",
    type="primary",
)


# ============================================================
# SEARCH RESULT STATE (with skeleton loading)
# ============================================================

if search_clicked:

    if not product_name.strip():
        st.warning("⚠️ Please enter a product name.")

    elif target_price <= 0:
        st.warning("⚠️ Please enter a valid target price.")

    

    else:
        skeleton_slot = st.empty()

        with skeleton_slot.container():
            st.markdown(
                """
                <div style="display:flex; gap:1rem; margin-top:0.5rem;">
                    <div class="skeleton skeleton-card" style="flex:1;"></div>
                    <div class="skeleton skeleton-card" style="flex:1;"></div>
                    <div class="skeleton skeleton-card" style="flex:1;"></div>
                </div>
                <div class="skeleton skeleton-block"></div>
                """,
                unsafe_allow_html=True,
            )

        with st.spinner(
            f"Searching Daraz for **{product_name}**..."
            ):

            try:

                result = run_search(
                product_name=product_name,
                target_price=target_price,
                condition=condition,
                brand=brand,
                )

                st.session_state["search_completed"] = True
                st.session_state["search_result"] = result
                st.session_state["filtered_products"] = (
                    result["products"]
                )
                st.session_state["tracking_result"] = None

                st.success(
                    f"Search completed successfully for "
                    f"**{product_name}**."
                )

            except Exception as e:

                st.session_state["search_completed"] = False

                st.error(
                f"❌ Scraping failed: {e}"
                )


# ============================================================
# RESULTS SECTION
# ============================================================
result = st.session_state.get(
    "search_result",
    {}
)

products_found = result.get(
    "products_found",
    0
)

filtered_count = result.get(
    "filtered_count",
    0
)

if st.session_state.get("search_completed", False):

    st.markdown(
        '<div class="section-title fade-in">📊 Search Results</div>',
        unsafe_allow_html=True,
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.markdown(
            f"""
            <div class="metric-card fade-in fade-in-1">
                <div class="metric-label">Products Found</div>
                <div class="metric-value">{products_found}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric2:
        st.markdown(
            f"""
            <div class="metric-card fade-in fade-in-2">
                <div class="metric-label">Price Matched</div>
                <div class="metric-value">{filtered_count}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric3:
        st.markdown(
            f"""
            <div class="metric-card fade-in fade-in-3">
                <div class="metric-label">Brand Matched</div>
                <div class="metric-value">{filtered_count}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
# --------------------------------------------------------
# REPORT
# --------------------------------------------------------

filtered_products = st.session_state.get(
    "filtered_products",
    []
)

st.markdown(
    f"""
    <div class="result-box fade-in fade-in-2">
        <h3>📄 Product Report</h3>
        <p>
            {
                f"{len(filtered_products)} filtered products found."
                if filtered_products
                else "No products matched your selected criteria."
            }
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------
# PRODUCT TABLE
# --------------------------------------------------------

if filtered_products:

    report_df = pd.DataFrame(
        filtered_products
    )

    st.dataframe(
        report_df,
        use_container_width=True,
        hide_index=True,
    )

# --------------------------------------------------------
# REPORT ACTIONS
# --------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    if filtered_products:

        excel_buffer = BytesIO()

        report_df.to_excel(
            excel_buffer,
            index=False,
            engine="openpyxl",
        )

        excel_buffer.seek(0)

        st.download_button(
            "📊 Download Excel Report",
            data=excel_buffer.getvalue(),
            file_name="daraz_filtered_products.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            use_container_width=True,
        )

    else:

        st.button(
            "📊 Download Excel Report",
            disabled=True,
            use_container_width=True,
        )

with col2:

    track_clicked = st.button(
        "📈 Track Price",
        disabled=not bool(filtered_products),
        use_container_width=True,
    )
    # ========================================================
# TRACKING SECTION
# ========================================================

# ============================================================
# TRACK PRICE
# ============================================================

if track_clicked:

    # --------------------------------------------------------
    # TRACKING LOADER
    # --------------------------------------------------------

    track_skeleton = st.empty()

    with track_skeleton.container():

        st.markdown(
            '<div class="skeleton skeleton-block" '
            'style="margin-top:1rem;"></div>',
            unsafe_allow_html=True,
        )

    with st.spinner("Comparing product prices..."):

        try:

            # ------------------------------------------------
            # CURRENT FILTERED PRODUCTS
            # ------------------------------------------------

            filtered_products = st.session_state.get(
                "filtered_products",
                []
            )

            # ------------------------------------------------
            # PRICE TRACKER
            # ------------------------------------------------

            tracking_result = track_price(
                filtered_products=filtered_products
            )

            # ------------------------------------------------
            # SAVE TRACKING RESULT
            # ------------------------------------------------

            st.session_state["tracking_result"] = (
                tracking_result
            )

            st.session_state["tracking_done"] = True

            logger.info(
                "Tracking result saved successfully."
            )

        except Exception as e:

            logger.error(
                f"Price tracking failed | {e}"
            )

            st.session_state["tracking_result"] = None
            st.session_state["tracking_done"] = False

            st.error(
                f"❌ Price tracking failed: {e}"
            )

    track_skeleton.empty()


# ============================================================
# GET PERSISTENT TRACKING RESULT
# ============================================================

tracking_result = st.session_state.get(
    "tracking_result",
    None
)

tracking_done = st.session_state.get(
    "tracking_done",
    False
)


# ============================================================
# PRICE TRACKING SECTION
# ============================================================

if tracking_done and tracking_result:

    # --------------------------------------------------------
    # PRICE TRACKING TITLE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title fade-in">'
        '📈 Price Tracking</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # TRACKING STATUS
    # --------------------------------------------------------

    status = tracking_result.get(
        "status",
        "unknown"
    )

    # ========================================================
    # FIRST RUN
    # ========================================================

    if status == "first_run":

        st.info(
            "🗂️ Initial price snapshot created. "
            "Run tracking again later to detect "
            "price changes."
        )

        st.markdown(
            """
            <div class="result-box fade-in fade-in-1">
                <h3>🔍 Tracking Status</h3>
                <p>
                    This is the first tracking run.
                    Current filtered products have been
                    saved as the initial snapshot.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # PRICE DROP FOUND
    # ========================================================

    elif status == "price_drop":

        price_drops = tracking_result.get(
            "price_drops",
            []
        )

        st.success(
            f"📉 {len(price_drops)} "
            "price drop(s) detected!"
        )

        st.markdown(
            """
            <div class="result-box fade-in fade-in-1">
                <h3>🔍 Tracking Status</h3>
                <p>
                    Products with reduced prices
                    compared with the previous snapshot.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # DROPPED PRODUCTS TABLE
        # ----------------------------------------------------

        if price_drops:

            dropped_df = pd.DataFrame(
                price_drops
            )

            st.dataframe(
                dropped_df,
                use_container_width=True,
                hide_index=True,
            )

    # ========================================================
    # NO PRICE DROP
    # ========================================================

    elif status == "no_drop":

        st.info(
            "📊 No price drop detected."
        )

        st.markdown(
            """
            <div class="result-box fade-in fade-in-1">
                <h3>🔍 Tracking Status</h3>
                <p>
                    Previous and current product prices
                    were compared successfully.
                    No product price has decreased.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # NO PRODUCTS
    # ========================================================

    elif status == "empty":

        st.warning(
            "⚠️ No filtered products available "
            "for tracking."
        )

        st.markdown(
            """
            <div class="result-box fade-in fade-in-1">
                <h3>🔍 Tracking Status</h3>
                <p>
                    No products were found matching
                    your selected brand and price criteria.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # UNKNOWN STATUS
    # ========================================================

    else:

        st.warning(
            f"⚠️ Unknown tracking status: {status}"
        )


# ============================================================
# EMAIL SECTION
# ============================================================

if tracking_done and tracking_result:

    st.markdown(
        '<div class="section-title fade-in fade-in-2">'
        '📧 Email Report</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # EMAIL INPUT
    # --------------------------------------------------------

    email = st.text_input(
        "Email Address",
        placeholder="example@gmail.com",
        key="target_email",
    )

    # --------------------------------------------------------
    # PRICE DROP DATA
    # --------------------------------------------------------

    price_drops = tracking_result.get(
        "price_drops",
        []
    )

    # --------------------------------------------------------
    # SEND EMAIL BUTTON
    # --------------------------------------------------------

    send_email_clicked = st.button(
        "📧 Send Email",
        disabled=False,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # SEND EMAIL
    # --------------------------------------------------------

    if send_email_clicked:

        if not email.strip():

            st.warning(
                "⚠️ Please enter your email address."
            )

        else:

            try:

                with st.spinner(
                    "Sending email..."
                ):

                    email_result = send_price_email(
                        tracked_products=price_drops,
                        target_email=email.strip(),
                    )

                # --------------------------------------------
                # EMAIL SUCCESS
                # --------------------------------------------

                if (
                    email_result
                    and email_result.get("status")
                    == "sent"
                ):

                    st.success(
                        "📧 Email sent successfully!"
                    )

                # --------------------------------------------
                # EMAIL OTHER RESULT
                # --------------------------------------------

                else:

                    st.info(
                        email_result.get(
                            "message",
                            "Email process completed."
                        )
                        if email_result
                        else
                        "Email process completed."
                    )

            except Exception as e:

                logger.exception(
                    "Email sending failed."
                )

                st.error(
                    f"❌ Failed to send email: {e}"
                )
# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Daraz Price Tracker • Automated Product Monitoring System
    </div>
    """,
    unsafe_allow_html=True,
)