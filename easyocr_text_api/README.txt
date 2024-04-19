1) Install dependencies:

pip install easyocr
pip install fastapi
pip install uvicorn

2) Start server:

uvicorn main:app --reload


3) Send request: 

http://127.0.0.1:8000/get-card-data?image=real_id.jpg

where "real_id.jpg" is name of image present in same directory as main.py

Output will be in json format
