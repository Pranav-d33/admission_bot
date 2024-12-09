from flask import Flask, request, jsonify
import pickle
import pandas as pd
import spacy
import ast

# Load the NLP model
nlp = spacy.load('en_core_web_sm')

# Load the dataset
file_path = 'colleges_data.csv'  # Ensure the correct path to your CSV file
data = pd.read_csv(file_path)

# Fill missing values
data['Hostel Fees'] = data['Hostel Fees'].fillna(0)
data['Mess Fees'] = data['Mess Fees'].fillna(0)
data['Hostel_Available'] = data['Hostel Availability'].apply(lambda x: 1 if x else 0)

# Extract keywords
locations = data['Location'].dropna().unique().tolist()
courses = data['Course'].dropna().unique().tolist()

# Define helper functions
categories = ['OPEN', 'SC', 'ST', 'OBC', 'EWS', 'PWD']

def extract_category(query):
    doc = nlp(query)
    for token in doc:
        if token.text.upper() in categories:
            return token.text.upper()
    return 'OPEN'

def extract_number(query):
    doc = nlp(query)
    for token in doc:
        if token.like_num:
            try:
                return float(token.text.replace(',', ''))
            except ValueError:
                continue
    return None

def suggest_colleges_above_cutoff(percentile):
    suggested_colleges = data[data['Cutoff'].apply(lambda x: isinstance(x, dict) and x.get('OPEN', 0) > percentile)]
    if suggested_colleges.empty:
        return f"No colleges found with a cutoff above {percentile} percentile."
    return suggested_colleges[['College Name', 'Course']].to_dict('records')

def suggest_colleges_below_cutoff(percentile):
    suggested_colleges = data[data['Cutoff'].apply(lambda x: isinstance(x, dict) and x.get('OPEN', 0) < percentile)]
    if suggested_colleges.empty:
        return f"No colleges found with a cutoff below {percentile} percentile."
    return suggested_colleges[['College Name', 'Course']].to_dict('records')

# Load the model
model_file = 'college_recommendation_model.pkl'
with open(model_file, 'rb') as file:
    model = pickle.load(file)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the College Recommendation API!",
        "endpoints": ["/suggest", "/above_cutoff", "/below_cutoff"]
    })

@app.route('/suggest', methods=['POST'])
def suggest_colleges():
    user_query = request.json.get('query', '')
    number = extract_number(user_query)
    if number:
        if 'above' in user_query.lower():
            results = suggest_colleges_above_cutoff(number)
        elif 'below' in user_query.lower():
            results = suggest_colleges_below_cutoff(number)
        else:
            results = {"message": "Specify 'above' or 'below' for cutoff range in your query."}
    else:
        results = {"message": "Please provide a specific percentile for the cutoff."}
    return jsonify(results)

@app.route('/above_cutoff', methods=['POST'])
def above_cutoff():
    percentile = request.json.get('percentile', 0)
    results = suggest_colleges_above_cutoff(percentile)
    return jsonify(results)

@app.route('/below_cutoff', methods=['POST'])
def below_cutoff():
    percentile = request.json.get('percentile', 0)
    results = suggest_colleges_below_cutoff(percentile)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
