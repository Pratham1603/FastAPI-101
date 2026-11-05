# FastAPI Demo API

A reusable FastAPI blueprint containing practical implementations, code patterns, and backend concepts that can be referenced whenever starting a new FastAPI project.

This repository serves as a personal collection of reusable FastAPI implementations, helping reduce repetitive setup work and providing a consistent starting point for building APIs.

## Overview

This repository demonstrates two practical API implementations:

- **Patient Management API:** A REST API demonstrating CRUD operations, Pydantic models, request validation, computed fields, exception handling, and JSON-based data persistence.
- **Insurance Premium Prediction API:** An ML-powered API demonstrating model integration, input validation, feature engineering, computed fields, and predictions using a trained machine learning model.

The goal is to maintain a reusable reference for common FastAPI concepts and backend development patterns.

## Project Structure

```text
FastAPI_Tutorial/
│
├── app.py                      # Insurance prediction API
├── main.py                     # Patient management API
├── frontend.py                 # Streamlit frontend
│
├── fastapi_ml_model.ipynb      # ML model development notebook
├── insurance.csv               # Insurance dataset
├── model.pkl                   # Serialized ML model
│
├── patient.json                # Patient records (JSON storage)
│
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git exclusion rules
├── LICENSE                     # Repository license
└── README.md                   # Project documentation
```

## File-by-File Explanation

| File | Description |
|---|---|
| `app.py` | Implements the Insurance Premium Prediction API. Loads the trained ML model, validates incoming data using Pydantic, calculates derived features, and predicts the insurance premium category. |
| `main.py` | Implements the Patient Management API with endpoints for creating, viewing, updating, deleting, and sorting patient records. |
| `frontend.py` | Provides a Streamlit-based user interface for entering user details and sending prediction requests to the Insurance API. |
| `fastapi_ml_model.ipynb` | Jupyter Notebook used for developing the machine learning model and exploring the insurance prediction workflow. |
| `insurance.csv` | Dataset associated with the insurance premium prediction project. |
| `model.pkl` | Serialized machine learning model loaded by `app.py` for making predictions. |
| `patient.json` | Stores patient records used by the Patient Management API. |
| `requirements.txt` | Contains the Python dependencies and their pinned versions required to run the project. |
| `.gitignore` | Prevents unnecessary files such as virtual environments, Python cache, environment variables, and IDE configurations from being tracked by Git. |
| `LICENSE` | Defines the licensing terms for using and distributing the repository. |

## Implementations

### 1. Patient Management API

Implemented in `main.py`.

A REST API that manages patient records using JSON as its data storage mechanism.

**Features:**

- Create new patient records.
- Retrieve all patient records.
- Retrieve individual patient records using their ID.
- Update existing patient information.
- Delete patient records.
- Sort patient records by height, weight, or BMI.
- Validate incoming requests using Pydantic.
- Calculate BMI and automatically determine the BMI category.
- Handle invalid requests using HTTP exceptions.

