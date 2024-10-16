import pandas as pd
import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
import io

app = FastAPI()

# Setting up the templates directory for HTML files
templates = Jinja2Templates(directory="templates")

# Static files (for CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Function to generate random data for the DataFrame
def generate_random_data():
    names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivy', 'Jack']
    scores = [random.uniform(70, 100) for _ in range(10)]  # Random scores between 70 and 100
    passed = ['Yes' if score >= 80 else 'No' for score in scores]  # Pass if score >= 80
    complete = [random.choice([True, False]) for _ in range(10)]  # Random checkbox state (complete or not)
    df = pd.DataFrame({
        'ID': list(range(1, 11)),
        'Name': names,
        'Score': [round(score, 1) for score in scores],  # Round to 1 decimal place
        'Passed': passed,
        'Complete': complete
    })
    return df


# Main route for rendering the page
@app.get("/", response_class=HTMLResponse)
async def get_table(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Route to get updated table data as JSON
@app.get("/data", response_class=JSONResponse)
async def get_data():
    df = generate_random_data()
    data = df.to_dict(orient="records")
    return {"data": data}


# Route to handle CSV download
@app.get("/download_csv")
async def download_csv():
    df = generate_random_data()  # Use the same data generation function

    # Convert DataFrame to CSV format
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv"
                                )
    response.headers["Content-Disposition"] = "attachment; filename=table_data.csv"
    return response
