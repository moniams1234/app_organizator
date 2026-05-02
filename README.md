# 💼 Finance Apps — App Organizator

Ciemny, bordowy panel zarządzania aplikacjami Streamlit w stylu **Interim CFO / Finance Apps**.

---

## 🚀 Uruchomienie

```bash
# 1. Zainstaluj zależności
pip install -r requirements.txt

# 2. Uruchom aplikację
streamlit run app.py
```

Aplikacja automatycznie tworzy bazę SQLite i konto admina przy pierwszym uruchomieniu.

---

## 🔐 Domyślne dane logowania

| Login | Hasło    | Rola  |
|-------|----------|-------|
| admin | admin123 | admin |

> ⚠️ Zmień hasło admina po pierwszym zalogowaniu!

---

## 📁 Struktura projektu

```
app_organizator/
├── app.py          # Główna aplikacja Streamlit
├── database.py     # Obsługa SQLite (CRUD)
├── auth.py         # Logowanie, bcrypt, sesje
├── config.py       # Konfiguracja i dane startowe
├── requirements.txt
└── README.md
```

---

## 👤 Role użytkowników

- **admin** — pełny dostęp: zarządzanie aplikacjami, użytkownikami i przypisaniami
- **user** — widzi tylko aplikacje, do których ma dostęp

---

## ⚙️ Funkcje

### Panel użytkownika
- Kafelki aplikacji w gridzie 3-kolumnowym
- Wyszukiwarka aplikacji
- Przycisk „Otwórz aplikację" otwierający w nowej karcie
- Automatyczne „rozbudzenie" aplikacji przez `requests.get()` przed otwarciem
- Ostrzeżenie gdy URL nie jest skonfigurowany

### Panel administratora
- **Aplikacje** — dodawanie, edycja, usuwanie/dezaktywacja
- **Użytkownicy** — tworzenie, zmiana hasła, aktywacja/dezaktywacja, usuwanie
- **Przypisania** — multi-select aplikacji per użytkownik

---

## 🎨 Styl

- Ciemny bordowy gradient (`#2A0000 → #120000`)
- Sidebar: `#1A0000 → #080000`
- Nazwy aplikacji: niebieski akcent `#4DA8E0`
- Ikony: czerwono-pomarańczowy gradient
- Przyciski: granatowy `#173A6A → #1E5F9E`
- Inspiracja: strona **Interim CFO / Finance Apps**

---

## 🗄️ Baza danych

SQLite `app_organizator.db` — 3 tabele:

| Tabela      | Opis                        |
|-------------|-----------------------------|
| `users`     | Użytkownicy + hashe bcrypt  |
| `apps`      | Aplikacje Streamlit          |
| `user_apps` | Relacja user ↔ app           |

Zmień lokalizację bazy przez zmienną środowiskową:
```bash
export DB_PATH=/ścieżka/do/bazy.db
```
