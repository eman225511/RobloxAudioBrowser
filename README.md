# 🎮 **Roblox Cache Audio Player**
- **Built-in audio player** with volume control
- **Multiple format support** - OGG Vorbis, MP3, WAV, FLAC
- **Play/Pause/Stop controls** with GUI buttons
- **Real-time volume adjustment** during playbackser

A powerful desktop application for browsing, playing, and extracting audio files from Roblox's cache directories. Built with Python and Tkinter, this tool helps you discover and manage cached audio files with an intuitive interface.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

## ✨ Features

### 🔍 **Smart Scanning**
- **Multi-threaded scanning** for fast performance
- **Automatic Roblox cache detection** - finds default cache locations
- **Custom folder scanning** - browse any directory for audio files
- **Real-time progress tracking** with cancellation support
- **Intelligent file filtering** - skips non-audio files automatically

### 🎮 **Audio Playback**
- **Built-in audio player** with volume control
- **Multiple format support** - OGG Vorbis, MP3, WAV, FLAC
- **Play/Pause/Stop controls** with keyboard shortcuts
- **Real-time volume adjustment** during playback

### 📊 **Enhanced Information Panel**
- **Detailed file information** - format, size, duration estimates, modification date
- **Collection statistics** - total files, formats breakdown, combined size
- **Smart format detection** - automatically identifies audio formats
- **Real-time playback status** with volume display

### 💾 **Export Capabilities**
- **Extract as OGG** - save clean OGG files from Roblox cache
- **Export hash files** - preserve original cached files
- **Batch operations** - process multiple files
- **File path copying** - quick clipboard access

### 🎨 **Modern UI**
- **Dark theme** - easy on the eyes
- **Professional layout** - clean and intuitive design
- **Context menus** - right-click for quick actions
- **Search/Filter** - find files quickly
- **Responsive design** - scales well on different screen sizes

## 🚀 Quick Start

### Option 1: Pre-built Executable (Easiest!)
**For users who just want to run the application without any setup:**

1. **Go to the [Releases](../../releases) tab**
2. **Download** the latest `RobloxAudioBrowser.exe`
3. **Double-click** the executable to run - no installation required!

*The pre-built executable includes all dependencies and requires no Python installation.*

### Option 2: Automatic Setup (Recommended for Developers)
1. **Download** the repository
2. **Run** `run.bat` - this will automatically:
   - Create a Python virtual environment
   - Install all required dependencies
   - Launch the application

### Option 3: Manual Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/roblox-audio-browser.git
cd roblox-audio-browser

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python roblox_audio_browser.py
```

## 📋 Requirements

- **Python 3.7+** (Python 3.8+ recommended)
- **Windows OS** (primarily tested on Windows 10/11)
- **Required Python packages** (automatically installed):
  - `pygame` - Audio playback
  - `tkinter` - GUI (usually included with Python)

## 🎯 Usage

### Getting Started
1. **Launch** the application using `run.bat` or `python roblox_audio_browser.py`
2. **Scan** Roblox cache by clicking "🔍 Scan Roblox Cache"
3. **Browse** found audio files in the list
4. **Select** a file to view detailed information
5. **Double-click** or use "▶️ Play" to listen

### Key Features
- **Double-click** any file to play it immediately
- **Right-click** for context menu with export options
- **Use the filter** box to search through your audio collection
- **Adjust volume** with the slider during playback
- **View collection statistics** when no file is selected

### Default Roblox Cache Locations
The application automatically scans these directories:
- `%LOCALAPPDATA%\Roblox\http`
- `%TEMP%\Roblox\http`

## 🛠️ Technical Details

### Architecture
- **Multi-threaded scanning** - Uses ThreadPoolExecutor for efficient file processing
- **Async UI updates** - Non-blocking interface during operations
- **Memory efficient** - Processes files in chunks to avoid memory issues
- **Error resilient** - Graceful handling of corrupted or inaccessible files

### File Detection
- **Header analysis** - Examines file headers to identify audio formats
- **Size filtering** - Skips obviously non-audio files (too small/large)
- **Format support** - OGG Vorbis, MP3, WAV, FLAC, and more

### Performance
- **Concurrent processing** - Uses multiple CPU cores for scanning
- **Progress tracking** - Real-time updates every 10 files processed
- **Cancellable operations** - Stop long-running scans anytime
- **Smart caching** - Avoids re-scanning unchanged directories

## 🔧 Troubleshooting

### Common Issues

**"No audio files found"**
- Ensure Roblox has been run recently to populate cache
- Try scanning custom folders where you know audio files exist
- Check if antivirus is blocking access to Roblox directories

**"Could not play audio file"**
- File might be corrupted or not actually audio
- Try extracting as OGG and playing in external player
- Ensure pygame is properly installed

**"Permission denied" errors**
- Run as administrator if scanning system directories
- Check if Roblox is currently running (may lock cache files)

### Audio Format Support
- **Primary**: OGG Vorbis (most Roblox audio)
- **Secondary**: MP3, WAV, FLAC
- **Experimental**: M4A, AAC (detection only)

## 📁 Project Structure
```
roblox-audio-browser/
├── roblox_audio_browser.py    # Main application
├── run.bat                    # Automatic setup and launcher
├── requirements.txt           # Python dependencies
├── README.md                 # This file
└── .venv/                    # Virtual environment (created by run.bat)
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/roblox-audio-browser.git

# Create development environment
python -m venv dev-env
dev-env\Scripts\activate
pip install -r requirements.txt

# Run tests (if available)
python -m pytest

# Run the application
python roblox_audio_browser.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is designed to help users manage their own cached audio files from Roblox. It does not facilitate piracy or copyright infringement. Users are responsible for ensuring they have the right to access and use any audio files they extract or play.

## 🙏 Acknowledgments

- **Pygame Community** - For the excellent audio playback library
- **Roblox** - For creating the platform that generates these audio caches
- **Python Community** - For the amazing ecosystem of libraries

## 🔄 Version History

- **v1.3** (Current) - Removed keyboard shortcuts, simplified to mouse-only interface
- **v1.2** - Enhanced info panel with detailed file information and statistics
- **v1.1** - Multi-threaded scanning and improved performance
- **v1.0** - Initial release with basic scanning and playback

## 🆘 Support

If you encounter issues or have questions:

1. **Check** the troubleshooting section above
2. **Search** existing issues on GitHub
3. **Create** a new issue with detailed information:
   - Python version
   - Operating system
   - Error messages
   - Steps to reproduce

---

**Made with ❤️ for the Roblox community**
