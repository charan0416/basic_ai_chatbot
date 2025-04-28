# File: chatbot/nlu.py

# --- Simple NLU (Keyword Based) ---

INTENTS = {
    "greet": ["hello", "hi", "hey", "good morning", "good afternoon"],
    "goodbye": ["bye", "goodbye", "thanks", "thank you", "ok bye", "later"],
    "list_cards": ["options", "cards", "list cards", "show me cards", "what cards"],
    "card_details": ["tell me about", "details on", "more info", "info about", "what is the", "about the"],
    "ask_fee": ["fee", "cost", "annual fee", "how much is"],
    "ask_eligibility": ["eligible", "eligibility", "qualify", "requirements", "need for"],
    "start_application": ["apply", "application", "sign up", "get the card", "want the"]
}

# Maps keywords to canonical card IDs (longest match first is important here)
ENTITY_MAP = {
    "rewards card": "cb-rewards",
    "cb-rewards": "cb-rewards",
    "travelmaster": "cb-travel", # Longer name first
    "travel card": "cb-travel",
    "cb-travel": "cb-travel",
    "simplecash": "cb-cashback", # Longer name first
    "cashback card": "cb-cashback",
    "cb-cashback": "cb-cashback",
}

def parse_message(message):
    """
    Analyzes the user message to identify intent and entities using keywords.
    Returns: dict {'intent': 'intent_name' or 'unknown', 'entities': {'card_id': 'value' or None}}
    """
    message_lower = message.lower().strip()
    parsed = {'intent': 'unknown', 'entities': {}}

    # 1. Identify Intent (simple first match)
    for intent, keywords in INTENTS.items():
        if any(keyword in message_lower for keyword in keywords):
            parsed['intent'] = intent
            break

    # 2. Extract Entities (Basic Card ID)
    # Check even if intent is unknown, as mentioning card name implies interest
    found_card_id = None
    # Check for longest match first to avoid partial matches (e.g., "rewards card" before "card")
    sorted_entity_keys = sorted(ENTITY_MAP.keys(), key=len, reverse=True)
    for keyword in sorted_entity_keys:
        if keyword in message_lower:
            found_card_id = ENTITY_MAP[keyword]
            parsed['entities']['card_id'] = found_card_id
            # If intent was unknown but we found a card, assume they want details
            if parsed['intent'] == 'unknown':
                 parsed['intent'] = 'card_details'
            break # Stop after first (longest) entity match

    print(f"NLU Result for '{message}': {parsed}")
    return parsed