import psutil
import time

# Set your CPU's TDP in watts (lookup online or estimate)
TDP = 45  # Example for many Intel CPUs

def estimate_power_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    estimated_power = (cpu_percent * TDP) / 100
    return estimated_power

# Simulate a time window
initial_power = estimate_power_usage()
print(f"Initial Estimated Power: {initial_power:.2f} W")
a=0
def fn(a):
    for i in range(10):
        a=a+i
    time.sleep(5)
fn(a)

final_power = estimate_power_usage()
print(f"Final Estimated Power: {final_power:.2f} W")
p=final_power-initial_power
if p<0:
    p=p*-1
print('Power consumed:',p)
# Calculate average and CO2
average_power = (initial_power + final_power) / 2
runtime_seconds = 5
energy_used_wh = (average_power * runtime_seconds) / 3600
co2_emission = energy_used_wh * 0.475  # kg CO2 per Wh

print(f"Estimated CO2 Emission: {co2_emission:.6f} kg")
