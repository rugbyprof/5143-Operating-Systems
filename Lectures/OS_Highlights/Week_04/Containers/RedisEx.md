```yaml
title: "FastAPI + Redis: Caching Student Grades (with Persistence)"
section: "Mini Tutorial"
stack: ["FastAPI", "Redis", "Docker Compose"]
domain: "student_grades_cache"
source: "ChatGPT"
```

_Below is a **small, parallel tutorial** to the MongoDB version, but using **Redis**._

- Focus: **simple grade storage / cache** with **persistence** via Redis + Docker volume.
- Good for: showing **key–value data**, **inter-container networking**, and **volumes**.

---

## 1. Goal / Architecture

We’ll build:

- A **FastAPI** service (Python)
- A **Redis** instance
- Both wired together with **Docker Compose**
- Redis data will persist using a **named Docker volume** (mapped to `/data`)

Simple data model:

- A single key per student:
  - key: `grade:<student_id>`
  - value: JSON string with grade info

Example value:

```json
{
  "course_code": "CS-5303",
  "assignment": "HW1",
  "score": 95.0,
  "max_score": 100.0
}
```

---

## 2. Folder Structure

Create a new project folder, e.g. `fastapi-redis-grades/`:

```text
fastapi-redis-grades/
├── app/
│   └── main.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

(Simpler than the Mongo version: no separate `models.py` needed unless you want it.)

---

## 3. Python Dependencies

`requirements.txt`:

```txt
fastapi
uvicorn[standard]
redis[hiredis]   # includes asyncio support
pydantic
```

---

## 4. FastAPI App Using Redis

`app/main.py`:

```python
import os
import json
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import redis.asyncio as redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB   = int(os.getenv("REDIS_DB", "0"))

app = FastAPI(title="Student Grades (Redis)")

# Pydantic model for incoming grade data
class Grade(BaseModel):
    student_id: str = Field(..., example="s12345")
    course_code: str = Field(..., example="CS-5303")
    assignment: str = Field(..., example="HW1")
    score: float = Field(..., example=95.0)
    max_score: float = Field(..., example=100.0)


@app.on_event("startup")
async def startup_event():
    # Create a single shared async Redis client
    app.state.redis = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,  # return strings instead of bytes
    )


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis.close()


def _grade_key(student_id: str) -> str:
    return f"grade:{student_id}"


@app.get("/")
async def root():
    return {"message": "Redis-backed Student Grades API is running"}


@app.post("/grades/", response_model=Grade)
async def set_grade(grade: Grade):
    """
    Store or update the latest grade for a student in Redis.
    """
    r = app.state.redis
    key = _grade_key(grade.student_id)
    # Store as JSON string
    await r.set(key, grade.model_dump_json())
    return grade


@app.get("/grades/{student_id}", response_model=Grade)
async def get_grade(student_id: str):
    """
    Get the latest grade for a student from Redis.
    """
    r = app.state.redis
    key = _grade_key(student_id)
    value = await r.get(key)

    if value is None:
        raise HTTPException(status_code=404, detail="Grade not found")

    # Parse JSON back into Grade model
    data = json.loads(value)
    return Grade(**data)


@app.delete("/grades/{student_id}")
async def delete_grade(student_id: str):
    """
    Delete the grade for a student from Redis.
    """
    r = app.state.redis
    key = _grade_key(student_id)
    deleted = await r.delete(key)
    return {"deleted": bool(deleted)}
```

Key points:

- Uses `redis.asyncio` so it plays nicely with FastAPI’s async model.
- Stores grade JSON under `grade:<student_id>` keys.
- Perfect for showing _key–value_ semantics but still with structured data.

---

## 5. Dockerfile for FastAPI Service

`Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Same pattern as the Mongo example: thin Python image, install deps, run uvicorn.

---

## 6. Docker Compose (FastAPI + Redis + Volume)

`docker-compose.yml`:

```yaml
version: "3.9"

services:
  api:
    build: .
    container_name: redis-grades-api
    ports:
      - "8001:8000" # host:container
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_DB=0
    depends_on:
      - redis
    networks:
      - backend

  redis:
    image: redis:7
    container_name: redis-grades-db
    restart: always
    # Persist Redis data to a named volume
    volumes:
      - redis_data:/data
    command: ["redis-server", "--save", "60", "1", "--loglevel", "warning"]
    # --save 60 1 -> snapshot every 60s if at least 1 key changed
    networks:
      - backend

volumes:
  redis_data:

networks:
  backend:
```

Notes:

- `redis_data` is a **named volume** → persists data.
- Redis is configured with `--save 60 1` to write snapshots (RDB) to `/data/dump.rdb`.
- FastAPI uses `REDIS_HOST=redis`, which is the service (and DNS) name on the `backend` network.
- API exposed on **host port 8001** (so it doesn’t clash with the Mongo example if both are running).

---

## 7. Running the Stack

From `fastapi-redis-grades/`:

```bash
docker compose up --build
```

Then:

- Swagger UI: <http://localhost:8001/docs>
- Root: <http://localhost:8001/>

---

## 8. Testing with `curl`

### 8.1 Set a grade

```bash
curl -X POST "http://localhost:8001/grades/" \
  -H "Content-Type: application/json" \
  -d '{
        "student_id": "s99999",
        "course_code": "CS-5303",
        "assignment": "Project 1",
        "score": 88.5,
        "max_score": 100.0
      }'
```

