import spacy
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import ast

# Load NLP model
nlp = spacy.load('en_core_web_sm')

# Load dataset
file_path = './colleges_data.csv'
data = pd.read_csv(file_path)

# Fill missing values in fees columns for consistency
data['Hostel Fees'] = data['Hostel Fees'].fillna(0)
data['Mess Fees'] = data['Mess Fees'].fillna(0)

# Drop duplicate rows for clean results
data = data.drop_duplicates(subset=['College Name', 'Course'])

# Extract keywords from dataset
locations = data['Location'].dropna().unique().tolist()
courses = data['Course'].dropna().unique().tolist()
types = data['Type'].dropna().unique().tolist()

# Feature engineering - Fix Cutoff column with valid numeric value
def extract_cutoff(cutoff_str):
    try:
        cutoff_dict = ast.literal_eval(cutoff_str)
        return cutoff_dict
    except (ValueError, SyntaxError, AttributeError):
        return None

data['Cutoff'] = data['Cutoff'].apply(lambda x: extract_cutoff(x) if isinstance(x, str) else x)

# Feature engineering - Apply Hostel Availability transformation
data['Hostel_Available'] = data['Hostel Availability'].apply(lambda x: 1 if x else 0)

# Prepare the model and save it with pickle
def prepare_and_save_model(data, model_file='college_recommendation_model.pkl'):
    X = data[['Hostel Fees', 'Mess Fees', 'Hostel_Available']]
    y = data['College Name']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Save the model
    with open(model_file, 'wb') as file:
        pickle.dump(model, file)

    print(f"Model saved to {model_file}")

# Call the function to save the model
prepare_and_save_model(data)

# Load the model
def load_model(model_file='college_recommendation_model.pkl'):
    with open(model_file, 'rb') as file:
        model = pickle.load(file)
    print("Model loaded successfully")
    return model

model = load_model()

# Utility functions
def extract_number(query):
    doc = nlp(query)
    for token in doc:
        if token.like_num:
            try:
                return float(token.text.replace(',', ''))
            except ValueError:
                continue
    return None

# Category extraction
categories = ['OPEN', 'SC', 'ST', 'OBC', 'EWS', 'PWD']

def extract_category(query):
    doc = nlp(query)
    for token in doc:
        if token.text.upper() in categories:
            return token.text.upper()
    return 'OPEN'  # Default category if none specified

def extract_college(query):
    college_names = data['College Name'].tolist()
    for college in college_names:
        if college.lower() in query.lower():
            return college
    return None

def extract_course(query):
    for course in courses:
        if course.lower() in query.lower():
            return course
    return None

def process_query(query):
    college_name = extract_college(query)
    course_name = extract_course(query)
    category = extract_category(query)
    number = extract_number(query)

    # Intent for cutoff range (above or below a specific percentile)
    if 'cutoff' in query.lower():
        if number is not None:
            if 'above' in query.lower() or 'greater than' in query.lower():
                return suggest_colleges_above_cutoff(number)
            elif 'below' in query.lower() or 'less than' in query.lower():
                return suggest_colleges_below_cutoff(number)
        else:
            return "Please provide a specific percentile for the cutoff."

    if 'suggest' in query.lower() and number is not None:
        return suggest_colleges(number)

    if college_name:
        if course_name and 'cutoff' in query.lower():
            return fetch_college_cutoff(college_name, course_name, category)
        if 'mess fees' in query.lower():
            return fetch_college_details(college_name, 'mess')
        elif 'courses' in query.lower() or 'course' in query.lower():
            return fetch_college_courses(college_name)
        elif 'fees' in query.lower() and 'structure' not in query.lower():
            return fetch_college_details(college_name, 'fees')
        elif 'fees structure' in query.lower():
            return fetch_college_details(college_name, 'fees_structure')
        elif 'hostel' in query.lower():
            return fetch_college_details(college_name, 'hostel')
        elif 'type' in query.lower():
            return fetch_college_details(college_name, 'type')
        elif 'package' in query.lower():
            return fetch_package_details(college_name, query)
        elif 'scholarships' in query.lower():
            return fetch_college_details(college_name, 'scholarships')
        elif 'gender' in query.lower():
            return fetch_college_details(college_name, 'gender')
        elif 'location' in query.lower():
            return fetch_college_details(college_name, 'location')
        else:
            return "Please specify the detail you're looking for (e.g., mess fees, courses, cutoff, etc.)."

    return "Could not find the college you're looking for. Please check the spelling or try again."

# Function to suggest colleges above a specific cutoff
def suggest_colleges_above_cutoff(percentile):
    suggested_colleges = data[data['Cutoff'].apply(lambda x: isinstance(x, dict) and x.get('OPEN', 0) > percentile)]
    if suggested_colleges.empty:
        return f"No colleges found with a cutoff above {percentile} percentile."

    college_list = suggested_colleges[['College Name', 'Course', 'Cutoff']].to_dict('records')
    return f"Colleges with cutoff above {percentile}%:\n" + "\n".join([f"{college['College Name']} - {college['Course']} (Cutoff: {college['Cutoff']['OPEN']})" for college in college_list])

# Function to suggest colleges below a specific cutoff
def suggest_colleges_below_cutoff(percentile):
    suggested_colleges = data[data['Cutoff'].apply(lambda x: isinstance(x, dict) and x.get('OPEN', 0) < percentile)]
    if suggested_colleges.empty:
        return f"No colleges found with a cutoff below {percentile} percentile."

    college_list = suggested_colleges[['College Name', 'Course', 'Cutoff']].to_dict('records')
    return f"Colleges with cutoff below {percentile}%:\n" + "\n".join([f"{college['College Name']} - {college['Course']} (Cutoff: {college['Cutoff']['OPEN']})" for college in college_list])

# Main interactive chatbot
if __name__ == "__main__":
    print("Welcome to the College Recommendation Chatbot!")
    print("\nYou can ask queries related to:")
    print("Locations:", locations)
    print("Courses:", courses)
    print("Types:", types)

    while True:
        user_query = input("\nEnter your query (type 'exit' to quit): ")
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = process_query(user_query)
        print(f"\nChatbot: {response}")
