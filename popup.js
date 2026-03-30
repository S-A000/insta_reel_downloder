document.getElementById('dlBtn').addEventListener('click', async () => {
    const status = document.getElementById('status');
    const fileNameInput = document.getElementById('fileName').value; // Naam uthayein
    
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const videoUrl = tab.url;

    status.innerText = "Processing...";

    try {
        const response = await fetch('http://localhost:5000/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                url: videoUrl, 
                fileName: fileNameInput // Python ko naam bhejein
            })
        });

        const result = await response.json();
        status.innerText = result.message;
    } catch (error) {
        status.innerText = "Server band hai!";
    }
});