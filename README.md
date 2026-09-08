# ASEEL - Saudi Cultural Etiquette Agent

ASEEL is a Streamlit multi-agent assistant for Saudi cultural-etiquette questions. It uses the supplied regional CSV files as its only cultural knowledge source. Responses are validated against retrieved records; when evidence is missing, ASEEL says so instead of inventing guidance.

## Architecture

```text
User -> Understanding Agent -> Retrieval Agent -> Cultural Validation Agent
                                      ^                 |
                                      |   retry/refine   | evidence sufficient
                                      +-----------------+        v
                                                   Response Agent -> Answer
```

The LangGraph workflow passes a structured shared state containing the interpreted region, user role, occasion, retrieval query, retrieval attempts, retrieved records, validation result, response, and sources.

- **Understanding agent** uses a Context Extraction Tool and Region Resolution Tool to form a structured, non-cultural interpretation of the request.
- **Retrieval agent** uses a Cultural Search Tool and Metadata Filter Tool to search a persisted ChromaDB collection using local SentenceTransformer embeddings, then enforce region/category scope.
- **Cultural validation agent** uses an Evidence Validation Tool and Conflict Check Tool to reject low-relevance, region-mismatched, contradictory, or unscoped mixed-region records before permitting one conservative query-refinement retry.
- **Response agent** creates a source-grounded response. With an OpenAI key it writes a polished answer; without one, it still works with a deterministic, evidence-only response. It never calls an LLM when there is no validated knowledge.

## Project layout

```text
ASEEL/
├── app.py                 # Streamlit UI
├── agents/                # agent responsibilities and shared state
├── config/                # central paths and environment settings
├── data/raw/              # supplied CSVs (not committed)
├── data/vector_store/     # generated ChromaDB index (not committed)
├── prompts/               # versioned LLM instructions
├── retrieval/             # normalization, ingestion, and vector search
├── scripts/build_index.py # index construction
├── tests/                 # unit tests
├── tools/                 # retrieval-agent tool boundary
├── workflow/              # LangGraph orchestration
├── .env.example
├── requirements.txt
└── README.md
```

## Installation

From the project root, create and activate a virtual environment, then install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env`.

```powershell
Copy-Item .env.example .env
```

Required variables:

- `OPENAI_API_KEY` - optional; enables LLM-written grounded replies.
- `OPENAI_MODEL` - optional; defaults to `gpt-4o-mini`.
- `ASEEL_COLLECTION`, `ASEEL_TOP_K`, `ASEEL_MIN_RELEVANCE` - optional retrieval tuning.

No key is required for indexing, tests, or deterministic evidence-only answers.

## Dataset setup and ingestion

Place these files in `data/raw/`: `WEST.csv`, `SOUTH.csv`, `NORTH.csv`, `GENERAL.csv`, `EAST.csv`, and `CENTERAL.csv`. The importer accommodates the observed schema difference: General has five columns, while regional files can include `Question Type`.

Other CSV files may remain in the folder; ASEEL will skip them and print a warning.

To copy a supplied dataset folder into the project and validate it:

```powershell
python -m retrieval.ingestion --source-dir "C:\path\to\dataset" --stage
```

Build (or rebuild) the vector database:

```powershell
python -m scripts.build_index
```

## Run the app

```powershell
streamlit run app.py
```

## Test

```powershell
pytest -q
```

## Troubleshooting

- **Index not found:** copy the CSVs into `data/raw/` and run `python -m scripts.build_index`.
- **Embedding model download fails:** confirm internet access for the first `sentence-transformers` model download, then retry indexing.
- **LLM error:** remove or correct `OPENAI_API_KEY`; ASEEL will use deterministic grounded responses when no key is configured.
- **No answer found:** provide the Saudi region and a more specific occasion. A fallback is expected when the dataset lacks relevant information.

## Dataset fidelity

The ingestion layer preserves the CSV question, answer, domain, category, question type, and source region. It does not synthesize or augment cultural knowledge.
