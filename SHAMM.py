class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
import configparser
config = configparser.ConfigParser(dict_type=AttrDict)
import tkinter as tk
import os
config._interpolation = configparser.ExtendedInterpolation()
# Read the INI file
config.read('StarfieldConsole.ini')

# Create a new Tkinter window
window = tk.Tk(className=' Starfield Hotkeys ')

# Create an entry widget for each command
row = 0
col = 0
entries = []
for key in config['Hotkeys']:
    label = tk.Label(window, text=config['Hotkeys'][key])
    label.grid(row=row, column=col)

    # Create an entry widget for each command's keybind
    entry = tk.Entry(window)
    entry.insert(0, key)
    entry.grid(row=row, column=col+1)

    
    entries.append(entry)
    
    col += 2
    if col > 7:
        row += 1
        col = 0


def refresh_gui():
    window.destroy()



# Save the changes to the INI file when the user clicks the "Save" button
def save_changes():
    for i, key in enumerate(config['Hotkeys']):
        new_key = entries[i].get()
        if new_key != key:
            config['Hotkeys'][new_key] = config['Hotkeys'][key]
            del config['Hotkeys'][key]



    with open('StarfieldConsole.ini', 'w') as f:
        config.write(f, space_around_delimiters=False)



        refresh_gui()

save_button = tk.Button(window, text='Save', command=save_changes)
save_button.grid(row=row+1, column=0, columnspan=8)

window.mainloop()


