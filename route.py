from fastapi import APIRouter

router = APIRouter(tags= ['first tag'], prefix= '/myprefix')

router.get('/test')
async def home():
    return {"Message" : "Welcome to magic covert. Go to /convert to convert files."}

router.post('/test1')
async def home():
    return {"Message" : "Welcome to magic covert. Go to /convert to convert files."}