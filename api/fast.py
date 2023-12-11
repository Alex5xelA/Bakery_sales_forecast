from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import csv
import codecs

from bakery_sales.modeling import model

app = FastAPI()

app.state.model = model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

    
@app.post("/upload")
def upload(file: UploadFile = File(...)):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    data = {}
    for rows in csvReader:             
        key = rows[['traditional_baguette']]  # Assuming a column named 'Id' to be the primary key
        data[key] = rows
    
    file.file.close()
    data.pd_dataframe()
    return data

@app.get("/")
def root():
    return {'greeting': 'Hello'}