# app.py
# Create a FastAPI endpoint ar route localhost/swuare for function square that returns the squared value of the variable input of the payload json
# 2023-11-17, J J. Köppern

# Import statements
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define a Pydantic model for request data validation
class InputMode(BaseModel):
    input: float

# Create an instance of the FastAPI class
app = FastAPI()

# Define the endpoint /square
@app.post("/square")
def square(data: InputMode):
    # Calculate the square of the input
    squared_value = data.input ** 2

    return {"squared_value": squared_value}

