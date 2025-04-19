from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import tempfile
import time
import os
import psutil
import wmi

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code1: str
    code2: str
    language: str

# Get CPU temperature using LibreHardwareMonitor
def get_cpu_temp():
    try:
        w = wmi.WMI(namespace="root\\LibreHardwareMonitor")
        sensors = w.Sensor()
        for sensor in sensors:
            if sensor.SensorType == 'Temperature' and 'CPU Package' in sensor.Name:
                return round(sensor.Value, 1)
    except Exception as e:
        print("Temperature fetch error:", e)
    return None

@app.post("/compare")
async def compare_codes(req: CodeRequest):
    if req.language != "python":
        return {"output": "Only Python is supported in this version.", "ecoScore": 0, "metrics": {}}

    def execute_and_measure(code: str):
        # Write code to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
            tmp_file.write(code.encode("utf-8"))
            tmp_filename = tmp_file.name

        #  Measure before execution
        start_time = time.time()
        process = psutil.Process(os.getpid())
        cpu_before = psutil.cpu_percent(interval=None)
        mem_before = process.memory_info().rss / (1024 ** 2)  # MB
        temp_before = get_cpu_temp()

        try:
            result = subprocess.run(["python", tmp_filename], capture_output=True, text=True)
            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)

        #  Measure after execution
        end_time = time.time()
        cpu_after = psutil.cpu_percent(interval=None)
        mem_after = process.memory_info().rss / (1024 ** 2)  # MB
        temp_after = get_cpu_temp()

        exec_time = round(end_time - start_time, 3)
        cpu_delta = abs(cpu_after - cpu_before)
        mem_used = round(mem_after - mem_before, 2)

        # Temperature difference
        temp_diff = None
        if temp_before is not None and temp_after is not None:
            temp_diff = round(temp_after - temp_before, 2)
            if temp_diff <0 :
                temp_diff = temp_diff * -1

        # EcoScore Calculation
        eco_score = max(0, 100 - (cpu_delta * 0.5 + exec_time * 2 + mem_used * 0.2))

        metrics = {
            "cpu_time": f"{exec_time}s",
            "memory_usage": f"{mem_used}MB",
            "cpu_percent": f"{cpu_delta}%",
            "temperature_increase": f"{temp_diff}°C" if temp_diff is not None else "N/A",
            "co2_emission": f"{round(0.002 * exec_time + 0.01 * mem_used, 2)}g"
        }

        os.remove(tmp_filename)

        return {
            "output": output,
            "ecoScore": round(eco_score, 2),
            "metrics": metrics
        }

    # Execute and measure for both codes
    result_code1 = execute_and_measure(req.code1)
    result_code2 = execute_and_measure(req.code2)

    comparison = {
        "code1": result_code1,
        "code2": result_code2,
        "comparison_metrics": {
            "ecoScore_diff": round(result_code1["ecoScore"] - result_code2["ecoScore"], 2),
            "cpu_percent_diff": round(float(result_code1["metrics"]["cpu_percent"].strip('%')) - float(result_code2["metrics"]["cpu_percent"].strip('%')), 2),
            "exec_time_diff": round(float(result_code1["metrics"]["cpu_time"].strip('s')) - float(result_code2["metrics"]["cpu_time"].strip('s')), 3),
            "memory_usage_diff": round(float(result_code1["metrics"]["memory_usage"].strip('MB')) - float(result_code2["metrics"]["memory_usage"].strip('MB')), 2),
        }
    }

    return comparison