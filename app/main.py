from fastapi import FastAPI
from lib.score import getScore
from lib.difficult import getDifficult

app = FastAPI()

@app.get('/')
def index(name):
    return {'message': 'Hello, ' + name}

@app.get('/ocr/score')
def score(url, psm):
    return getScore(url, psm)

@app.get('/ocr/difficult')
def difficult(url, psm):
    return getDifficult(url, psm)
