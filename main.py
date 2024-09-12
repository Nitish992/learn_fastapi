from fastapi import FastAPI, UploadFile, HTTPException,status
import pandas as pd
from io import StringIO
from route import router as r

app = FastAPI()

app.include_router(r)

@app.get("/")
async def home():
    return {"Message" : "Welcome to magic covert. Go to /convert to convert files."}


@app.post("/convert")
async def convert(file: UploadFile):
    # If the file is json
    if file.content_type == "application/json":
        # Reading the json file
        json_data = await file.read()

        # Converting to json string
        json_string = json_data.decode()
        
        # To pandas dataframe to easily convert to csv
        df = pd.read_json(json_string)

        # Converting to csv and saving the file
        df.to_csv('data.csv', encoding='utf-8', index=False)

        return {'message' : 'Sucessfully converted to csv file.'}

    elif file.content_type == "text/csv":
        # If the file is csv
        if file.content_type == "text/csv":
            # Reading the csv file
            csv_data = await file.read()
  
            # to csv string
            csv_str = csv_data.decode('utf-8')

            # To csv buffer as pandas need buffer
            csv_buffer = StringIO(csv_str)
 
            # To pandas data frame from buffer
            df = pd.read_csv(csv_buffer)
        
            # To json and saving the file
            df.to_json('data.json', orient='records', indent=4)
    
            return {'message' : 'Sucessfully converted to json file.'}
    
    else:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = 'Invalid file type. Only supported - json or csv.')