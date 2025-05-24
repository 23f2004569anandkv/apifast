from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET"],  # Only allow GET requests
    allow_headers=["*"],
)

# Load the CSV file
df = pd.read_csv("q-fastapi.csv")

# Function to filter students based on class
def get_students_data(class_filters: Optional[List[str]] = None):
    if class_filters:
        # Filter dataframe for selected classes
        filtered_df = df[df["class"].isin(class_filters)]
    else:
        filtered_df = df

    # Convert to list of dictionaries (maintains original CSV order)
    students = filtered_df.to_dict(orient="records")
    
    return students

# API route to fetch student data based on class filter
@app.get("/api")
async def get_students(class_param: Optional[List[str]] = Query(None, alias="class")):
    """
    Get student data.
    - Optional query parameter 'class' filters students by class.
    - Example: /api?class=1A&class=1B
    - Students are returned in the original CSV order.
    """
    students = get_students_data(class_param)
    return {"students": students}

# Root route for API info
@app.get("/")
async def root():
    return {"message": "Student API is running. Use /api endpoint to get student data."}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
