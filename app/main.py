from fastapi import FastAPI
from lib.score import getScore

app = FastAPI()

@app.get('/')
def index(name):
    return {'message': 'Hello, ' + name}

@app.get('/ocr/score')
def score(url, psm):
    return getScore(url, psm)
