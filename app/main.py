from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index(name):
    return {'message': 'Hello, ' + name}
