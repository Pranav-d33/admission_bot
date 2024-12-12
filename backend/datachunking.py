import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load JSON Data
def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file).get("colleges", [])

# Prepare data for chunking
def prepare_data(data):
    documents = []
    for college in data:
        college_text = f"""
        Name: {college.get('name', 'N/A')}
        Location: {college.get('location', 'N/A')}
        Type: {college.get('type', 'N/A')}
        Affiliation: {college.get('affiliation', 'N/A')}
        Established: {college.get('established', 'N/A')}
        Courses: {", ".join(college.get('courses', []))}
        Facilities: {college.get('facilities', 'N/A')}
        Hostel Facilities: {college.get('hostel_facilities', 'N/A')}
        Mess Facilities: {college.get('mess_facilities', 'N/A')}
        Placement Records: {college.get('placement_records', 'N/A')}
        Average Package: {college.get('average_package', 'N/A')}
        Highest Package: {college.get('highest_package', 'N/A')}
        Fee Structure: {college.get('fee_structure', 'N/A')}
        REAP Percentile Required: {college.get('reap_percentile_required', 'N/A')}
        """
        documents.append(college_text.strip())
    return documents

# Chunk data
def chunk_data(documents, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.create_documents(documents)

# Main function
if __name__ == "__main__":
    # Load data
    file_path = "colleges_data.json"  # Path to your JSON file
    data = load_data(file_path)

    # Prepare data for chunking
    documents = prepare_data(data)

    # Chunk the data
    chunks = chunk_data(documents)

    # Save chunks to a file for later use
    with open("chunks.json", "w") as chunk_file:
        json.dump([chunk.dict() for chunk in chunks], chunk_file, indent=4)

    print(f"Data chunked successfully! Saved {len(chunks)} chunks to chunks.json.")
