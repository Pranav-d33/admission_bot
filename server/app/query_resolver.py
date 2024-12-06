from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize NLP model (spaCy)
nlp = spacy.load('en_core_web_sm')

# Load college data
def load_college_data():
    data = pd.read_csv('data/colleges_data.csv')  # Load from data folder
    return data

def extract_number(query):
    doc = nlp(query)
    for token in doc:
        if token.like_num:
            return float(token.text.replace(',', ''))
    return None

def extract_course_location(query):
    doc = nlp(query)
    course_keywords = ["literature", "science", "engineering", "arts", "commerce"]
    course_name = next((word for word in course_keywords if word in query.lower()), None)
    locations = [ent.text.strip() for ent in doc.ents if ent.label_ == "GPE"]
    return course_name, locations

# Function to apply filters
def apply_filters(data, course_name=None, max_fees=None, locations=None):
    if locations:
        data = data[data['Location'].str.lower().isin([loc.lower() for loc in locations])]
    if course_name:
        data = data[data['Course Name'].str.lower().str.contains(course_name.lower(), case=False, na=False)]
    if max_fees is not None:
        data = data[data['Fees'] <= max_fees]
    return data

# Main query resolution function
def resolve_query(query: str):
    data = load_college_data()
    
    # Extract course and location
    course_name, locations = extract_course_location(query)
    max_fees = extract_number(query)

    # Filter colleges
    filtered_data = apply_filters(data, course_name, max_fees, locations)

    if not filtered_data.empty:
        response = "\n".join(
            [
                f"{row['College Name']} ({row['Location']}): {row['Course Name']} - Fees: {row['Fees']}"
                for _, row in filtered_data.iterrows()
            ]
        )
        return response
    else:
        return "No matching colleges found. Please refine your query."

