import { runConvertedScript } from './script.js';

document.getElementById('runPython').addEventListener('click', async () => {
  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const currentTab = tabs[0];
    const domain = new URL(currentTab.url).hostname;

    // Call the converted function with the domain as an argument
    const result = await runConvertedScript(domain);

    // Display the result in an alert box
    alert(result);
  });
});