**Available Endpoints:**

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/about` | API information |
| GET | `/view` | Retrieve all patients |
| GET | `/patient/{patient_id}` | Retrieve a specific patient |
| GET | `/sort` | Sort patient records |
| POST | `/create` | Create a patient |
| PUT | `/update/{patient_id}` | Update patient information |
| DELETE | `/delete/{patient_id}` | Delete a patient |

**Sorting Example:**

```http
GET /sort?sort_by=height&order=asc
```

Supported sorting fields:

- `height`
- `weight`
- `bmi`

Supported ordering:

- `asc`
- `desc`

### 2. Insurance Premium Prediction API

Implemented in `app.py`.

An ML-powered API that predicts an insurance premium category based on user information and a previously trained machine learning model.

**Features:**

- Load a serialized ML model using Pickle.
- Validate incoming data using Pydantic.
- Apply field-level validation using `Annotated` and `Field`.
- Calculate BMI automatically using computed fields.
- Determine lifestyle risk based on BMI and smoking habits.
- Categorize users into age groups.
- Determine city tiers based on predefined city lists.
- Convert validated input into a Pandas DataFrame.
- Generate predictions using the trained ML model.

**Prediction Endpoint:**

| Method | Endpoint | Description |
|---|---|---|
| POST | `/predict` | Predict insurance premium category |

**Example Request:**

```json
{
    "age": 30,
    "weight": 65,
    "height": 1.7,
    "income_lpa": 10,
    "smoker": false,
    "city": "Mumbai",
    "occupation": "private_job"
}
```

**Example Response:**

```json
{
    "predicted_category": "..."
}
```

The predicted category depends on the trained model.

### 3. Streamlit Frontend

Implemented in `frontend.py`.

A simple frontend that collects user information and sends a POST request to the Insurance Premium Prediction API.

**Features:**

- Collect age, weight, height, and annual income.
- Capture smoking status, city, and occupation.
- Send user input to the FastAPI prediction endpoint.
- Display API responses and connection errors.

The frontend communicates with:

```text
http://localhost:8000/predict
```

Note: The current frontend expects a nested `response` object containing confidence and class probabilities, whereas `app.py` currently returns `predicted_category` directly. The response handling needs to be aligned for the prediction result to display correctly.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API development |
| Pydantic | Data validation and serialization |
| Uvicorn | ASGI server |
| Pandas | Data manipulation |
| Scikit-learn | Machine learning model integration |
| Pickle | Model serialization |
| Streamlit | Frontend development |
| Requests | HTTP communication |
| JSON | Patient data persistence |

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Pratham1603/FastAPI_demo_API-.git
```

### 2. Navigate to the Project Directory

```bash
cd FastAPI_demo_API-
```

### 3. Create a Virtual Environment

```bash
python -m venv myenv
```

Activate the environment.

**Windows (CMD):**

```cmd
myenv\Scripts\activate
```

**macOS / Linux:**

```bash
source myenv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

This repository contains two independent FastAPI applications. Run the one you want to work with.

**Patient Management API:**

```bash
uvicorn main:app --reload
```

**Insurance Premium Prediction API:**

```bash
uvicorn app:app --reload
```

Make sure to run these commands from the project root directory so the JSON and Pickle files can be located.

### 6. Run the Streamlit Frontend

First, start the Insurance Premium Prediction API in one terminal.

Then open another terminal, activate the virtual environment, and execute:

```bash
streamlit run frontend.py
```

## API Documentation

FastAPI automatically generates interactive API documentation.

Once an API is running, access the following URLs:

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI Schema | http://127.0.0.1:8000/openapi.json |

You can use Swagger UI to test endpoints, inspect request schemas, and view API responses directly from your browser.

## Key FastAPI Concepts Covered

| Concept | Implementation |
|---|---|
| FastAPI Application | `FastAPI()` |
| HTTP Methods | GET, POST, PUT, DELETE |
| Pydantic Models | `BaseModel` |
| Field Validation | `Field()` |
| Advanced Type Hints | `Annotated` |
| Optional Fields | `Optional` |
| Restricted Values | `Literal` |
| Computed Fields | `@computed_field` |
| Path Parameters | `Path()` |
| Query Parameters | `Query()` |
| HTTP Exceptions | `HTTPException` |
| JSON Responses | `JSONResponse` |
| Serialization | `model_dump()` |
| Partial Updates | `exclude_unset=True` |
| Data Persistence | JSON |
| ML Model Integration | Pickle and Scikit-learn |

## Learning Resource

For a deeper understanding of FastAPI fundamentals, API design principles, and building production-ready APIs, check out my Medium article:

**[Building Production-Ready APIs: A First-Principles FastAPI Guide](https://medium.com/@prathamharer1603/building-production-ready-apis-a-first-principles-fastapi-guide-4120aa058267)**

## Author

**Pratham Harer**

- GitHub: [@Pratham1603](https://github.com/Pratham1603)
- Medium: [@prathamharer1603](https://medium.com/@prathamharer1603)

---

This repository is intended to evolve as a reusable FastAPI reference. New implementations, concepts, and backend patterns can be added as development experience grows.