You should get the same JSON back.

---

### 8.2 Get that grade

```bash
curl "http://localhost:8001/grades/s99999"
```

You should see:

```json
{
  "student_id": "s99999",
  "course_code": "CS-5303",
  "assignment": "Project 1",
  "score": 88.5,
  "max_score": 100.0
}
```

---

### 8.3 Delete the grade

```bash
curl -X DELETE "http://localhost:8001/grades/s99999"
```

Then verify it’s gone:

```bash
curl "http://localhost:8001/grades/s99999"
# -> 404
```

---

## 9. Verifying Redis Persistence

This is where you can make the **“persistence via volumes”** point very explicit.

1. Start the stack and set a grade as above.
2. Stop containers **without** removing the volume:

   ```bash
   docker compose down
   ```

3. Bring them back up:

   ```bash
   docker compose up
   ```

4. Check again:

   ```bash
   curl "http://localhost:8001/grades/s99999"
   ```

If enough time passed for the `--save 60 1` rule to trigger (or you adjust it), the grade should still be there.

You can emphasize:

- Redis is **in-memory**, but
- Docker’s volume (`redis_data`) + Redis’s persistence (RDB snapshot)  
  → makes data survive container restarts.

---

## 10. Where This Fits Conceptually

This tiny stack is a nice OS/container teaching bridge:

- **Inter-container networking**
  - `api` ↔ `redis` over `backend` network
  - name-based discovery (`redis` hostname)
- **Volumes**
  - `redis_data` mapped to `/data` inside Redis container
  - snapshot file `dump.rdb` persists there
- **Namespace & cgroups (under the hood)**
  - Separate process trees, network namespaces, mount namespaces
- **Different persistence story than Mongo**
  - Mongo: disk-based DB by default
  - Redis: in-memory, optional persistence (RDB/AOF)
  - Docker volume layer is the same conceptually

---

## 11. Quick Command Summary (Redis Version)

```bash
# Build and run the FastAPI + Redis stack
docker compose up --build

# View containers
docker ps

# View networks
docker network ls
docker network inspect fastapi-redis-grades_backend  # name may vary

# View volumes
docker volume ls
docker volume inspect fastapi-redis-grades_redis_data

# Stop stack (keep data)
docker compose down

# Remove stack + volumes (wipe data)
docker compose down -v
```

```yaml
section: "Appendix — Redis Version: Command Summary"
format: "Slide/PDF-ready"
tone: "neutral, concise"
source: "ChatGPT"
```

## 📎 **Appendix / Command Summary**

A compact, slide-ready reference for managing the **FastAPI + Redis** stack, inspecting networks/volumes, verifying persistence, and running tests.

---

## 🐳 **Docker Compose (Redis Version)**

### **Start the API + Redis stack**

```bash
docker compose up --build
```

### **Stop containers but keep the persistent Redis data**

```bash
docker compose down
```

### **Stop containers AND delete the Redis data volume**

```bash
docker compose down -v
```

---

## 📦 **Container & Image Management**

### **List running containers**

```bash
docker ps
```

### **List all containers (including stopped)**

```bash
docker ps -a
```

### **Stop a specific container**

```bash
docker stop <container-id-or-name>
```

### **Remove a specific container**

```bash
docker rm <container-id-or-name>
```

---

## 🗂️ **Redis Volume Operations**

### **List Docker volumes**

```bash
docker volume ls
```

### **Inspect the Redis data volume**

_(The name typically follows the pattern `<folder>_redis_data`)_

```bash
docker volume inspect fastapi-redis-grades_redis_data
```

### **Delete a specific volume**

```bash
docker volume rm fastapi-redis-grades_redis_data
```

---

## 🕸️ **Docker Network Operations**

### **List networks**

```bash
docker network ls
```

### **Inspect the app’s network**

(Replace `fastapi-redis-grades_backend` with the actual name.)

```bash
docker network inspect fastapi-redis-grades_backend
```

### **Determine which containers are attached**

Look under the `"Containers"` section in the inspect output.

---

## 🧾 **Logging Commands**

### **View FastAPI logs**

```bash
docker logs redis-grades-api
```

### **View Redis server logs**

```bash
docker logs redis-grades-db
```

### **Follow logs (streaming mode)**

```bash
docker logs -f redis-grades-api
```

---

# 🧪 **Testing the API (curl)**

### **Create or update a grade**

```bash
curl -X POST "http://localhost:8001/grades/" \
  -H "Content-Type: application/json" \
  -d '{
        "student_id": "s12345",
        "course_code": "CS-5303",
        "assignment": "HW1",
        "score": 90.5,
        "max_score": 100.0
      }'
```

### **Fetch the latest grade**

```bash
curl "http://localhost:8001/grades/s12345"
```

### **Delete a grade**

```bash
curl -X DELETE "http://localhost:8001/grades/s12345"
```

---

## 💾 **Persistence Verification Checklist**

1. Start the stack:
   ```bash
   docker compose up
   ```
2. POST a grade record.
3. Stop the stack (data should remain):
   ```bash
   docker compose down
   ```
4. Restart it:
   ```bash
   docker compose up
   ```
5. Confirm data still exists:
   ```bash
   curl "http://localhost:8001/grades/s12345"
   ```

If Redis’s persistence rules (`--save 60 1`, etc.) were met, the `dump.rdb` file is stored in the `redis_data` volume and survives restarts.
