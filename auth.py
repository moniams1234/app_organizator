import bcrypt
import streamlit as st
from database import get_user


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def login(username: str, password: str):
    """Attempt login. Returns (user_dict, error_str)."""
    user = get_user(username)
    if not user:
        return None, "Nieprawidłowy login lub hasło."
    if not user["active"]:
        return None, "Konto jest nieaktywne. Skontaktuj się z administratorem."
    if not verify_password(password, user["password_hash"]):
        return None, "Nieprawidłowy login lub hasło."
    return user, None


def logout():
    for key in ["user", "logged_in"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


def require_login():
    return st.session_state.get("logged_in", False)


def is_admin():
    user = st.session_state.get("user")
    return user and user.get("role") == "admin"
