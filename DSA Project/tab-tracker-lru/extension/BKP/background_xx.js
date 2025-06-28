let tabUsageData = {};  // { tabId: lastInteractionTime }

// Track tab activation
chrome.tabs.onActivated.addListener(activeInfo => {
    tabUsageData[activeInfo.tabId] = Date.now();
});

// Track window focus (when switching between Chrome windows)
chrome.windows.onFocusChanged.addListener(windowId => {
    if (windowId === chrome.windows.WINDOW_ID_NONE) return;
    chrome.tabs.query({ active: true, windowId }, tabs => {
        if (tabs.length > 0) {
            tabUsageData[tabs[0].id] = Date.now();
        }
    });
});

// Send usage info every 15s
setInterval(() => {
    chrome.tabs.query({}, function(tabs) {
        const now = Date.now();

        tabs.forEach(tab => {
            const lastUsed = tabUsageData[tab.id] || now;
            const idleTime = now - lastUsed;

            fetch("http://127.0.0.1:8000/track_tab", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    tab_id: tab.id,
                    url: tab.url,
                    title: tab.title,
                    usage_time_ms: idleTime
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

// Remove closed tabs from memory
chrome.tabs.onRemoved.addListener((tabId) => {
    delete tabUsageData[tabId];
});
