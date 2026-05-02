import os

DB_PATH = os.getenv("DB_PATH", "app_organizator.db")

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

INITIAL_APPS = [
    {
        "name": "Aging PROWAX i NON PROWAX",
        "description": "Analiza starzenia zapasów PROWAX i NON PROWAX. Identyfikuj wolno rotujące pozycje i poprawiaj decyzje magazynowe.",
        "url": "https://aging-prowax-and-non-prowax-cz4yjz7l8a6dpbiddvwvey.streamlit.app/",
        "active": True,
        "icon": "📦",
    },
    {
        "name": "Anomalie Cenowe",
        "description": "Wykrywanie anomalii cenowych w danych magazynowych. Identyfikuj nietypowe odchylenia cen automatycznie.",
        "url": "",
        "active": True,
        "icon": "📊",
    },
    {
        "name": "BS Mapp",
        "description": "Mapowanie bilansu i rachunku wyników. Narzędzie do analizy struktury finansowej przedsiębiorstwa.",
        "url": "",
        "active": True,
        "icon": "🗺️",
    },
    {
        "name": "Financial Analyzer",
        "description": "Zaawansowana analiza finansowa. Raporty, wskaźniki i wizualizacje danych finansowych.",
        "url": "",
        "active": True,
        "icon": "💹",
    },
    {
        "name": "Inventory App",
        "description": "Zarządzanie zapasami magazynowymi. Kontrola stanów, rotacji i wartości magazynu.",
        "url": "",
        "active": True,
        "icon": "🏭",
    },
    {
        "name": "Inventory App 2",
        "description": "Rozszerzona wersja aplikacji magazynowej z dodatkowymi raportami i funkcjami analitycznymi.",
        "url": "",
        "active": True,
        "icon": "📋",
    },
]

APP_TITLE = "Finance Apps — Interim CFO"
APP_ICON = "💼"
SESSION_TIMEOUT_MINUTES = 60
