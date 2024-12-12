import json
import re
from typing import List, Dict, Any, Optional
import unicodedata

class LLMResponseGenerator:
    """
    Simulated LLM response generator.
    In a real implementation, this would interface with an actual LLM API.
    """
    @staticmethod
    def generate_response(college_info: Dict[Any, Any], query: str, key: str) -> str:
        """
        Generate a natural language response based on retrieved college information.

        :param college_info: Dictionary containing college details
        :param query: Original user query
        :param key: Key identifying the type of information requested
        :return: Formatted natural language response
        """
        templates = {
            "location": "{name} is located in {location}.",
            "courses": "{name} offers courses such as: {courses}.",
            "placement": "The placement record at {name} includes an average package of {average_package} and a highest package of {highest_package}.",
            "fee": "The fee structure at {name} is {fee_structure}.",
            "facilities": "Facilities at {name} include: {facilities}."
        }

        try:
            template = templates.get(key, "")
            if template:
                return template.format(
                    name=college_info.get('name', 'The college'),
                    location=college_info.get('location', 'an unspecified location'),
                    courses=', '.join(college_info.get('courses', ['various disciplines'])),
                    average_package=college_info.get('average_package', 'competitive packages'),
                    highest_package=college_info.get('highest_package', 'impressive top packages'),
                    fee_structure=college_info.get('fee_structure', 'reasonable fees'),
                    facilities=college_info.get('facilities', 'modern infrastructure')
                )
        except Exception as e:
            print(f"LLM Response Generation Error: {e}")

        return "Sorry, specific information is not available for this query."

class CollegeQueryHandler:
    def __init__(self, data_path="colleges_data.json"):
        """
        Initialize the query handler with college data.

        :param data_path: Path to the JSON file containing college information
        """
        try:
            with open(data_path, 'r', encoding='utf-8') as file:
                self.colleges_data = json.load(file)['colleges']

            # Preprocess data for more flexible searching
            for college in self.colleges_data:
                college['normalized_name'] = self.normalize_text(college['name'])
                college['normalized_location'] = self.normalize_text(college['location'])
                college['normalized_courses'] = [self.normalize_text(course) for course in college.get('courses', [])]
        except Exception as e:
            print(f"Error loading college data: {e}")
            self.colleges_data = []

        # Initialize LLM response generator
        self.llm_generator = LLMResponseGenerator()

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text for more flexible matching.

        :param text: Input text to normalize
        :return: Normalized text
        """
        if not isinstance(text, str):
            return str(text).lower().strip()

        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        text = re.sub(r'[^\w\s]', '', text.lower().strip())

        return text

    def find_college(self, query: str) -> Optional[Dict[Any, Any]]:
        """
        Find a specific college based on the query with flexible matching.

        :param query: User's search query
        :return: Matching college or None
        """
        normalized_query = self.normalize_text(query)

        for college in self.colleges_data:
            if (normalized_query in college['normalized_name'] or
                normalized_query in college['normalized_location'] or
                any(normalized_query in course for course in college['normalized_courses']) or
                any(term in normalized_query for term in college['normalized_name'].split())):
                return college

        return None

    def handle_query(self, query: str) -> str:
        """
        Main query handling function with specific response.

        :param query: User's input query
        :return: Formatted response
        """
        college = self.find_college(query)
        if not college:
            return f"No college found matching the query '{query}'."

        keywords = {
            "location": ["location", "where", "situated"],
            "courses": ["courses", "branch", "study", "program"],
            "placement": ["placement", "job", "recruit", "company", "package"],
            "fee": ["fee", "scholarship", "cost"],
            "facilities": ["facility", "infrastructure", "campus"]
        }

        for key, terms in keywords.items():
            if any(term in query.lower() for term in terms):
                return self.llm_generator.generate_response(college, query, key)

        return f"Sorry, I couldn't find specific information for your query about '{college['name']}'."

def main():
    handler = CollegeQueryHandler()
    print("Precise College Information Retrieval System")
    print("Enter 'quit' to exit the application")

    while True:
        try:
            query = input("\nEnter your search query: ")
            if query.lower() == 'quit':
                print("Thank you for using the system. Goodbye!")
                break

            print("\n--- Search Results ---")
            print(handler.handle_query(query))

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
