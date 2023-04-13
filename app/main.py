from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from lib.score import getScore
from lib.difficult import getDifficult
from lib.title import getTitle
from lib.judge import getJudge

from lib.candidate import candidateDifficult
from lib.candidate import candidateTitle

import requests
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def index(name:str):
    return {"message": "Hello,{}!".format(name)}

@app.get('/ocr/score')
def score(url, psm):
    return getScore(url, psm)

@app.get('/ocr/difficult') 
def difficult(url, psm):
    return getDifficult(url, psm)

@app.get('/ocr/title')
def title(url, psm, border):
    return getTitle(url, psm, border)

@app.get('/ocr/judge')
def judge(url, psm, border):
    return getJudge(url, psm, border)

@app.get('/candidate/difficult')
def candidate_difficult(data):
    return {'candidate': candidateDifficult(data)}

@app.get('/candidate/title')
def candidate_title(data, ratio):
    return {'candidate': candidateTitle(data, ratio)}
