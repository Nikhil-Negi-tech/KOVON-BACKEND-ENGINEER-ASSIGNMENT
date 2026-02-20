# Semantic Candidate–Job Matching Backend

FastAPI backend for semantic candidate-job matching using HuggingFace embeddings and FAISS vector search.

## Tech Stack

- Python 3.10+
- FastAPI
- FAISS (`faiss-cpu`) for vector storage
- HuggingFace sentence-transformers for embeddings
- Pydantic v2 models

## Project Structure

```text
app/
 ├── main.py
 ├── api/
 │    ├── candidates.py
 │    └── jobs.py
 ├── services/
 │    ├── embedding_service.py
 │    └── matching_service.py
 ├── db/
 │    ├── dependencies.py
 │    ├── repositories.py
 │    └── vector_store.py
 ├── models/
 │    ├── candidate.py
 │    └── job.py
 ├── schemas/
 │    ├── candidate.py
 │    ├── job.py
 │    └── matching.py
 └── config.py
```

## API Endpoints

### 1) Create Candidate
`POST /candidates`

Request body:

```json
{
  "name": "Alice",
  "skill_description": "Python backend developer with FastAPI and SQL experience",
  "experience": 5,
  "location": "Berlin"
}
```

Behavior:
- Generates embedding for `skill_description`
- Stores candidate metadata in repository
- Stores candidate embedding in FAISS candidate index

### 2) Create Job
`POST /jobs`

Request body:

```json
{
  "title": "Backend Engineer",
  "country": "Germany",
  "description": "Looking for a FastAPI engineer with Python microservices experience"
}
```

Behavior:
- Generates embedding for `description`
- Stores job metadata in repository
- Stores job embedding in FAISS job index/cache

### 3) Match Candidates
`GET /jobs/{job_id}/match`

Behavior:
- Retrieves stored job embedding
- Searches candidate vectors by cosine similarity
- Ranks by:
  1. similarity score (descending)
  2. experience (descending) as tie-breaker
- Returns top 5 candidates

Example response:

```json
{
  "jobId": "f3ff3cd8-7b91-40a6-a7f8-df8e7b8dfd6f",
  "matches": [
    {
      "candidateId": "74127d6e-d047-41e2-b312-d5d8873e9716",
      "similarityScore": 0.8123,
      "experience": 6
    }
  ]
}
```

## Embedding Model Used

Default model: `sentence-transformers/all-MiniLM-L6-v2`

Configured in `app/config.py` via `EMBEDDING_MODEL_NAME` environment variable.

## Similarity Calculation

Embeddings are L2-normalized before insertion and query. FAISS uses `IndexFlatIP` (inner product).
For normalized vectors, inner product equals cosine similarity:

- $\cos(\theta) = \frac{A \cdot B}{\|A\|\|B\|}$
- with $\|A\|=\|B\|=1$, cosine similarity becomes $A \cdot B$

So the returned FAISS score is cosine similarity.

## Setup (Local)

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the API:

```bash
uvicorn app.main:app --reload
```

4. Open docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker

Build image:

```bash
docker build -t semantic-matching-api .
```

Run container:

```bash
docker run --rm -p 8000:8000 semantic-matching-api
```

## Notes

- Storage is in-memory (repositories + FAISS indexes). Restarting the service resets data.
- This is intentionally lightweight and modular for extension to persistent databases.
