# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import tempfile
import time
import os
import psutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    language: str

@app.post("/execute")
async def execute_code(req: CodeRequest):
    if req.language != "python":
        return {"output": "Only Python is supported in this version.", "ecoScore": 0, "metrics": {}}

    # Write code to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
        tmp_file.write(req.code.encode("utf-8"))
        tmp_filename = tmp_file.name

    # Measure before
    start_time = time.time()
    process = psutil.Process(os.getpid())
    cpu_before = psutil.cpu_percent(interval=None)
    mem_before = process.memory_info().rss / (1024 ** 2)  # MB

    try:
        result = subprocess.run(["python", tmp_filename], capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr
    except Exception as e:
        output = str(e)

    # Measure after
    end_time = time.time()
    cpu_after = psutil.cpu_percent(interval=None)
    mem_after = process.memory_info().rss / (1024 ** 2)  # MB
    temp = psutil.sensors_temperatures().get('coretemp', [{}])[0].get('current', None)
    exec_time = round(end_time - start_time, 3)
    cpu_delta = abs(cpu_after - cpu_before)
    mem_used = round(mem_after - mem_before, 2)

    # EcoScore Calculation
    eco_score = max(0, 100 - (cpu_delta * 0.5 + exec_time * 2 + mem_used * 0.2))

    metrics = {
        "cpu_time": f"{exec_time}s",
        "memory_usage": f"{mem_used}MB",
        "cpu_percent": f"{cpu_delta}%",
        "temperature": f"{temp}°C", 
        "co2_emission": f"{round(0.2 * exec_time + 0.01 * mem_used, 2)}g"
    }

    os.remove(tmp_filename)

    return {
        "output": output,
        "ecoScore": round(eco_score, 2),
        "metrics": metrics
    }
