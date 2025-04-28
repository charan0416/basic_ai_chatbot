# File: chatbot/bank_api_client.py
import requests # Use requests structure even for simulation
import json
from .config import APP_CONFIG # Relative import for config within the package

# --- Internal API Simulation (Replace with Actual Calls to Charan's Bank) ---

MOCK_CARD_DB = {
    "cb-rewards": {
        "id": "cb-rewards", "name": "Charan Bank Rewards Card", "summary": "Earn points on every purchase.",
        "details": "Earn 2x points on groceries, 1x on everything else. Annual Fee: $50. APR: 18.99%.",
        "eligibility": "Minimum income $30,000/year."
    },
    "cb-travel": {
        "id": "cb-travel", "name": "Charan Bank TravelMaster", "summary": "Airline miles and travel perks.",
        "details": "Earn 3x miles on travel bookings, lounge access. Annual Fee: $150. APR: 21.99%.",
        "eligibility": "Minimum income $60,000/year. Good credit score required."
    },
    "cb-cashback": {
        "id": "cb-cashback", "name": "Charan Bank SimpleCash", "summary": "Flat cashback on all spending.",
        "details": "Earn 1.5% cashback on all purchases. No Annual Fee. APR: 19.99%.",
        "eligibility": "Minimum income $25,000/year."
    }
}

MOCK_FAQS = {
    "fee": "Fees vary by card. The Rewards Card is $50, TravelMaster is $150. SimpleCash has no annual fee.",
    "eligibility": "Eligibility depends on the card, income, and credit score. Please check the details for each card.",
    "apply": "You can start an application by telling me which card you want to apply for.",
    "general": "You can ask about card options, fees, benefits, and how to apply."
}

def get_all_cards():
    """Simulates GET /api/credit-cards. Returns (data, status_code)."""
    print(f"SIMULATING API CALL: GET {APP_CONFIG.BANK_API_URL}/credit-cards")
    # In real life: response = requests.get(f"{APP_CONFIG.BANK_API_URL}/credit-cards", headers=...)
    cards_summary = [{"id": data["id"], "name": data["name"], "summary": data["summary"]} for data in MOCK_CARD_DB.values()]
    return {"cards": cards_summary}, 200

def get_card_details(card_id):
    """Simulates GET /api/credit-cards/{card_id}. Returns (data, status_code)."""
    print(f"SIMULATING API CALL: GET {APP_CONFIG.BANK_API_URL}/credit-cards/{card_id}")
    if card_id in MOCK_CARD_DB:
        return MOCK_CARD_DB[card_id], 200
    else:
        return {"error": f"Card '{card_id}' not found"}, 404

def get_faq_answer(query_term):
    """Simulates GET /api/faqs/credit-cards?query=... Returns (data, status_code)."""
    print(f"SIMULATING API CALL: GET {APP_CONFIG.BANK_API_URL}/faqs/credit-cards?query={query_term}")
    query_term_lower = query_term.lower()
    for keyword, answer in MOCK_FAQS.items():
        if keyword in query_term_lower:
            return {"faqs": [{"q": f"Info about {keyword}", "a": answer}]}, 200
    # Return general if specific term not found in keywords
    return {"faqs": [{"q": "General Info", "a": MOCK_FAQS["general"]}]}, 200

def start_application_process(card_id, user_details=None):
    """Simulates POST /api/applications/credit-card/start. Returns (data, status_code)."""
    print(f"SIMULATING API CALL: POST {APP_CONFIG.BANK_API_URL}/applications/credit-card/start")
    print(f"  Payload: {{'card_id': '{card_id}', 'user_info': {user_details}}}")
    if card_id in MOCK_CARD_DB:
        return {
            "message": f"Application process initiated for {MOCK_CARD_DB[card_id]['name']}. Follow up instructions will be provided.",
            "application_reference": f"APP-{card_id.upper()}-{abs(hash(card_id)) % 10000}"
        }, 201 # 201 Created
    else:
        return {"error": f"Cannot start application for unknown card '{card_id}'"}, 400