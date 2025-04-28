# File: chatbot/dialog.py

# --- Simple Dialog Management ---

def get_next_action(nlu_result):
    """
    Determines the next action based on parsed intent and entities.
    Returns: dict {'action': 'action_type', 'params': {}}
             action_type can be 'respond_static', 'call_api'
    """
    intent = nlu_result.get('intent', 'unknown')
    entities = nlu_result.get('entities', {})
    card_id = entities.get('card_id') # Will be None if not found

    action = {'action': 'respond_static', 'params': {'text_key': 'fallback'}} # Default action

    if intent == 'greet':
        action = {'action': 'respond_static', 'params': {'text_key': 'greet'}}
    elif intent == 'goodbye':
        action = {'action': 'respond_static', 'params': {'text_key': 'goodbye'}}
    elif intent == 'list_cards':
        action = {'action': 'call_api', 'params': {'api_func': 'get_all_cards', 'args': []}}
    elif intent == 'card_details':
        if card_id:
            action = {'action': 'call_api', 'params': {'api_func': 'get_card_details', 'args': [card_id]}}
        else:
            action = {'action': 'respond_static', 'params': {'text_key': 'clarify_card'}}
    elif intent == 'ask_fee':
        if card_id:
             # Ask for details, fee info is usually included
             action = {'action': 'call_api', 'params': {'api_func': 'get_card_details', 'args': [card_id]}}
        else:
             # Call general FAQ about fees
             action = {'action': 'call_api', 'params': {'api_func': 'get_faq_answer', 'args': ['fee']}}
    elif intent == 'ask_eligibility':
         if card_id:
             # Ask for details, eligibility info is usually included
             action = {'action': 'call_api', 'params': {'api_func': 'get_card_details', 'args': [card_id]}}
         else:
             # Call general FAQ about eligibility
             action = {'action': 'call_api', 'params': {'api_func': 'get_faq_answer', 'args': ['eligibility']}}
    elif intent == 'start_application':
        if card_id:
            # In a real app, you might collect more info here first via dialog
            action = {'action': 'call_api', 'params': {'api_func': 'start_application_process', 'args': [card_id]}}
        else:
            action = {'action': 'respond_static', 'params': {'text_key': 'clarify_apply'}}

    # If intent remained 'unknown', the default fallback action is used.

    print(f"Dialog Action determined: {action}")
    return action