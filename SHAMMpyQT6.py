import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout
import configparser
import os
import filecmp
import json
# Open Settings Files
with open('SHAMM/SHAMM.json') as f:
        data = json.load(f)
# Open Hotkeys File
config = configparser.ConfigParser(allow_no_value=True)
config.read('StarfieldConsole.ini')

def backupIni():
    # Check if setting has changed
    with open('SHAMM/SHAMM.json') as f:
        data = json.load(f)
    # Access the value of the backup setting
    for setting in data['Settings']:
        if setting['name'] == 'backup':
            backup_setting = setting['value']           
    if backup_setting == 'true':
        # Backup Feature
        def backupcheck():
            backupfile = '.StarfieldConsole.ini'
            i = 1
            while os.path.exists(f"backup{i:03d}{backupfile}") and not filecmp.cmp('StarfieldConsole.ini', f"backup{i:03d}{backupfile}"):
                i += 1
            # Checks to see if new backup is needed.
            if not os.path.exists(f"backup{i:03d}{backupfile}"):
                with open(f"backup{i:03d}{backupfile}", 'w') as f:
                    config.write(f, space_around_delimiters=False)
        backupcheck()
    else:
        pass
backupIni()

class StarfieldHotkeys(QWidget):
    # Hotkey UI needs to be redone
    def __init__(SHAMM):
        super().__init__() 
        SHAMM.setWindowTitle("SHAMM - Starfield Hotkeys And Macro Manager")
        SHAMM.grid = QGridLayout()
        SHAMM.setLayout(SHAMM.grid)
        SHAMM.entries = []
        row = 0
        col = 0
        for key in config['Hotkeys']:
            label = QLabel(config['Hotkeys'][key])
            SHAMM.grid.addWidget(label, row, col)

            entry = QLineEdit()
            entry.insert(key)
            SHAMM.grid.addWidget(entry, row, col+1)

            SHAMM.entries.append(entry)
        
            col += 2
            if col > 7:
                row += 1
                col = 0
        # Save & Close Button
        close_button = QPushButton('Save And Exit')
        close_button.clicked.connect(SHAMM.save_changes)
        SHAMM.grid.addWidget(close_button, row+1, 0, 1, 1)
        
        # Setting Window Button
        settings_button = QPushButton('Settings', SHAMM)
        settings_button.clicked.connect(SHAMM.open_settings_window)
        SHAMM.grid.addWidget(settings_button, row+1, 6, 1, 8)            

        # Store a reference to the SettingsWindow object as an instance variable
        SHAMM.settings_window = None
                
    def open_settings_window(SHAMM):
        # Create a new instance of the SettingsWindow class and show it when the settings button is pressed
        if not SHAMM.settings_window:
            SHAMM.settings_window = SettingsWindow()
        SHAMM.settings_window.show()

    # Save changes to the hotkeys
    def save_changes(SHAMM):
        for i, key in enumerate(config['Hotkeys']):
            new_key = SHAMM.entries[i].text()
            if new_key != key:          # Important, checks to replace key=value 
                config['Hotkeys'][new_key] = config['Hotkeys'][key]
                del config['Hotkeys'][key]
        with open('StarfieldConsole.ini', 'w') as f:
            config.write(f, space_around_delimiters=False)
        backupIni()
        app.quit()
        
    def closeEvent(SHAMM, event):
        if SHAMM.settings_window:
            SHAMM.settings_window.close()
        
        event.accept()
        
class SettingsWindow(QMainWindow):
    def __init__(SHAMM):
        super().__init__()
        # Set the title and size of the window
        SHAMM.setWindowTitle("Settings")
        SHAMM.setGeometry(500, 400, 100, 100)
        # Add widgets to the window
        label = QLabel("SHAMM SETTINGS", SHAMM)
        label.move(45, 1)
        # Creates a button with a dynamic label 
        SHAMM.backup_button = QPushButton("Enable Backup", SHAMM)
        SHAMM.backup_button.move(45, 30)
        # Sets the initial state of the button based on the value in the JSON file
        backup_setting = data['Settings'][0]['value']
        if backup_setting == 'true': 
            SHAMM.backup_button.setText("Disable Backup")
        # When button is pressed trigger toggle_backup function
        SHAMM.backup_button.clicked.connect(SHAMM.toggle_backup)
        # Set the tooltip for the button
        SHAMM.backup_button.setToolTip('Click to enable/disable backup')    
        # Resize the window to fit its contents
        SHAMM.adjustSize()
    # Backup Setting Function
    def toggle_backup(SHAMM):
        with open('SHAMM/SHAMM.json', 'r') as f:
            data = json.load(f)
            # Checks backup current setting, then changes from true to false or vice versa
        for setting in data['Settings']:
            if setting['name'] == 'backup':
                setting['value'] = str(not (setting['value'] == 'true')).lower()
                if setting['value'] == 'true':
                    # Updates Button Text
                    SHAMM.backup_button.setText("Disable Backup")
                else:
                    SHAMM.backup_button.setText("Enable Backup")
        with open('SHAMM/SHAMM.json', 'w') as f:
                json.dump(data, f)  
                
app = QApplication(sys.argv)
icon = QIcon('SHAMM/.resource/SHAMM.ico')
app.setWindowIcon(icon)
hotkeys_window = StarfieldHotkeys()
hotkeys_window.show()
sys.exit(app.exec())