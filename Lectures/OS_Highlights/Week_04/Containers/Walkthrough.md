```yaml
title: "Lab Manual — Containerized Student Grades API"
audience: "Graduate OS / Systems Lab"
components: ["FastAPI", "MongoDB or Redis", "Docker", "Docker Compose"]
source: "ChatGPT"
format: "Step-by-step Lab Manual"
```

# 🧪 **Lab Manual — Containerized Student Grades API (FastAPI + Database + Docker)**

---

# 🧭 **Lab Goals**

By completing this lab, you will:

- Build a **FastAPI** microservice
- Connect it to a **MongoDB or Redis** database
- Run everything using **Docker Compose**
- Persist data using **Docker volumes**
- Demonstrate **inter-container networking**
- Observe OS mechanisms like namespaces, mount layers, and networking isolation

---

# 📁 **Part 1 — Set Up Your Lab Environment**

### 1. Create a project folder:

```bash
mkdir grades-lab
cd grades-lab
```

### 2. Create the folder structure:

```bash
mkdir app
touch app/main.py Dockerfile requirements.txt docker-compose.yml
```

---

# 📘 **Part 2 — Choose Your Database Path**

You will choose **ONE** of the two database backends:

## **Option A — MongoDB (recommended for multi-record data)**

Use if you want:

- multiple grades per student
- document storage
- rich querying

## **Option B — Redis (good for simple, latest-value storage)**

Use if you want:

- key–value storage
- one grade per student
- fast caching-like behavior

_(The lab steps diverge slightly depending on your choice. Follow the section that matches your selection.)_

---

# 🧰 **Part 3 — Write the FastAPI Application**

Inside `app/main.py`, paste the appropriate version:

---

## **3A — FastAPI + MongoDB Version**

```python
from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List
import os

# Models
class GradeIn(BaseModel):
    student_id: str
    course_code: str
    assignment: str
    score: float
    max_score: float

class GradeOut(GradeIn):
    id: str = Field(default=None, alias="_id")

app = FastAPI(title="Mongo Grades API")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.getenv("MONGO_DB", "grades_db")

@app.on_event("startup")
async def startup_db():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URI)
    app.db = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown_db():
    app.mongodb_client.close()

def get_collection():
    return app.db["grades"]

@app.post("/grades/", response_model=GradeOut)
async def create_grade(grade: GradeIn, grades=Depends(get_collection)):
    result = await grades.insert_one(grade.model_dump())
    created = await grades.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created

@app.get("/grades/{student_id}", response_model=List[GradeOut])
async def get_grades(student_id: str, grades=Depends(get_collection)):
    docs = await grades.find({"student_id": student_id}).to_list(100)
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

@app.delete("/grades/{student_id}")
async def del_grades(student_id: str, grades=Depends(get_collection)):
    result = await grades.delete_many({"student_id": student_id})
    return {"deleted": result.deleted_count}
```

---

## **3B — FastAPI + Redis Version**

```python
import os, json
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Grade(BaseModel):
    student_id: str
    course_code: str
    assignment: str
    score: float
    max_score: float

app = FastAPI(title="Redis Grades API")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")

@app.on_event("startup")
async def startup():
    app.redis = redis.Redis(host=REDIS_HOST, decode_responses=True)

@app.on_event("shutdown")
async def shutdown():
    await app.redis.close()

@app.post("/grades/")
async def set_grade(grade: Grade):
    key = f"grade:{grade.student_id}"
    await app.redis.set(key, grade.model_dump_json())
    return grade

@app.get("/grades/{student_id}")
async def get_grade(student_id: str):
    key = f"grade:{student_id}"
    raw = await app.redis.get(key)
    if not raw:
        raise HTTPException(404, "Not found")
    return json.loads(raw)

@app.delete("/grades/{student_id}")
async def del_grade(student_id: str):
    deleted = await app.redis.delete(f"grade:{student_id}")
    return {"deleted": bool(deleted)}
```

---

# 🐳 **Part 4 — Requirements & Dockerfile**

Create `requirements.txt`:

```
fastapi
uvicorn[standard]
motor          # Mongo version only
redis[hiredis] # Redis version only
pydantic
```

> _Include only what your chosen DB requires._

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# 🐋 **Part 5 — Docker Compose Setup**

Option A or B depending on your DB:

---

## **5A — MongoDB Compose File**

`docker-compose.yml`:

```yaml
version: "3.9"

services:
  api:
    build: .
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

---

## **5B — Redis Compose File**

```yaml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
    networks:
      - backend

  redis:
    image: redis:7
    command: ["redis-server", "--save", "60", "1"]
    volumes:
      - redis_data:/data
    networks:
      - backend

volumes:
  redis_data:

networks:
  backend:
```

---

# ▶️ **Part 6 — Run Everything**

```bash
docker compose up --build
```

Then visit:

```
http://localhost:8000/docs
```

This opens Swagger UI for interacting with the API.

---

# 🧪 **Part 7 — Test the API with curl**

### 1. Create a grade

```bash
curl -X POST http://localhost:8000/grades/ \
 -H "Content-Type: application/json" \
 -d '{"student_id":"s1","course_code":"CS-5303","assignment":"HW1","score":95,"max_score":100}'
```

### 2. Read it back

Mongo:

```bash
curl http://localhost:8000/grades/s1
```

Redis:

```bash
curl http://localhost:8000/grades/s1
```

### 3. Delete

```bash
curl -X DELETE http://localhost:8000/grades/s1
```

---

# 💾 **Part 8 — Persistence Verification**

### Step A — Add data

```bash
docker compose up
```

Use `/grades/` POST to add data.

### Step B — Stop stack (data should persist)

```bash
docker compose down
```

### Step C — Restart

```bash
docker compose up
```

### Step D — Verify data still exists

```bash
curl http://localhost:8000/grades/s1
```

### Step E — Delete volume (data should vanish)

```bash
docker compose down -v
docker compose up
curl http://localhost:8000/grades/s1  # expect 404
```

---

# 🛰️ **Part 9 — Networking Verification**

### 1. Show containers

```bash
docker ps
```

### 2. Exec into API container & ping DB

Mongo:

```bash
docker exec -it <api-container> ping -c 2 mongo
```

Redis:

```bash
docker exec -it <api-container> ping -c 2 redis
```

### 3. Check networks

```bash
docker network ls
docker network inspect grades-lab_backend
```

---

# 🧠 **Part 10 — OS Concepts to Observe**

Students should record observations about:

### **Namespaces**

- PID difference (container PID = 1, host PID ≠ 1)
- Different network interfaces (eth0 vs host)
- Different filesystem root (`/` inside container)

### **Cgroups**

- Optional: run API with `--cpus=0.5` or memory limit

### **Mount namespaces + volumes**

- DB data stored outside the ephemeral container layer

### **Inter-container DNS**

- `mongo` or `redis` resolves via user-defined network

---

# 📝 **Part 11 — Lab Report Requirements (not required)**

Your report should contain:

- Architecture diagram (API ↔ DB ↔ Volume ↔ Host)
- Evidence of:
  - API tests
  - Persistence
  - Inter-container networking
  - Volume behavior
- Short discussion on:
  - How containers differ from VMs
  - How DB persistence is achieved
  - Why volumes bypass the writable layer

---

# 🎉 **Lab Complete!**

This lab translates the theory of container isolation, networking, and volumes into a real, working microservice you can build, run, inspect, break, and fix.
