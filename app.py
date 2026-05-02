import streamlit as st
import requests
import time
from config import APP_TITLE, APP_ICON
from database import (
    init_db, get_apps_for_user, get_all_apps, get_all_users,
    create_app, update_app, delete_app,
    create_user, update_user_password, toggle_user_active, delete_user,
    get_user_app_ids, set_user_apps,
)
from auth import login, logout, is_admin

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;600;700&display=swap');

/* ── ROOT VARIABLES ── */
:root {
    --bg-main:       #1A0000;
    --bg-sidebar:    #0E0000;
    --bg-card:       rgba(255,255,255,0.04);
    --bg-card-hover: rgba(255,255,255,0.07);
    --border-card:   rgba(255,255,255,0.08);
    --accent-red:    #C1121F;
    --accent-blue:   #1E6CB0;
    --accent-blue2:  #2B7FD4;
    --text-primary:  #FFFFFF;
    --text-secondary:#C8C8C8;
    --text-muted:    #8A8A8A;
    --green:         #22C55E;
    --red:           #EF4444;
    --orange:        #F97316;
    --font:          'Barlow', sans-serif;
    --font-cond:     'Barlow Condensed', sans-serif;
}

/* ── BASE ── */
html, body, [data-testid="stApp"] {
    background: linear-gradient(160deg, #2A0000 0%, #1A0000 40%, #120000 100%) !important;
    font-family: var(--font) !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A0000 0%, #0E0000 60%, #080000 100%) !important;
    border-right: 1px solid rgba(193,18,31,0.25) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-secondary) !important;
    font-family: var(--font) !important;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: transparent !important;
    border: 1px solid rgba(193,18,31,0.4) !important;
    color: var(--text-secondary) !important;
    border-radius: 6px;
    font-size: 0.85rem;
    padding: 0.45rem 0.8rem;
    margin-top: 0.3rem;
    transition: all 0.2s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(193,18,31,0.2) !important;
    border-color: var(--accent-red) !important;
    color: #fff !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── MAIN CONTENT AREA ── */
.main .block-container {
    padding: 1.5rem 2.5rem 2rem 2.5rem !important;
    max-width: 1400px;
}

/* ── HEADER BANNER ── */
.page-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.2rem 1.8rem;
    background: linear-gradient(135deg, #2A0000 0%, #1A0000 100%);
    border: 1px solid rgba(193,18,31,0.3);
    border-radius: 12px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5);
}
.page-header-logo {
    width: 52px;
    height: 52px;
    background: linear-gradient(135deg, #C1121F, #8B0000);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    flex-shrink: 0;
}
.page-header-title {
    font-family: var(--font-cond);
    font-size: 1.7rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: 0.04em;
    line-height: 1.15;
}
.page-header-sub {
    font-size: 0.85rem;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── SEARCH BAR ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-family: var(--font) !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 2px rgba(30,108,176,0.25) !important;
}
.stTextInput > label {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em;
}

/* ── APP CARD GRID ── */
.app-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.2rem;
    margin-top: 0.5rem;
}
@media (max-width: 1100px) { .app-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 700px)  { .app-grid { grid-template-columns: 1fr; } }

.app-card {
    background: linear-gradient(160deg, rgba(60,5,5,0.65) 0%, rgba(25,2,2,0.85) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.4rem 1.3rem 1.1rem;
    transition: all 0.25s ease;
    box-shadow: 0 2px 16px rgba(0,0,0,0.45);
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    position: relative;
    overflow: hidden;
}
.app-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #C1121F 0%, #F97316 100%);
    opacity: 0.6;
    border-radius: 14px 14px 0 0;
}
.app-card:hover {
    background: linear-gradient(160deg, rgba(80,8,8,0.75) 0%, rgba(35,3,3,0.9) 100%);
    border-color: rgba(193,18,31,0.35);
    box-shadow: 0 6px 28px rgba(0,0,0,0.6);
    transform: translateY(-2px);
}

