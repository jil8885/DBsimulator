// load module from node_modules
const {app, BrowserWindow} = require('electron');

let win;

function createWindow () {
    win = new BrowserWindow({width: 1200, height: 900, frame: false});

    win.loadFile('templates/power_on.html');

    win.on('closed', () => {
        win = null;
    })
}


app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (win === null) {
        createWindow();
    }
});