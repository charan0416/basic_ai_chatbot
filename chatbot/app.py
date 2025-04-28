# File: app.py
# (Place this in the main charan_chatbot directory, OUTSIDE the chatbot folder)

from flask import Flask, request, jsonify
from flask_cors import CORS
# Import the main handler function from our chatbot package
from chatbot.core import handle_message

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all domains on all routes.
# For production, you might want to restrict origins:
# CORS(app, resources={r"/chat": {"origins": "http://yourfrontenddomain.com"}})
CORS(app)

@app.route('/')
def index():
    """Basic route to check if the server is running."""
    return "Charan's Bank Chatbot Backend is running."

@app.route('/chat', methods=['POST', 'OPTIONS']) # Add OPTIONS for CORS preflight
def chat():
    """Main endpoint to handle incoming chat messages."""
    # Flask-CORS handles the OPTIONS request automatically,
    # but having it in methods list can sometimes help avoid issues.

    if request.method == 'OPTIONS':
        # CORS headers are added by Flask-CORS automatically
        return '', 204 # No Content response for preflight

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        user_message = data.get('message')

        if not user_message:
            return jsonify({"error": "Missing 'message' key in request body"}), 400

        print("-" * 20)
        print(f"Received message: {user_message}")

        # Process the message using the chatbot core logic
        try:
            bot_reply = handle_message(user_message)
        except Exception as e:
            # Catch unexpected errors during message handling
            print(f"!!! UNEXPECTED ERROR in handle_message: {e}")
            # You might want more sophisticated error logging here
            import traceback
            traceback.print_exc()
            bot_reply = "Sorry, I encountered an internal problem. Please try again later."
            return jsonify({"response": bot_reply}), 500 # Internal Server Error


        print(f"Sending reply: {bot_reply}")
        print("-" * 20)

        # Return the bot's response
        return jsonify({"response": bot_reply})

    # Should not happen if only POST/OPTIONS are defined, but good practice
    return jsonify({"error": "Method not allowed"}), 405


# Run the Flask development server
if __name__ == '__main__':
    # host='0.0.0.0' makes it accessible from other devices on the network
    # debug=True enables auto-reloading and provides detailed error pages
    # Use port 5001 to avoid common conflicts
    app.run(host='0.0.0.0', port=5001, debug=True)