.app-card-top {
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
}
.app-icon {
    width: 52px;
    height: 52px;
    border-radius: 10px;
    background: linear-gradient(135deg, #C1121F 0%, #F97316 60%, #FF6B00 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
    box-shadow: 0 3px 10px rgba(193,18,31,0.4);
}
.app-card-info { flex: 1; min-width: 0; }
.app-name {
    font-family: var(--font-cond);
    font-size: 1.05rem;
    font-weight: 700;
    color: #4DA8E0;
    letter-spacing: 0.02em;
    line-height: 1.2;
    margin-bottom: 0.25rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.app-desc {
    font-size: 0.78rem;
    color: var(--text-muted);
    line-height: 1.45;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.app-url-badge {
    font-size: 0.7rem;
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    display: inline-block;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.url-set   { background: rgba(34,197,94,0.15); color: var(--green); border: 1px solid rgba(34,197,94,0.3); }
.url-unset { background: rgba(239,68,68,0.12); color: var(--red);   border: 1px solid rgba(239,68,68,0.25); }

/* ── OPEN BUTTON ── */
.open-btn-wrap { margin-top: 0.4rem; }
.open-btn-wrap .stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #173A6A 0%, #1E5F9E 100%) !important;
    border: 1px solid rgba(30,108,176,0.5) !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-family: var(--font) !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 1rem !important;
    letter-spacing: 0.04em;
    transition: all 0.2s !important;
    text-transform: uppercase;
}
.open-btn-wrap .stButton > button:hover {
    background: linear-gradient(135deg, #1E4F8F 0%, #2B7FD4 100%) !important;
    border-color: var(--accent-blue2) !important;
    box-shadow: 0 3px 14px rgba(30,108,176,0.45) !important;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: var(--font-cond);
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 1.2rem 0 0.7rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}

/* ── ADMIN TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 8px;
    padding: 0.25rem;
    gap: 0.25rem;
    border: 1px solid rgba(255,255,255,0.07);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: var(--font) !important;
    font-size: 0.85rem !important;
    border-radius: 6px !important;
    padding: 0.4rem 1rem !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2A0000, #1A0000) !important;
    color: #fff !important;
    border: 1px solid rgba(193,18,31,0.4) !important;
}

/* ── FORMS ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #fff !important;
}
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-family: var(--font) !important;
}
.stCheckbox > label { color: var(--text-secondary) !important; }
.stForm { 
    background: rgba(255,255,255,0.03) !important; 
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}

/* ── PRIMARY BUTTONS ── */
.stButton > button[kind="primary"],
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #173A6A 0%, #1E5F9E 100%) !important;
    border: 1px solid rgba(30,108,176,0.5) !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-family: var(--font) !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #1E4F8F 0%, #2B7FD4 100%) !important;
}

/* ── DATAFRAME ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }
[data-testid="stDataFrameContainer"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px;
}

/* ── ALERTS ── */
.stSuccess { background: rgba(34,197,94,0.1) !important; border-color: rgba(34,197,94,0.35) !important; color: #86efac !important; border-radius: 8px !important; }
.stError   { background: rgba(239,68,68,0.1) !important; border-color: rgba(239,68,68,0.3) !important;  color: #fca5a5 !important; border-radius: 8px !important; }
.stWarning { background: rgba(249,115,22,0.1) !important; border-color: rgba(249,115,22,0.3) !important; color: #fdba74 !important; border-radius: 8px !important; }
.stInfo    { background: rgba(30,108,176,0.1) !important; border-color: rgba(30,108,176,0.3) !important; color: #93c5fd !important; border-radius: 8px !important; }

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── METRIC ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px;
    padding: 1rem !important;
}
[data-testid="metric-container"] label { color: var(--text-muted) !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #fff !important; }

/* ── SIDEBAR USER BADGE ── */
.user-badge {
    background: linear-gradient(135deg, rgba(193,18,31,0.2), rgba(139,0,0,0.15));
    border: 1px solid rgba(193,18,31,0.35);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 1rem;
    text-align: center;
}
.user-badge-name {
    font-family: var(--font-cond);
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: 0.04em;
}
.user-badge-role {
    font-size: 0.72rem;
    color: var(--accent-red);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}

/* ── NO URL MESSAGE ── */
.no-url-msg {
    font-size: 0.75rem;
    color: var(--red);
    text-align: center;
    padding: 0.3rem 0;
    opacity: 0.8;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-family: var(--font) !important;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ── LOGIN SCREEN ─────────────────────────────────────────────────────────────

def render_login():
    st.markdown("""
    <style>
    .login-outer {
        display: flex; align-items: center; justify-content: center;
        min-height: 80vh; flex-direction: column;
    }
    .login-box {
        background: linear-gradient(160deg, rgba(50,5,5,0.7) 0%, rgba(18,0,0,0.9) 100%);
        border: 1px solid rgba(193,18,31,0.3);
        border-radius: 18px;
        padding: 2.5rem 2rem;
        width: 360px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.6);
        text-align: center;
    }
    .login-logo {
        width: 70px; height: 70px;
        background: linear-gradient(135deg, #C1121F, #8B0000);
        border-radius: 16px;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 2rem; margin-bottom: 1rem;
        box-shadow: 0 4px 18px rgba(193,18,31,0.45);
    }
    .login-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.6rem; font-weight: 700; color: #fff;
        letter-spacing: 0.04em; margin-bottom: 0.2rem;
    }
    .login-sub { font-size: 0.8rem; color: #888; margin-bottom: 1.5rem; letter-spacing: 0.05em; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; margin: 3rem 0 1.5rem;">
            <div class="login-logo">💼</div>
            <div class="login-title">Finance Apps</div>
            <div class="login-sub">INTERIM CFO — PANEL ZARZĄDZANIA</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Login", placeholder="Wprowadź login")
            password = st.text_input("Hasło", type="password", placeholder="Wprowadź hasło")
            submitted = st.form_submit_button("🔐  Zaloguj się", use_container_width=True)

        if submitted:
            user, err = login(username, password)
            if err:
                st.error(err)
            else:
                st.session_state["user"] = user
                st.session_state["logged_in"] = True
                st.rerun()


# ── SIDEBAR ──────────────────────────────────────────────────────────────────

def render_sidebar():
    user = st.session_state["user"]
    with st.sidebar:
        st.markdown(f"""
        <div class="user-badge">
            <div style="font-size:1.8rem; margin-bottom:0.3rem;">👤</div>
            <div class="user-badge-name">{user['username']}</div>
            <div class="user-badge-role">{'Administrator' if user['role'] == 'admin' else 'Użytkownik'}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">Nawigacja</div>', unsafe_allow_html=True)
        st.markdown("**📱 Finance Apps Portal**")
        st.caption("Panel aplikacji finansowych")

        st.markdown("---")
        if st.button("🚪 Wyloguj się", key="logout_btn"):
            logout()


# ── USER DASHBOARD ────────────────────────────────────────────────────────────

def wake_app(url: str) -> bool:
    try:
        requests.get(url, timeout=10)
        return True
    except Exception:
        return False


def render_user_dashboard():
    user = st.session_state["user"]
    apps = get_apps_for_user(user["id"])

    # Header
    st.markdown("""
    <div class="page-header">
        <div class="page-header-logo">💼</div>
        <div>
            <div class="page-header-title">Finance Apps Portal</div>
            <div class="page-header-sub">Interim CFO — Twoje aplikacje finansowe</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Search
    search = st.text_input("", placeholder="🔍  Szukaj aplikacji...", key="search_apps", label_visibility="collapsed")

    if search:
        apps = [a for a in apps if search.lower() in a["name"].lower() or search.lower() in (a["description"] or "").lower()]

    if not apps:
        st.info("Brak dostępnych aplikacji. Skontaktuj się z administratorem.")
        return

    st.markdown(f'<div class="section-title">Dostępne aplikacje — {len(apps)}</div>', unsafe_allow_html=True)

    # Grid — 3 columns
    cols = st.columns(3)
    for idx, app in enumerate(apps):
        col = cols[idx % 3]
        with col:
            url_set = bool(app.get("url", "").strip())
            url_badge = (
                '<span class="app-url-badge url-set">● Dostępna</span>'
                if url_set else
                '<span class="app-url-badge url-unset">● Brak URL</span>'
            )
            st.markdown(f"""
            <div class="app-card">
                <div class="app-card-top">
                    <div class="app-icon">{app.get('icon','📱')}</div>
                    <div class="app-card-info">
                        <div class="app-name">{app['name']}</div>
                        <div class="app-desc">{app.get('description','')}</div>
                    </div>
                </div>
                {url_badge}
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="open-btn-wrap">', unsafe_allow_html=True)
            if url_set:
                btn_key = f"open_{app['id']}"
                if st.button("▶  Otwórz aplikację", key=btn_key, use_container_width=True):
                    with st.spinner("Rozbudzam aplikację..."):
                        ok = wake_app(app["url"])
                    if not ok:
                        st.warning(f"⚠️ Nie udało się połączyć z {app['name']}, ale możesz spróbować otworzyć ją ręcznie.")
                    st.markdown(
                        f'<script>window.open("{app["url"]}", "_blank");</script>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'**[→ Kliknij tutaj, aby otworzyć {app["name"]}]({app["url"]})**'
                    )
            else:
                st.button("⚙️  URL nie skonfigurowany", key=f"nourl_{app['id']}", use_container_width=True, disabled=True)
            st.markdown("</div>", unsafe_allow_html=True)


# ── ADMIN PANEL ───────────────────────────────────────────────────────────────

def render_admin_panel():
    st.markdown('<div class="section-title">Panel Administratora</div>', unsafe_allow_html=True)

    tab_apps, tab_users, tab_assign = st.tabs(["📱 Aplikacje", "👥 Użytkownicy", "🔗 Przypisania"])

    # ── TAB: APPS ──
    with tab_apps:
        st.markdown('<div class="section-title">Dodaj nową aplikację</div>', unsafe_allow_html=True)
        with st.form("add_app_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Nazwa aplikacji *")
                new_url  = st.text_input("URL aplikacji")
            with col2:
                new_icon = st.text_input("Ikona (emoji)", value="📱")
                new_active = st.checkbox("Aktywna", value=True)
            new_desc = st.text_area("Opis", height=80)
            if st.form_submit_button("➕ Dodaj aplikację", use_container_width=True):
                if not new_name.strip():
                    st.error("Nazwa aplikacji jest wymagana.")
                else:
                    create_app(new_name.strip(), new_desc.strip(), new_url.strip(), new_icon.strip() or "📱", new_active)
                    st.success(f"✅ Aplikacja '{new_name}' została dodana.")
                    st.rerun()

        st.markdown('<div class="section-title">Wszystkie aplikacje</div>', unsafe_allow_html=True)
        all_apps = get_all_apps()
        if not all_apps:
            st.info("Brak aplikacji w bazie.")
        else:
            for app in all_apps:
                with st.expander(f"{'✅' if app['active'] else '❌'} {app['icon']}  {app['name']} — {'aktywna' if app['active'] else 'nieaktywna'}"):
                    with st.form(f"edit_app_{app['id']}"):
                        c1, c2 = st.columns(2)
                        with c1:
                            e_name   = st.text_input("Nazwa", value=app["name"])
                            e_url    = st.text_input("URL",   value=app.get("url",""))
                        with c2:
                            e_icon   = st.text_input("Ikona", value=app.get("icon","📱"))
                            e_active = st.checkbox("Aktywna", value=bool(app["active"]))
                        e_desc = st.text_area("Opis", value=app.get("description",""), height=80)
                        bc1, bc2 = st.columns(2)
                        with bc1:
                            if st.form_submit_button("💾 Zapisz zmiany", use_container_width=True):
                                update_app(app["id"], e_name, e_desc, e_url, e_icon, e_active)
                                st.success("✅ Zapisano zmiany.")
                                st.rerun()
                        with bc2:
                            if st.form_submit_button("🗑️ Usuń aplikację", use_container_width=True):
                                delete_app(app["id"])
                                st.success("🗑️ Aplikacja usunięta.")
                                st.rerun()

    # ── TAB: USERS ──
    with tab_users:
        st.markdown('<div class="section-title">Utwórz nowego użytkownika</div>', unsafe_allow_html=True)
        with st.form("add_user_form"):
            cu1, cu2, cu3 = st.columns(3)
            with cu1: new_uname = st.text_input("Login *")
            with cu2: new_upass = st.text_input("Hasło *", type="password")
            with cu3: new_urole = st.selectbox("Rola", ["user", "admin"])
            if st.form_submit_button("➕ Utwórz użytkownika", use_container_width=True):
                if not new_uname.strip() or not new_upass.strip():
                    st.error("Login i hasło są wymagane.")
                else:
                    uid, err = create_user(new_uname.strip(), new_upass.strip(), new_urole)
                    if err:
                        st.error(err)
                    else:
                        st.success(f"✅ Użytkownik '{new_uname}' utworzony.")
                        st.rerun()

        st.markdown('<div class="section-title">Wszyscy użytkownicy</div>', unsafe_allow_html=True)
        all_users = get_all_users()
        current_user = st.session_state["user"]

        for u in all_users:
            is_self = u["id"] == current_user["id"]
            label   = f"{'✅' if u['active'] else '❌'} {u['username']} ({u['role']})"
            with st.expander(label):
                uc1, uc2, uc3 = st.columns(3)
                with uc1:
                    with st.form(f"pwd_form_{u['id']}"):
                        np = st.text_input("Nowe hasło", type="password", key=f"np_{u['id']}")
                        if st.form_submit_button("🔑 Zmień hasło"):
                            if np.strip():
                                update_user_password(u["id"], np.strip())
                                st.success("✅ Hasło zmienione.")
                            else:
                                st.error("Hasło nie może być puste.")
                with uc2:
                    if not is_self:
                        label_toggle = "🔴 Dezaktywuj" if u["active"] else "🟢 Aktywuj"
                        if st.button(label_toggle, key=f"toggle_{u['id']}"):
                            toggle_user_active(u["id"], not bool(u["active"]))
                            st.rerun()
                    else:
                        st.caption("(to Twoje konto)")
                with uc3:
                    if not is_self:
                        if st.button("🗑️ Usuń", key=f"del_user_{u['id']}"):
                            delete_user(u["id"])
                            st.rerun()

    # ── TAB: ASSIGNMENTS ──
    with tab_assign:
        st.markdown('<div class="section-title">Przypisz aplikacje użytkownikom</div>', unsafe_allow_html=True)
        all_users = get_all_users()
        all_apps  = get_all_apps()
        app_names = {a["id"]: a["name"] for a in all_apps}

        sel_user = st.selectbox("Wybierz użytkownika", options=all_users,
                                format_func=lambda u: f"{u['username']} ({u['role']})",
                                key="assign_user")

        if sel_user:
            current_ids = get_user_app_ids(sel_user["id"])
            with st.form("assign_form"):
                selected = st.multiselect(
                    "Aplikacje dostępne dla użytkownika",
                    options=[a["id"] for a in all_apps],
                    default=current_ids,
                    format_func=lambda aid: f"{app_names.get(aid,'?')}",
                )
                if st.form_submit_button("💾 Zapisz przypisania", use_container_width=True):
                    set_user_apps(sel_user["id"], selected)
                    st.success(f"✅ Przypisania dla '{sel_user['username']}' zapisane.")
                    st.rerun()


# ── MAIN FLOW ─────────────────────────────────────────────────────────────────

def main():
    if not st.session_state.get("logged_in"):
        render_login()
        return

    render_sidebar()

    user = st.session_state["user"]

    if user["role"] == "admin":
        render_user_dashboard()
        st.markdown("---")
        render_admin_panel()
    else:
        render_user_dashboard()


if __name__ == "__main__":
    main()
