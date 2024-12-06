# Query Resolver Application

This README outlines the setup, structure, and functionality of the **Query Resolver Application**. The application integrates machine learning and NLP techniques to process and resolve user queries about colleges, courses, fees, and more.

---

## Features

1. **Query Resolution**: Leverages TF-IDF and cosine similarity for matching user queries with college data.
2. **Data Filtering**: Filters colleges based on course, fees, and location criteria.
3. **Ambiguous Query Handling**: Identifies and prompts for clarification on ambiguous queries.
4. **Generative AI Integration**: Uses OpenAI and Google Gemini models as fallbacks for complex or unknown queries.

---

## Folder Structure

```
server/
│
├── main.py               # Entry point for the backend
├── requirements.txt      # Python dependencies
└── app/
    ├── __init__.py       # Initialize app module (can be empty)
    ├── models.py         # Pydantic models for validation
    ├── routes.py         # API route definitions
    ├── query_resolver.py # Core logic to process and resolve queries
    ├── ml_model.py       # Model-related code (e.g., training ML models)
    └── data/             # Folder for raw or preprocessed data
        └── college_data.csv  # College dataset
```

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- FastAPI
- scikit-learn
- spaCy
- pandas
- joblib
- OpenAI and Google Generative AI Python SDKs

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/query-resolver.git
   cd query-resolver
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Set up API keys for OpenAI and Google Generative AI (if required):
   - Configure the OpenAI SDK with your API key.
   - Add your Google Generative AI API key to the application code.

---

## Usage

### Running the Application

Start the FastAPI server by running:
```bash
uvicorn main:app --reload
```

Access the application at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Endpoints

#### `GET /`
**Description**: Returns a welcome message.

#### `POST /resolve-query/`
**Description**: Accepts a query and resolves it using the query resolver.

**Request Body**:
```json
{
    "query": "Find colleges offering Computer Engineering in Mumbai under 10 lakhs."
}

```

**Response Example**:
```json
{
    "response": "XYZ College (Mumbai): Computer Engineering - Fees: 9,50,000"
}
```

---

## Query Resolver Logic

1. **Data Loading**:
   - Reads the `college_data.csv` file into a pandas DataFrame.

2. **NLP Processing**:
   - Extracts numerical values (e.g., fees), courses, and locations using spaCy.

3. **Filtering**:
   - Applies multi-criteria filters based on the query.

4. **Fallbacks**:
   - Queries OpenAI or Google Gemini models for unsupported or ambiguous queries.

5. **Response Generation**:
   - Generates a user-friendly response with matching colleges and their details.

---

## Future Enhancements

1. **Add more robust filtering**: Support additional filters like ratings and placements.
2. **Train ML models on large-scale data**: Improve accuracy for unknown queries.
3. **Integrate a database**: Replace CSV with a scalable database like PostgreSQL or MongoDB.
4. **Enhanced UI/UX**: Build a frontend to improve user interaction.

---

## Troubleshooting

1. **Error: Can't find model 'en_core_web_sm'**
   - Run `python -m spacy download en_core_web_sm` to install the required spaCy mo