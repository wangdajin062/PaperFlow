const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  openInVSCode: (args) => ipcRenderer.invoke('vscode:open', args),
  platform: process.platform,
});
