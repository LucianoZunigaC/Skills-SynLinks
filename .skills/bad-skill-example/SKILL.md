---
name: backend-guidelines
description: "general guidelines for the backend using python and fastapi"
metadata:
  author: aki-team
  version: 1.0.0
---

# Backend Guidelines

## Purpose
This skill contains the rules for writing backend code.

## When to Use This Skill
Use this skill when you are writing code for the backend in Python using FastAPI.

## Instructions
When writing backend code, always follow these rules:
1. Make sure to use type hints everywhere.
2. We use Pydantic for validation, so use Pydantic models.
3. Don't write slow queries to the database.
4. Name your variables clearly.
5. All endpoints need to handle errors properly and return standard HTTP status codes like 400 for bad requests.

## Examples
Here is an example of an endpoint:
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # get user from db here
    return {"id": user_id, "name": "John"}
```

If you get an error, check your code and the logs.
