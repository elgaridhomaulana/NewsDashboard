How to use this app?

## Initial Requirement
- You must install python in your machine
- You must install node v12.14.1 or above
- You must install npm v6.13.6 or above

Make sure to install all things that is needed in the initial requirement. After that you can:

1. Clone this repository
2. Go to the cloned directory

## Backend Section
- Go to backend folder
- Create virutal environment in backend directory `python -m venv env`
- Activate the environment `env\Scripts\activate`
- run `pip install -r requirements.txt`
- run `uvicorn main:app --reload` to run the api server

## Frontend Section
- Go to frontend/react-news folder
- run `npm install`
- run `npm start` to run the frontend server

### Note
If the react run in localhost port 3000 change origins in main.py that is located in backend folder .

```python
origins = [
    "http://localhost:3000"
]
```

