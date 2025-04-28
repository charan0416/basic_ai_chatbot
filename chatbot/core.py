# File: chatbot/core.py
import json
# Use relative imports within the package
from . import nlu
from . import dialog
from . import bank_api_client

# Simple map for static text responses keyed by dialog action params
STATIC_RESPONSES = {
    "greet": "Hello! How can I help you with Charan's Bank credit cards today?",
    "goodbye": "You're welcome! Feel free to ask if anything else comes up. Goodbye!",
    "fallback": "I'm sorry, I didn't quite understand that. You can ask me to 'list cards', 'tell me about the rewards card', ask about 'fees' or 'eligibility', or 'apply for simplecash'.",
    "clarify_card": "Which credit card are you interested in? (e.g., Rewards Card, TravelMaster, SimpleCash)",
    "clarify_apply": "Sure, I can help with that. Which credit card would you like to apply for? (e.g., Rewards Card, TravelMaster, SimpleCash)",
    "api_error": "Sorry, I encountered an issue trying to get that information from our systems right now. Please try again in a moment.",
    "card_not_found": "Hmm, I couldn't find information for the specific card you mentioned. Could you please check the name (e.g., Rewards Card, TravelMaster, SimpleCash)?"
}

# --- Response Formatting Helpers ---

def format_card_list(api_data):
    """Formats the response from get_all_cards API."""
    cards = api_data.get("cards", [])
    if not cards:
        return "It seems we don't have any cards listed right now."
    card_list_str = "\n - ".join([f"{card['name']} ({card['summary']})" for card in cards])
    return f"Here are the credit cards we offer:\n - {card_list_str}\nWhich one would you like to know more about?"

def format_card_details(api_data):
    """Formats the response from get_card_details API."""
    if not api_data: return STATIC_RESPONSES["card_not_found"]
    details = api_data.get("details", "No specific details available.")
    eligibility = api_data.get("eligibility", "Eligibility criteria not specified.")
    name = api_data.get("name", "This card")
    # Using markdown-like bold for emphasis in the response
    return f"**{name}**\n*   **Details:** {details}\n*   **Eligibility:** {eligibility}"

def format_faq(api_data):
    """Formats the response from get_faq_answer API."""
    faqs = api_data.get("faqs", [])
    if not faqs:
        # Should ideally not happen with current FAQ logic, but good to handle
        return STATIC_RESPONSES["fallback"]
    # Just return the first answer for simplicity
    return faqs[0].get("a", STATIC_RESPONSES["fallback"])

def format_application_start(api_data):
     """Formats the response from start_application_process API."""
     return api_data.get("message", "Okay, the application process has been started.")

# --- Main Handler ---

def handle_message(user_message):
    """
    Main function to process a user message and return a bot response string.
    Orchestrates NLU -> Dialog -> API Call (if needed) -> Response Formatting.
    """
    # 1. Understand the message
    parsed_nlu = nlu.parse_message(user_message)

    # 2. Decide what to do
    next_action = dialog.get_next_action(parsed_nlu)

    bot_response = ""
    action_type = next_action.get('action')
    params = next_action.get('params', {})

    # 3. Execute the action
    if action_type == 'respond_static':
        bot_response = STATIC_RESPONSES.get(params.get('text_key'), STATIC_RESPONSES['fallback'])

    elif action_type == 'call_api':
        api_func_name = params.get('api_func')
        api_args = params.get('args', [])
        # Dynamically get the function object from the bank_api_client module
        api_func = getattr(bank_api_client, api_func_name, None)

        if api_func and callable(api_func):
            try:
                # Call the actual (simulated) API function
                api_result, status_code = api_func(*api_args)

                # 4. Format the response based on API result
                if 200 <= status_code < 300: # Success range
                    # Call specific formatter based on which API function was used
                    if api_func_name == 'get_all_cards':
                        bot_response = format_card_list(api_result)
                    elif api_func_name == 'get_card_details':
                        bot_response = format_card_details(api_result)
                    elif api_func_name == 'get_faq_answer':
                        bot_response = format_faq(api_result)
                    elif api_func_name == 'start_application_process':
                        bot_response = format_application_start(api_result)
                    else:
                        # Generic success response if no specific formatter
                        bot_response = f"OK. Received: {json.dumps(api_result)}"
                # Handle specific known errors
                elif status_code == 404 and api_func_name == 'get_card_details':
                     bot_response = STATIC_RESPONSES["card_not_found"]
                # Handle general API errors
                else:
                    print(f"API Error: Status {status_code}, Response: {api_result}")
                    bot_response = STATIC_RESPONSES['api_error']

            except Exception as e:
                # Handle errors during the API call itself (network, etc.)
                print(f"Error calling API function '{api_func_name}': {e}")
                bot_response = STATIC_RESPONSES['api_error']
        else:
            # Should not happen if dialog logic is correct
            print(f"Error: Dialog requested unknown or non-callable API function '{api_func_name}'")
            bot_response = STATIC_RESPONSES['api_error']

    else: # Fallback if action type is unknown
        print(f"Error: Unknown dialog action type '{action_type}'")
        bot_response = STATIC_RESPONSES['fallback']

    return bot_response