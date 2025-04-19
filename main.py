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
    code: str
    language: str

# CPU Thermal Design Power (TDP) in Watts — update based on your CPU
TDP = 45

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

@app.post("/execute")
async def execute_code(req: CodeRequest):
    if req.language != "python":
        return {"output": "Only Python is supported in this version.", "ecoScore": 0, "metrics": {}}

    # Write code to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
        tmp_file.write(req.code.encode("utf-8"))
        tmp_filename = tmp_file.name

    def estimate_power_usage():
        cpu_pecent= psutil.cpu_percent(interval=1)
        estimated_power = (cpu_pecent*TDP)/100
        return estimated_power

    #  Measure before
    start_time = time.time()
    process = psutil.Process(os.getpid())
    cpu_before = psutil.cpu_percent(interval=None)
    mem_before = process.memory_info().rss / (1024 ** 2)  # MB
    temp_before = get_cpu_temp()
    initial_power=estimate_power_usage()
    

    try:
        result = subprocess.run(["python", tmp_filename], capture_output=True, text=True)
        output = result.stdout + result.stderr
    except Exception as e:
        output = str(e)

    #  Measure after
    end_time = time.time()
    cpu_after = psutil.cpu_percent(interval=None)
    mem_after = process.memory_info().rss / (1024 ** 2)  # MB
    temp_after = get_cpu_temp()

    exec_time = round(end_time - start_time, 3)
    cpu_delta = abs(cpu_after - cpu_before)
    mem_used = round(mem_after - mem_before, 2)
    if mem_used<0:
        mem_used*=-1
    final_power= estimate_power_usage()

    # Temperature difference
    temp_diff = None
    if temp_before is not None and temp_after is not None:
        temp_diff = round(temp_after - temp_before, 2)
        if temp_diff < 0:
            temp_diff *= -1

    # Estimated Power & CO2 Emission
    avg_power=(initial_power + final_power)/2 
    power_consumed= final_power - initial_power
    if power_consumed<0:
        power_consumed*=-1
    energy_used_wh = (avg_power * exec_time) / 3600  # Wh
    co2_emission = round(energy_used_wh * 0.475, 6)  # g CO2

    # Updated EcoScore Calculation
    eco_score = max(0, 100 - (cpu_delta * 0.3 + temp_diff * 0.3 + exec_time * 0.2 + power_consumed * 0.2))

    metrics = {
        "cpu_time": f"{exec_time}s",
        "memory_usage": f"{mem_used}MB",
        "cpu_percent": f"{cpu_delta}%",
        "temperature_increase": f"{temp_diff}°C" if temp_diff is not None else "N/A",
        "estimated_power": f"{power_consumed:.2f}W",
        "energy_used": f"{energy_used_wh:.6f}Wh",
        "co2_emission": f"{co2_emission} g"
    }

    os.remove(tmp_filename)

    return {
        "output": output,
        "ecoScore": round(eco_score, 2),
        "metrics": metrics
    }
