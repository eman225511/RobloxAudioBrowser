# 🚀 Setup Guide

## Quick Start (Recommended)

Simply double-click `run.bat` and the application will automatically:
1. Check for Python installation
2. Create a virtual environment
3. Install required packages
4. Launch the application

## Manual Installation Steps

If you prefer to set up manually or encounter issues with the automated setup:

### Prerequisites
- Python 3.7 or higher
- Windows operating system
- Internet connection (for package installation)

### Step-by-Step Setup

1. **Install Python** (if not already installed)
   - Download from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation
   - Verify installation: Open Command Prompt and run `python --version`

2. **Download the Project**
   - Download all files to a folder (e.g., `C:\RobloxAudioBrowser\`)
   - Ensure these files are present:
     - `roblox_audio_browser.py`
     - `run.bat`
     - `requirements.txt`
     - `README.md`

3. **Run the Application**
   - Double-click `run.bat`, or
   - Open Command Prompt in the project folder and run:
     ```
     python -m venv .venv
     .venv\Scripts\activate
     pip install -r requirements.txt
     python roblox_audio_browser.py
     ```

## 🎹 Quick Usage Tips

Once the application is running:
- **Press F1** for complete keyboard shortcuts reference
- **Use Space** to play/pause audio
- **Use Arrow keys** to navigate files
- **Press F5** to scan for new Roblox audio files
- **Use Ctrl+F** to focus the search box

## Troubleshooting

### "Python is not installed or not in PATH"
- Install Python from [python.org](https://python.org)
- During installation, check "Add Python to PATH"
- Restart your computer after installation

### "Failed to create virtual environment"
- Ensure you have the latest Python version
- Try running as administrator
- Update pip: `python -m pip install --upgrade pip`

### "Failed to install required packages"
- Check your internet connection
- Try running as administrator
- Update pip: `python -m pip install --upgrade pip`
- Manually install pygame: `pip install pygame`

### "Permission denied" when scanning
- Run the application as administrator
- Close Roblox if it's currently running
- Check antivirus settings (may block access to cache folders)

### Application won't start
- Ensure all files are in the same directory
- Check that Python 3.7+ is installed
- Try deleting the `.venv` folder and running `run.bat` again

## Advanced Configuration

### Custom Python Installation
If you have multiple Python versions, you can specify which one to use:
1. Edit `run.bat`
2. Replace `python` with the full path to your preferred Python executable
3. Example: `C:\Python39\python.exe -m venv .venv`

### Development Setup
For developers who want to modify the code:
```bash
git clone <repository-url>
cd roblox-audio-browser
python -m venv dev-env
dev-env\Scripts\activate
pip install -r requirements.txt
pip install pytest  # for testing (if tests are added)
```

## System Requirements

### Minimum Requirements
- Windows 7/8/10/11
- Python 3.7+
- 50 MB free disk space
- 512 MB RAM

### Recommended Requirements
- Windows 10/11
- Python 3.8+
- 200 MB free disk space
- 1 GB RAM
- SSD for faster scanning

## Support

If you still encounter issues after following this guide:
1. Check the main [README.md](README.md) for additional information
2. Review the error messages carefully
3. Search for existing issues on GitHub
4. Create a new issue with:
   - Your Python version (`python --version`)
   - Your Windows version
   - The exact error message
   - Steps you tried to fix the issue

---

Happy audio browsing! 🎵
