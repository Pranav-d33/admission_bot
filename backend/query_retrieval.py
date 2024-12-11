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
    def generate_response(college_info: Dict[Any, Any], query: str) -> str:
        """
        Generate a natural language response based on retrieved college information.
        
        :param college_info: Dictionary containing college details
        :param query: Original user query
        :return: Formatted natural language response
        """
        # Basic context understanding and response generation
        prompt_mapping = [
            {
                'keywords': ['location', 'where', 'situated'],
                'template': "{}  is located in {}. It's situated in a strategic location that offers great opportunities for students interested in {}."
            },
            {
                'keywords': ['courses', 'branch', 'study', 'program'],
                'template': "{} offers a diverse range of courses including: {}. These programs are designed to provide comprehensive education in fields like engineering, technology, and applied sciences."
            },
            {
                'keywords': ['placement', 'job', 'recruit', 'company'],
                'template': "The placement record at {} is impressive. Students have an average package of {} and have been recruited by top companies. The highest package recorded is {}."
            },
            {
                'keywords': ['fee', 'scholarship', 'cost'],
                'template': "The fee structure at {} is competitive. {} provides various scholarship opportunities to support deserving students. The estimated fee structure is {}."
            },
            {
                'keywords': ['facility', 'infrastructure', 'campus'],
                'template': "{} boasts excellent facilities including: {}. The campus is designed to provide a holistic learning environment for students."
            }
        ]

        # Normalize query
        query_lower = query.lower()

        # Select appropriate response template
        for mapping in prompt_mapping:
            if any(keyword in query_lower for keyword in mapping['keywords']):
                try:
                    # Format the response using available information
                    return mapping['template'].format(
                        college_info.get('name', 'The college'),
                        college_info.get('location', 'an unspecified location'),
                        ', '.join(college_info.get('courses', ['various disciplines'])),
                        college_info.get('average_package', 'competitive packages'),
                        college_info.get('highest_package', 'impressive top packages'),
                        college_info.get('fee_structure', 'reasonable fees'),
                        college_info.get('scholarships', 'multiple scholarship options'),
                        college_info.get('facilities', 'modern infrastructure')
                    )
                except Exception as e:
                    print(f"LLM Response Generation Error: {e}")
        
        # Fallback generic response
        return f"Here's some information about {college_info.get('name', 'the college')}. " \
               f"Located in {college_info.get('location', 'a great location')}, " \
               f"it offers courses like {', '.join(college_info.get('courses', ['various disciplines']))}. " \
               f"With an average package of {college_info.get('average_package', 'competitive salary')}, " \
               f"it's a promising institution for students."

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
                # Create normalized versions of key fields
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
        
        # Remove accents
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^\w\s]', '', text.lower().strip())
        
        return text

    def find_college(self, query: str) -> Optional[Dict[Any, Any]]:
        """
        Find a specific college based on the query with flexible matching.
        
        :param query: User's search query
        :return: Matching college or None
        """
        # Normalize query
        normalized_query = self.normalize_text(query)
        
        # Try different matching strategies
        matching_strategies = [
            # Direct full normalized name match
            lambda q: next((college for college in self.colleges_data 
                            if q == college['normalized_name']), None),
            
            # Partial normalized name match
            lambda q: next((college for college in self.colleges_data 
                            if q in college['normalized_name'] or 
                               college['normalized_name'] in q), None),
            
            # Location match
            lambda q: next((college for college in self.colleges_data 
                            if q in college['normalized_location'] or 
                               college['normalized_location'] in q), None),
            
            # Course match
            lambda q: next((college for college in self.colleges_data 
                            if any(q in course or course in q 
                                   for course in college['normalized_courses'])), None),
            
            # Advanced abbreviation and partial matching
            lambda q: next((college for college in self.colleges_data 
                            if (q == ''.join(word[0] for word in college['name'].split()) or
                                any(q in alt_name for alt_name in [
                                    college['normalized_name'], 
                                    college.get('short_name', '').lower()
                                ]))), None)
        ]
        
        # Try each matching strategy
        for strategy in matching_strategies:
            match = strategy(normalized_query)
            if match:
                return match
        
        return None

    def handle_query(self, query: str) -> str:
        """
        Main query handling function with LLM-enhanced response.
        
        :param query: User's input query
        :return: Formatted response
        """
        # Find the specific college
        college = self.find_college(query)
        
        # If no college found, perform general search
        if not college:
            return self.general_search(query)
        
        # Generate LLM-enhanced response
        try:
            llm_response = self.llm_generator.generate_response(college, query)
            return llm_response
        except Exception as e:
            # Fallback to standard college info if LLM generation fails
            print(f"LLM Response Generation Error: {e}")
            return self.get_specific_college_info(college, query)

    def get_specific_college_info(self, college: Dict[Any, Any], query: str) -> str:
        """
        Generate a detailed, context-aware response for a specific college.
        
        :param college: College dictionary
        :param query: Original user query
        :return: Formatted response string
        """
        response_parts = []

        # Always start with basic college information
        response_parts.append(f"📍 {college['name']}")

        # Context-specific information extraction
        info_extractors = [
            (lambda q: 'location' in q or 'where' in q, 
             lambda: f"📍 Location: {college['location']}"),
            
            (lambda q: 'courses' in q or 'branch' in q, 
             lambda: "🎓 Courses Offered:\n" + 
                     "\n".join(f"   - {course}" for course in college.get('courses', ['Not available']))),
            
            (lambda q: 'facilities' in q or 'facility' in q, 
             lambda: f"🏫 Facilities: {college.get('facilities', 'Not available')}"),
            
            (lambda q: 'placement' in q or 'recruit' in q or 'company' in q, 
             lambda: f"💼 Placement Records: {college.get('placement_records', 'Not available')}\n" +
                     f"📊 Average Package: {college.get('average_package', 'Not available')}"),
            
            (lambda q: 'fee' in q or 'tfws' in q or 'scholarship' in q, 
             lambda: f"💰 Fee Structure: {college.get('fee_structure', 'Not available')}\n" +
                     f"🎓 Scholarship Information: {college.get('scholarships', 'Not available')}"),
        ]

        # Check each extractor and add relevant information
        info_found = False
        for condition, info_extractor in info_extractors:
            if condition(query.lower()):
                response_parts.append(info_extractor())
                info_found = True

        # If no specific info found, add a general description
        if not info_found:
            description = self.llm_generator.generate_response(college, query)
            response_parts.append(description)

        # Add website
        response_parts.append(f"🌐 Website: {college.get('website', 'Not available')}")

        return "\n".join(response_parts)

    def general_search(self, query: str) -> str:
        """
        Perform a general search across all colleges when no specific college is found.
        
        :param query: User's search query
        :return: Formatted response
        """
        # Normalize query
        normalized_query = self.normalize_text(query)
        
        # Find matching colleges
        matching_colleges = [
            college for college in self.colleges_data
            if (normalized_query in college['normalized_name'] or
                normalized_query in college['normalized_location'] or
                any(normalized_query in course for course in college['normalized_courses']) or
                normalized_query in self.normalize_text(college.get('facilities', '')) or
                normalized_query in self.normalize_text(college.get('placement_records', '')))
        ]
        
        # If no matches found
        if not matching_colleges:
            return f"Sorry, no matching colleges found for '{query}'. Please try a different search query."
        
        # Format multiple college results with LLM-enhanced descriptions
        results = []
        for college in matching_colleges:
            try:
                llm_desc = self.llm_generator.generate_response(college, query)
                results.append(
                    f"📍 {college['name']} - {college['location']}\n" +
                    f"🎓 Description: {llm_desc}"
                )
            except Exception as e:
                print(f"LLM Description Generation Error: {e}")
                results.append(
                    f"📍 {college['name']} - {college['location']}\n" +
                    f"🎓 Courses: {', '.join(college.get('courses', ['Not available']))}"
                )
        
        return "Multiple Colleges Found:\n\n" + "\n\n".join(results)

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
    def generate_response(college_info: Dict[Any, Any], query: str) -> str:
        """
        Generate a natural language response based on retrieved college information.

        :param college_info: Dictionary containing college details
        :param query: Original user query
        :return: Formatted natural language response
        """
        # Basic context understanding and response generation
        prompt_mapping = [
            {
                'keywords': ['location', 'where', 'situated'],
                'template': "{name} is located in {location}. It is situated in a strategic location that offers great opportunities for students."
            },
            {
                'keywords': ['courses', 'branch', 'study', 'program'],
                'template': "{name} offers a diverse range of courses including: {courses}. These programs provide comprehensive education in various fields."
            },
            {
                'keywords': ['placement', 'job', 'recruit', 'company'],
                'template': "The placement record at {name} is impressive. Students have an average package of {average_package} and have been recruited by top companies. The highest package recorded is {highest_package}."
            },
            {
                'keywords': ['fee', 'scholarship', 'cost'],
                'template': "The fee structure at {name} is competitive. The estimated fee structure is {fee_structure}."
            },
            {
                'keywords': ['facility', 'infrastructure', 'campus'],
                'template': "{name} boasts excellent facilities including: {facilities}. The campus is designed to provide a holistic learning environment for students."
            }
        ]

        # Normalize query
        query_lower = query.lower()

        # Select appropriate response template
        for mapping in prompt_mapping:
            if any(keyword in query_lower for keyword in mapping['keywords']):
                try:
                    # Format the response using available information
                    return mapping['template'].format(
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

        # Fallback generic response
        return f"Here's some information about {college_info.get('name', 'the college')}. " \
               f"Located in {college_info.get('location', 'a great location')}, " \
               f"it offers courses like {', '.join(college_info.get('courses', ['various disciplines']))}. " \
               f"With an average package of {college_info.get('average_package', 'competitive salary')}, " \
               f"it's a promising institution for students."

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
                # Create normalized versions of key fields
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

        # Remove accents
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

        # Convert to lowercase and remove special characters
        text = re.sub(r'[^\w\s]', '', text.lower().strip())

        return text

    def find_college(self, query: str) -> Optional[Dict[Any, Any]]:
        """
        Find a specific college based on the query with flexible matching.

        :param query: User's search query
        :return: Matching college or None
        """
        # Normalize query
        normalized_query = self.normalize_text(query)

        # Try different matching strategies
        matching_strategies = [
            # Direct full normalized name match
            lambda q: next((college for college in self.colleges_data 
                            if q == college['normalized_name']), None),

            # Partial normalized name match
            lambda q: next((college for college in self.colleges_data 
                            if q in college['normalized_name'] or 
                               college['normalized_name'] in q), None),

            # Location match
            lambda q: next((college for college in self.colleges_data 
                            if q in college['normalized_location'] or 
                               college['normalized_location'] in q), None),

            # Course match
            lambda q: next((college for college in self.colleges_data 
                            if any(q in course or course in q 
                                   for course in college['normalized_courses'])), None),

            # Advanced abbreviation and partial matching
            lambda q: next((college for college in self.colleges_data 
                            if (q == ''.join(word[0] for word in college['name'].split()) or
                                any(q in alt_name for alt_name in [
                                    college['normalized_name'], 
                                    college.get('short_name', '').lower()
                                ]))), None)
        ]

        # Try each matching strategy
        for strategy in matching_strategies:
            match = strategy(normalized_query)
            if match:
                return match

        return None

    def handle_query(self, query: str) -> str:
        """
        Main query handling function with LLM-enhanced response.

        :param query: User's input query
        :return: Formatted response
        """
        # Find the specific college
        college = self.find_college(query)

        # If no college found, perform general search
        if not college:
            return self.general_search(query)

        # Generate LLM-enhanced response
        try:
            llm_response = self.llm_generator.generate_response(college, query)
            return llm_response
        except Exception as e:
            # Fallback to standard college info if LLM generation fails
            print(f"LLM Response Generation Error: {e}")
            return self.get_specific_college_info(college, query)

    def get_specific_college_info(self, college: Dict[Any, Any], query: str) -> str:
        """
        Generate a detailed, context-aware response for a specific college.

        :param college: College dictionary
        :param query: Original user query
        :return: Formatted response string
        """
        response_parts = []

        # Always start with basic college information
        response_parts.append(f"📍 {college['name']}")

        # Context-specific information extraction
        info_extractors = [
            (lambda q: 'location' in q or 'where' in q, 
             lambda: f"📍 Location: {college['location']}"),

            (lambda q: 'courses' in q or 'branch' in q, 
             lambda: "🎓 Courses Offered:\n" + 
                     "\n".join(f"   - {course}" for course in college.get('courses', ['Not available']))),

            (lambda q: 'facilities' in q or 'facility' in q, 
             lambda: f"🏫 Facilities: {college.get('facilities', 'Not available')}"),

            (lambda q: 'placement' in q or 'recruit' in q or 'company' in q, 
             lambda: f"💼 Placement Records: {college.get('placement_records', 'Not available')}\n" +
                     f"📊 Average Package: {college.get('average_package', 'Not available')}")
        ]

        # Check each extractor and add relevant information
        info_found = False
        for condition, info_extractor in info_extractors:
            if condition(query.lower()):
                response_parts.append(info_extractor())
                info_found = True

        if not info_found:
            description = self.llm_generator.generate_response(college, query)
            response_parts.append(description)

        response_parts.append(f"🌐 Website: {college.get('website', 'Not available')}")

        return "\n".join(response_parts)

    def general_search(self, query: str) -> str:
        normalized_query = self.normalize_text(query)

        matching_colleges = [
            college for college in self.colleges_data
            if (normalized_query in college['normalized_name'] or
                normalized_query in college['normalized_location'] or
                any(normalized_query in course for course in college['normalized_courses']) or
                normalized_query in self.normalize_text(college.get('facilities', '')) or
                normalized_query in self.normalize_text(college.get('placement_records', '')))
        ]

        if not matching_colleges:
            return f"Sorry, no matching colleges found for '{query}'. Please try a different search query."

        results = []
        for college in matching_colleges:
            try:
                llm_desc = self.llm_generator.generate_response(college, query)
                results.append(
                    f"📍 {college['name']} - {college['location']}\n" +
                    f"🎓 Description: {llm_desc}"
                )
            except Exception as e:
                print(f"LLM Description Generation Error: {e}")
                results.append(
                    f"📍 {college['name']} - {college['location']}\n" +
                    f"🎓 Courses: {', '.join(college.get('courses', ['Not available']))}"
                )

        return "Multiple Colleges Found:\n\n" + "\n\n".join(results)

def main():
    handler = CollegeQueryHandler()
    print("Precise College Information Retrieval System")
    print("Enter 'quit' to exit the application")
    print("\nExample Queries:")
    print("- What are the courses at MNIT Jaipur?")
    print("- Where is IIT Jodhpur located?")
    print("- Placement details of GECA Ajmer")

    while True:
        try:
            query = input("\nEnter your search query: ")
            if query.lower() == 'quit':
                print("Thank you for using the College Information Retrieval System. Goodbye!")
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