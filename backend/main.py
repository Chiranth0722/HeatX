from fastapi import FastAPI
import psutil

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "HeatX API is running."}

@app.get("/metrics")
def get_metrics():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    # Safe temperature fallback
    try:
        temps = psutil.sensors_temperatures()
        temp = 0
        if temps:
            for name, entries in temps.items():
                if entries:
                    temp = entries[0].current
                    break
        else:
            temp = -1  # or "Not Available"
    except Exception as e:
        temp = -1  # fallback if unsupported

    return {
        "cpu": cpu,
        "ram": ram,
        "temperature": temp
    }
