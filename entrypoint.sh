#!/bin/bash

uvicorn FastAPI.src.main:app --port $PORT --host 0.0.0.0