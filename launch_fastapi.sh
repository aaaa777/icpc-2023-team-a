if [ "$(which uvicorn)" != "FastAPI/venv/bin/uvicorn" ]
  then . FastAPI/venv/bin/activate
fi
uvicorn FastAPI.src.main:app --reload