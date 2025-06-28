
let tabUsageData = {};  // { tabId: lastUpdated }

// Step 1: Initialize all open tabs once when the extension starts
chrome.tabs.query({}, function (tabs) {
    const now = Date.now();
    tabs.forEach(tab => {
        tabUsageData[tab.id] = now;

        // Send initial data to backend with usage time 0
        fetch("http://127.0.0.1:8000/track_tab", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                tab_id: tab.id,
                url: tab.url,
                title: tab.title,
                usage_time_ms: 0
            })
        });
    });
});

// Step 2: Every 15 seconds, update only the active tab in the focused window
setInterval(() => {
    const now = Date.now();

    chrome.tabs.query({ active: true, lastFocusedWindow: true }, function(tabs) {
        tabs.forEach(tab => {
            const lastUpdated = tabUsageData[tab.id] || now;
            const usageTime = now - lastUpdated;

            // Update only the active tab's last seen time
            tabUsageData[tab.id] = now;

            // Send data to backend
            fetch("http://127.0.0.1:8000/track_tab", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    tab_id: tab.id,
                    url: tab.url,
                    title: tab.title,
                    usage_time_ms: usageTime
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.close_tabs && data.close_tabs.length > 0) {
                    data.close_tabs.forEach(tabId => {
                        chrome.tabs.remove(tabId, () => {
                            console.log(`Closed tab from backend: ${tabId}`);
                        });
                    });
                }
            });
        });
    });
}, 15000);

// Cleanup closed tabs from local tracking
chrome.tabs.onRemoved.addListener((tabId, _) => {
    delete tabUsageData[tabId];
});
