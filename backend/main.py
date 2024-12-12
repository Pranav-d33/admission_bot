from flask import Flask, request, jsonify
from flask_cors import CORS
from query_retrieval import CollegeQueryHandler

app = Flask(__name__)
CORS(app)

# Initialize the CollegeQueryHandler with the path to your data file
handler = CollegeQueryHandler(data_path="colleges_data.json")

@app.route("/query", methods=["POST"])
def query():
    """
    Endpoint to handle queries sent by the React floating chatbot component.
    """
    try:
        data = request.json
        user_query = data.get("query", "")

        if not user_query:
            return jsonify({"error": "Query cannot be empty."}), 400

        response = handler.handle_query(user_query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
