# data_chunking.py

import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load JSON Data
def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)["colleges"]

# Prepare data for chunking
def prepare_data(data):
    documents = []
    for college in data:
        college_text = f"""
        Name: {college['name']}
        Location: {college['location']}
        Type: {college['type']}
        Affiliation: {college['affiliation']}
        Established: {college['established']}
        Courses: {", ".join(college['courses'])}
        Facilities: {college['facilities']}
        Hostel Facilities: {college['hostel_facilities']}
        Mess Facilities: {college['mess_facilities']}
        Placement Records: {college['placement_records']}
        Average Package: {college['average_package']}
        Highest Package: {college['highest_package']}
        Fee Structure: {college['fee_structure']}
        REAP Percentile Required: {college['reap_percentile_required']}
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
