import os
import sys
import json
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Environment & API Configurations (Secrets read dynamically from environment)
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
POLLINATIONS_API_KEY = os.environ.get("POLLINATIONS_API_KEY", "")
MAKE_WEBHOOK_URL = os.environ.get("MAKE_WEBHOOK_URL", "")

STATE_FILE = "autopilot_state.json"
BLOG_DIR = os.path.join(BASE_DIR, "blog")
ASSETS_BLOG_DIR = os.path.join(BASE_DIR, "assets", "blog")
BLOG_DATA_JSON = os.path.join(BASE_DIR, "blog_data.json")

SERVICES = {
    "google-ads": "Google Ads & SEA",
    "meta-ads": "Meta Ads & Social Ads",
    "seo": "Référencement Naturel (SEO)",
    "cro": "Optimisation des Conversions (CRO)",
    "emailing": "Emailing & Automation",
    "strategie": "Stratégie Digitale",
    "affichage": "Affichage Dynamique",
    "audit": "Audit Digital",
    "design": "Design & Impression",
    "developpement": "Développement Web & Mobile",
    "formations": "Formations & Master Classes"
}

def get_autopilot_state():
    """Load or initialize state file to track launch date and generation count."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    
    state = {
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "total_generated": 0,
        "history": []
    }
    save_autopilot_state(state)
    return state

def save_autopilot_state(state):
    """Save autopilot state to disk."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def calculate_daily_quota(state=None):
    """
    Calculate daily post quota based on active week:
    - Weeks 1 & 2 : 2 articles / day
    - Weeks 3 & 4 : 3 articles / day
    - Weeks 5 & 6 : 4 articles / day
    - Week 7+     : 5 articles / day
    """
    if not state:
        state = get_autopilot_state()
    
    try:
        start = datetime.strptime(state["start_date"], "%Y-%m-%d").date()
    except Exception:
        start = date.today()
        
    days_elapsed = (date.today() - start).days
    weeks_elapsed = (days_elapsed // 7) + 1

    if weeks_elapsed in (1, 2):
        quota = 2
    elif weeks_elapsed in (3, 4):
        quota = 3
    elif weeks_elapsed in (5, 6):
        quota = 4
    else:  # Week 7+
        quota = 5

    return {
        "week": weeks_elapsed,
        "quota": quota,
        "days_elapsed": days_elapsed
    }
