// Modules to control application life and create native browser window
const { app, BrowserWindow } = require('electron')

// Keep a global reference of the windows object, if you don't, the windows will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow
let loadingScreen

function createLoadingScreen() {
  // Create the loading screen window.
  loadingScreen = new BrowserWindow({
    width: 400,
    height: 300,
    frame: false, // Remove window frame
    transparent: true, // Make window transparent
    resizable: false, // make window non-resizable
    webPreferences: {
      nodeIntegration: true
    }
  });

  // and load the loading.html file.
  loadingScreen.loadFile('./web/components/loading/loading.html');

  // Show the loading screen window.
  loadingScreen.show();

  // Emitted when the window is closed.
  loadingScreen.on('closed', function () {
    // Dereference the window object and force garbage collection.
    loadingScreen = null
  })
}

function createWindow() {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 720,
    titleBarStyle: "hidden",
    titleBarOverlay: {
      color: "#2f3241",
      symbolColor: "#74b1be",
      height: 30,
    },
    webPreferences: {
      nodeIntegration: true,
    },
    show: false // Don't show the window initially
  });

  // and load the index.html of the app.
  mainWindow.loadURL('http://localhost:8000/index.html');

  // Emitted when the window is ready to show
  mainWindow.once('ready-to-show', () => {
    setTimeout(() => {
      loadingScreen.hide();
      mainWindow.show();
    }, 2000); // Wait 2 seconds before showing the main window
  });

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null;

    // Clean up all running processes of the app.
    app.quit();
  });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', () => {
  createLoadingScreen();
  createWindow();
});

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') app.quit()
})

app.on('activate', function () {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) createWindow()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here

app.on('will-quit', () => {
  // Quit the app.
  app.quit();
});