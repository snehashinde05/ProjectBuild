let tabUsageData = {};  // { tabId: lastUpdated }

setInterval(() => {
    chrome.tabs.query({}, function(tabs) {
        const now = Date.now();

        tabs.forEach(tab => {
            const lastUpdated = tabUsageData[tab.id] || now;
            const usageTime = now - lastUpdated;

            // Update last seen time
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

// Cleanup closed tabs
chrome.tabs.onRemoved.addListener((tabId, _) => {
    delete tabUsageData[tabId];
});
