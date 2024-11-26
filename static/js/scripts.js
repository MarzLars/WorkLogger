document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('start-button');
    const pauseButton = document.getElementById('pause-button');
    const stopButton = document.getElementById('stop-button');
    const elapsedTimeDisplay = document.getElementById('elapsed-time');
    const logsContainer = document.getElementById('logs');
    const delimiterSelect = document.getElementById('delimiter');
    const exportButton = document.getElementById('export-button');

    let timerInterval;

    startButton.addEventListener('click', function() {
        fetch('/start', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'started') {
                    startTimer();
                }
            });
    });

    pauseButton.addEventListener('click', function() {
        fetch('/pause', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'paused') {
                    stopTimer();
                }
            });
    });

    stopButton.addEventListener('click', function() {
        const description = prompt('Enter a description for the worklog:');
        fetch('/stop', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description: description })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'stopped') {
                    stopTimer();
                    fetchLogs();
                }
            });
    });

    delimiterSelect.addEventListener('change', function() {
        const selectedDelimiter = delimiterSelect.value;
        fetch('/set_delimiter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ delimiter: selectedDelimiter })
        });
    });

    exportButton.addEventListener('click', function() {
        fetch('/export', { method: 'GET' })
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'time_log.csv';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            });
    });

    function startTimer() {
        if (!timerInterval) {
            timerInterval = setInterval(updateElapsedTime, 1000);
        }
    }

    function stopTimer() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
    }

    function updateElapsedTime() {
        fetch('/elapsed_time')
            .then(response => response.json())
            .then(data => {
                const elapsedTime = data.elapsed_time;
                const hours = Math.floor(elapsedTime / 3600);
                const minutes = Math.floor((elapsedTime % 3600) / 60);
                const seconds = Math.floor(elapsedTime % 60);
                elapsedTimeDisplay.textContent = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
            });
    }

    function pad(number) {
        return number.toString().padStart(2, '0');
    }

    function fetchLogs() {
        fetch('/logs')
            .then(response => response.json())
            .then(data => {
                const logs = data.logs;
                logsContainer.innerHTML = '';
                logs.forEach(log => {
                    const logElement = document.createElement('div');
                    logElement.textContent = `Description: ${log[0]}, Date: ${log[1]}, Week: ${log[2]}, Time Spent: ${log[3]}, Hours: ${log[4]}, Minutes: ${log[5]}, Seconds: ${log[6]}`;
                    logsContainer.appendChild(logElement);
                });
            });
    }

    fetchLogs();
});
