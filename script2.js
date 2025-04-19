document.getElementById('submit-code').addEventListener('click', async function () {
    const code = document.getElementById('code-area').value;
    const language = document.getElementById('language-select').value;

    if (!code.trim()) {
        alert('Please write some code to run!');
        return;
    }

    // Show loading message
    document.getElementById('output-text').textContent = "Running code...";
    document.getElementById('eco-score').textContent = "Eco Score: Calculating...";
    document.getElementById('co2-emission').textContent = "CO₂ Emission: Calculating...";
    document.getElementById('cpu-heat').textContent = "CPU Heat: Calculating...";
    document.getElementById('power-consumption').textContent = "Power Consumption: Calculating...";

    // Send code and language to the backend
    const response = await fetch('/run-code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code, language }),
    });

    const data = await response.json();

    if (data.error) {
        // Show error message
        document.getElementById('output-text').textContent = `Error: ${data.error}`;
    } else {
        // Show output and execution metrics
        document.getElementById('output-text').textContent = data.output;
        document.getElementById('eco-score').textContent = `Eco Score: ${data.ecoScore}`;
        document.getElementById('co2-emission').textContent = `CO₂ Emission: ${data.co2Emission}`;
        document.getElementById('cpu-heat').textContent = `CPU Heat: ${data.cpuHeat}`;
        document.getElementById('power-consumption').textContent = `Power Consumption: ${data.powerConsumption}`;
    }
});
