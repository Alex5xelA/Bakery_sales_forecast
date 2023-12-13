from fastapi import FastAPI, UploadFile, File
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from bakery_sales.modeling import prediction

from darts.models.forecasting.tft_model import TFTModel

app = FastAPI()

# specify path to pytorch model .pt file
pt_file_path = 'weights/tft_tuning_2.pt'
# new tft model

# load pytorch model and set to eval mode
model = TFTModel.load(pt_file_path)
# model.eval()

app.state.model = model

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

    
@app.post("/upload")
def upload_files(files: List[UploadFile] = File(...)):
    dataframes = []
    for file in files:
        df = pd.read_csv(file.file)
        file.file.close()
        dataframes.append(df)
    pred = prediction(dataframes[0], dataframes[1], app.state.model)
    return {"output": pred}


@app.get("/")
def root():
    return {'greeting': 'Hello'}
