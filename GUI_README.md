# Scrcpy GUI Wrapper

A modern graphical user interface for scrcpy, making it easier to use scrcpy with a beautiful and intuitive interface.

## Features

- Modern, clean interface using ttkthemes
- Device selection dropdown
- Resolution control
- Bitrate adjustment
- Common options like "Turn screen off" and "Stay awake"
- Status bar showing current state
- Easy-to-use buttons with icons

## Requirements

- Python 3.6 or higher
- scrcpy installed and available in system PATH
- ADB installed and available in system PATH

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure scrcpy is installed and available in your system PATH.

## Usage

Run the GUI wrapper:
```bash
python scrcpy_gui.py
```

### Building Executable

To create a standalone executable:

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Build the executable
pyinstaller --name scrcpy-gui --windowed --icon=app/data/icon.png scrcpy_gui.py
```

The executable will be created in the `dist/scrcpy-gui` directory.

## Features in Detail

- **Device Selection**: Automatically detects and lists connected Android devices
- **Resolution Control**: Set maximum resolution for the display
- **Bitrate Control**: Adjust streaming quality
- **Options**:
  - Turn screen off: Disables the device screen while mirroring
  - Stay awake: Prevents the device from sleeping
- **Status Bar**: Shows current state and any errors

## Contributing

Feel free to submit issues and enhancement requests! 