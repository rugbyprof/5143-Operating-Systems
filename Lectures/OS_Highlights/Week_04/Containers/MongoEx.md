```yaml
title: "FastAPI + MongoDB: Persisting Student Grades"
section: "Mini Tutorial"
stack: ["FastAPI", "MongoDB", "Docker Compose"]
example_domain: "student_grades"
source: "ChatGPT"
```

Below is a **small but complete** tutorial using **FastAPI + MongoDB** in containers, with **persistent data** (e.g., student grades).

---

## 1. Goal / Architecture

We’ll build:

- A **FastAPI** service (Python)
- A **MongoDB** database
- Both wired together via **Docker Compose**
- MongoDB’s data stored in a **named volume** so it persists across container restarts

Data model (simplified):

```text
StudentGrade:
  student_id: string
  course_code: string
  assignment: string
  score: float
  max_score: float
```

---

## 2. Folder Structure

Create a new project folder, e.g. `fastapi-grades/`:

```text
fastapi-grades/
├── app/
│   ├── main.py
│   └── models.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 3. Python Dependencies

`requirements.txt`:

```txt
fastapi
uvicorn[standard]
motor  # async MongoDB driver
pydantic
```

(You can add `python-dotenv` later if you want env file support.)

---

## 4. Data Model (Pydantic)

`app/models.py`:

```python
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# Helper so we can serialize Mongo's ObjectId to string if needed
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class GradeIn(BaseModel):
    student_id: str = Field(..., example="s12345")
    course_code: str = Field(..., example="CS-5303")
    assignment: str = Field(..., example="Homework 1")
    score: float = Field(..., example=92.5)
    max_score: float = Field(..., example=100.0)


class GradeOut(GradeIn):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        # allow MongoDB's `_id` field to map to our Pydantic model
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
```

You can simplify if you don’t care about returning `_id`, but this is a clean “real-ish” version.

---

## 5. FastAPI App with Mongo Connection

`app/main.py`:

```python
from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
import os

from .models import GradeIn, GradeOut

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.getenv("MONGO_DB", "grades_db")

app = FastAPI(title="Student Grades API")

# We'll store the client on app state
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URI)
    app.mongodb = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


def get_grades_collection():
    return app.mongodb["grades"]


@app.get("/")
async def root():
    return {"message": "Student Grades API is running"}


@app.post("/grades/", response_model=GradeOut)
async def create_grade(grade: GradeIn, grades_collection=Depends(get_grades_collection)):
    grade_doc = grade.dict()
    result = await grades_collection.insert_one(grade_doc)
    created = await grades_collection.find_one({"_id": result.inserted_id})
    return GradeOut(**created)


@app.get("/grades/{student_id}", response_model=List[GradeOut])
async def get_grades_for_student(student_id: str, grades_collection=Depends(get_grades_collection)):
    cursor = grades_collection.find({"student_id": student_id})
    grades = await cursor.to_list(length=1000)
    return [GradeOut(**g) for g in grades]


@app.delete("/grades/{student_id}", response_model=dict)
async def delete_grades_for_student(student_id: str, grades_collection=Depends(get_grades_collection)):
    result = await grades_collection.delete_many({"student_id": student_id})
    return {"deleted_count": result.deleted_count}
```

Key points:

- `mongo:27017` is the hostname of the MongoDB container (defined in Compose).
- Grades are stored in the `grades` collection within `grades_db`.

---

## 6. Dockerfile for FastAPI Service

`Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Work directory inside the container
WORKDIR /app

# Install system deps (optional, but often handy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Expose port FastAPI will run on
EXPOSE 8000

# Start the app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 7. Docker Compose (App + Mongo + Persistence)

`docker-compose.yml`:

```yaml
version: "3.9"

services:
  api:
    build: .
    container_name: grades-api
    ports:
      - "8000:8000"
    environment:
      - MONGO_URI=mongodb://mongo:27017
      - MONGO_DB=grades_db
    depends_on:
      - mongo
    networks:
      - backend

  mongo:
    image: mongo:7
    container_name: grades-mongo
    restart: always
    volumes:
      - mongo_data:/data/db
    networks:
      - backend

volumes:
  mongo_data:

networks:
  backend:
```

Notes:

- `mongo_data` is a **named volume** → data persists even if the MongoDB container is recreated.
- `backend` network → containers can talk using hostnames `api` and `mongo`.
- FastAPI container maps `8000` → host port `8000`.

---

## 8. Running the Stack

From the project root (`fastapi-grades/`):

```bash
docker compose up --build
```

Then open the browser at:

- Swagger UI: <http://localhost:8000/docs>
- Root endpoint: <http://localhost:8000/>

You’ll see the interactive FastAPI docs and can test endpoints there.

---

## 9. Testing with `curl` (or `httpie`)

### 9.1 Create a grade

```bash
curl -X POST "http://localhost:8000/grades/" \
  -H "Content-Type: application/json" \
  -d '{
        "student_id": "s12345",
        "course_code": "CS-5303",
        "assignment": "HW1",
        "score": 95.0,
        "max_score": 100.0
      }'
```

### 9.2 Fetch grades for a student

```bash
curl "http://localhost:8000/grades/s12345"
```

You should get a JSON array with that grade.

### 9.3 Delete all grades for a student

```bash
curl -X DELETE "http://localhost:8000/grades/s12345"
```

---

## 10. Verifying Persistence

1. With the stack running, add a few grade records.
2. Stop the containers (data **should remain**):

   ```bash
   docker compose down
   ```

3. Bring them back up:

   ```bash
   docker compose up
   ```

4. Call:

   ```bash
   curl "http://localhost:8000/grades/s12345"
   ```

You should still see the grades.  
They are stored in the `mongo_data` volume mapped to `/data/db` in the Mongo container.

---

## 11. Connecting Back to OS / Containers Concepts

This little stack hits a bunch of the things you’ve been walking through:

- **Inter-container networking**
  - `api` ↔ `mongo` via the `backend` network and DNS names
- **Persistence via volumes**
  - `mongo_data` → survives container restarts
- **Namespaces & cgroups (under the hood)**
  - Each container has its own network + mount namespaces
  - Mongo and FastAPI are just groups of processes with isolation
