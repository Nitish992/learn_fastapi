from fastapi import FastAPI, UploadFile, HTTPException, status, Depends
from database import get_db, ParsedData
from models import UserDataIn
from sqlalchemy.orm import Session
from io import StringIO
import pandas as pd
from route import router

app = FastAPI()

app.include_router(router)

@app.get("/")
async def home():
    return {"message" : "Magic Convert - A simple API built using FastAPI that allows for converting CSV files to JSON and vice versa."}



@app.post("/convert")
async def convert(file: UploadFile, db: Session = Depends(get_db)):
    try:
        # If file type is application/json
        if file.content_type == "application/json":

            # Reading the JSON data
            json_data = await file.read()

            # Parsing the JSON data to JSON string
            json_string = json_data.decode()

            # From JSON string to pandas dataframe
            df = pd.read_json(StringIO(json_string))

            # Converting to csv and saving the file
            df.to_csv('data/data.csv', encoding='utf-8', index=False)

            # Validate and insert the data
            try:
                for _, row in df.iterrows():

                    # Validate the input data with Pydantic model
                    user_data = UserDataIn(**row.to_dict())

                    # User data to sql model
                    new_entry = ParsedData(
                        name=user_data.name,
                        language=user_data.language,
                        user_id=user_data.user_id,
                        bio=user_data.bio,
                        version=user_data.version
                    )

                    # Add the new entry
                    db.add(new_entry)

                # Commit the changes
                db.commit()

            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Data insertion failed: {e}")
            
            return {"message": "Successfully parsed and saved JSON data."}

        # If the file type is csv
        elif file.content_type == "text/csv":

            # Reading the CSV data
            csv_data = await file.read()

            # Parsing the CSV data
            csv_str = csv_data.decode('utf-8')

            # From csv to pandas dataframe
            df = pd.read_csv(StringIO(csv_str))
            
            # To json and saving the file
            df.to_json('data/data.json', orient='records', indent=4)
            
            # Validate and insert the data
            try:
                for _, row in df.iterrows():

                    # Validate the input data with Pydantic model
                    user_data = UserDataIn(**row.to_dict())

                    # Insert the validated data into the database
                    to_insert = ParsedData(
                        name=user_data.name,
                        language=user_data.language,
                        user_id=user_data.user_id,
                        bio=user_data.bio,
                        version=user_data.version
                    )

                    # Add new entry
                    db.add(to_insert)
                
                # Commit the changes
                db.commit()

            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Data insertion failed: {e}")
            
            return {"message": "Successfully parsed and saved CSV data."}

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Only supported - JSON or CSV.")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Something Went Wrong: {e}")


    
