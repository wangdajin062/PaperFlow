const { app, BrowserWindow, Tray, Menu, ipcMain, nativeImage, shell, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

// --- Configuration ---
const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;
const BACKEND_PORT = 8765;
const FRONTEND_DEV_PORT = 5173;

const BACKEND_DIR = isDev
  ? path.resolve(__dirname, '..', 'backend')
  : path.resolve(process.resourcesPath, 'backend');

const FRONTEND_DIST_DIR = isDev
  ? path.resolve(__dirname, '..', 'frontend', 'dist')
  : path.resolve(process.resourcesPath, 'frontend', 'dist');

let mainWindow = null;
let tray = null;
let backendProcess = null;

// --- Backend Management ---

function startBackend() {
  if (isDev) {
    // Dev mode: use system python with uvicorn --reload
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
    const args = ['-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', String(BACKEND_PORT), '--reload'];
    backendProcess = spawn(pythonCmd, args, {
      cwd: BACKEND_DIR,
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env },
    });
  } else {
    // Production: use bundled portable Python
    const pythonExe = path.join(BACKEND_DIR, 'python', 'python.exe');
    const runScript = path.join(BACKEND_DIR, 'run_backend.py');
    backendProcess = spawn(pythonExe, [runScript], {
      cwd: BACKEND_DIR,
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env },
    });
  }

  backendProcess.stdout.on('data', (data) => {
    console.log(`[backend] ${data.toString().trim()}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.log(`[backend] ${data.toString().trim()}`);
  });

  backendProcess.on('error', (err) => {
    console.error('[backend] Failed to start:', err.message);
  });

  backendProcess.on('exit', (code) => {
    console.log(`[backend] Process exited with code ${code}`);
    backendProcess = null;
  });

  console.log(`[backend] Started (PID: ${backendProcess.pid})`);
}

function stopBackend() {
  if (backendProcess) {
    console.log('[backend] Stopping...');
    if (process.platform === 'win32') {
      spawn('taskkill', ['/pid', String(backendProcess.pid), '/f', '/t']);
    } else {
      backendProcess.kill('SIGTERM');
    }
    backendProcess = null;
  }
}

/**
 * Wait for the backend health endpoint to respond.
 * Resolves when healthy, rejects after timeout.
 */
function waitForBackend(timeoutMs = 15000) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    function check() {
      if (Date.now() - start > timeoutMs) {
        reject(new Error(`Backend did not start within ${timeoutMs}ms`));
        return;
      }
      const req = http.get(`http://127.0.0.1:${BACKEND_PORT}/api/health`, (res) => {
        if (res.statusCode === 200) resolve();
        else setTimeout(check, 300);
      });
      req.on('error', () => setTimeout(check, 300));
      req.setTimeout(1000, () => { req.destroy(); setTimeout(check, 300); });
    }
    check();
  });
}

// --- Window Management ---

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 600,
    icon: path.join(__dirname, 'icon.png'),
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  // Load the frontend
  if (isDev) {
    mainWindow.loadURL(`http://localhost:${FRONTEND_DEV_PORT}`);
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(FRONTEND_DIST_DIR, 'index.html'));
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Minimize to tray instead of closing
  mainWindow.on('close', (event) => {
    if (!app.isQuitting) {
      event.preventDefault();
      mainWindow.hide();
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// --- System Tray ---

function createTray() {
  // Create a simple 16x16 tray icon programmatically
  const icon = nativeImage.createEmpty();

  try {
    const iconPath = path.join(__dirname, 'tray-icon.png');
    tray = new Tray(iconPath);
  } catch {
    // Fallback: create a minimal icon
    const size = 16;
    const canvas = Buffer.alloc(size * size * 4, 0);
    // Fill with a simple color (blue-ish)
    for (let i = 0; i < size * size; i++) {
      const offset = i * 4;
      canvas[offset] = 66;     // R
      canvas[offset + 1] = 133; // G
      canvas[offset + 2] = 244; // B
      canvas[offset + 3] = 255; // A
    }
    const img = nativeImage.createFromBuffer(canvas, { width: size, height: size });
    tray = new Tray(img);
  }

  tray.setToolTip('PaperFlow');

  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Open PaperFlow',
      click: () => {
        if (mainWindow) {
          mainWindow.show();
          mainWindow.focus();
        } else {
          createWindow();
        }
      },
    },
    { type: 'separator' },
    {
      label: 'Quit',
      click: () => {
        app.isQuitting = true;
        app.quit();
      },
    },
  ]);

  tray.setContextMenu(contextMenu);

  tray.on('double-click', () => {
    if (mainWindow) {
      mainWindow.show();
      mainWindow.focus();
    } else {
      createWindow();
    }
  });
}

// --- IPC Handlers ---

ipcMain.handle('vscode:open', async (_event, args) => {
  try {
    const uri = `vscode://file/${encodeURIComponent(args.path)}?line=${args.line || 1}`;
    await shell.openExternal(uri);
    return { success: true };
  } catch (err) {
    console.error('[ipc] vscode:open failed:', err.message);
    return { success: false, error: err.message };
  }
});

// --- App Lifecycle ---

app.whenReady().then(() => {
  startBackend();
  createTray();

  // Wait for backend to be ready, then show window
  waitForBackend()
    .then(() => {
      createWindow();
    })
    .catch((err) => {
      console.error('[backend] Health check failed:', err.message);
      dialog.showErrorBox(
        'Backend Error',
        'Failed to start the backend server. The application may not function correctly.\n\n' +
        `Error: ${err.message}`
      );
      // Still create the window so user sees something
      createWindow();
    });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    } else if (mainWindow) {
      mainWindow.show();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  app.isQuitting = true;
  stopBackend();
});

app.on('will-quit', () => {
  stopBackend();
});
