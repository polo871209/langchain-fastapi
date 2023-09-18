Install requirements
```shell
# python version 3.11
pip install -r requirements.txt
```
start server
```shell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Hierarchy
```shell
├── migrations # db migration folder
├── alembic.ini # db migration ini
├── requirements.txt # project requirements
├── app
│   ├── __init__.py 
│   ├── database.py # db session
│   ├── main.py 
│   ├── models.py # db models
│   ├── oauth.py # api key auth
│   ├── routers # router folders
│   └── utils # tools/utils folders
└── vertex-svc.json # vertex service account json
```