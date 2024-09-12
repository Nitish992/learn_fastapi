from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db, ParsedData
from models import DataOut
from typing import List, Optional

router = APIRouter(tags=["Get data from db"])

@router.get("/data", response_model = List[DataOut])
async def get_data(user_id: Optional[str] = None, db: Session = Depends(get_db)):

    query = select(ParsedData)
    
    if user_id:
        query = query.where(ParsedData.user_id == user_id)
    
    results = db.execute(query).scalars().all()
    
    if not results:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data found")
    
    return results  
