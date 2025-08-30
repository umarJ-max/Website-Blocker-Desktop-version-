# 🛡️ Website Blocker - Advanced Website Blocking Tool

## Full System Acess Need for Desktop Version or Use another Web version "aviable"
A powerful and user-friendly Python application for blocking distracting websites to boost productivity and maintain focus. Features a modern GUI interface, scheduling capabilities, and cross-platform support.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage](#-usage)
- [Requirements](#-requirements)
- [Platform-Specific Setup](#-platform-specific-setup)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Author](#-author)

## 🚀 Features

### Core Functionality
- **Real-time Website Blocking**: Instantly block and unblock websites
- **Advanced URL Validation**: Smart URL parsing and validation
- **DNS Flush Integration**: Automatic DNS cache clearing for immediate effect
- **Cross-Platform Support**: Works on Windows, macOS, and Linux

### User Interface
- **Modern GUI Design**: Clean, intuitive tkinter-based interface
- **Tabbed Interface**: Organized sections for different features
- **Real-time Status Updates**: Visual indicators for blocking status
- **Professional Branding**: "Umar J" branded interface

### Scheduling System
- **Time-based Blocking**: Schedule blocking sessions for specific hours
- **Day Selection**: Choose specific days for scheduled blocks
- **Automatic Management**: Auto-start/stop blocking based on schedule
- **Background Monitoring**: Continuous schedule checking

### Data Management
- **Configuration Persistence**: Save/load settings automatically
- **Import/Export**: Share configurations between devices
- **Backup/Restore**: Protect your hosts file with backup functionality
- **JSON Configuration**: Human-readable configuration files

### Security & Safety
- **Admin Privilege Handling**: Smart privilege escalation requests
- **Hosts File Protection**: Safe modification with backup options
- **Error Handling**: Comprehensive error management
- **Cross-platform Paths**: Automatic hosts file path detection

## 🖼️ Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────────┐
│  🛡️ Website Blocker                            ● Active  │
│  Advanced Website Blocking Tool - Created by Umar J     │
├─────────────────────────────────────────────────────────┤
│  [Website Blocking] [Scheduling] [Settings] [About]    │
│                                                         │
│  Add Website to Block:                                  │
│  ┌─────────────────────────────────────┐ [Add Website] │
│  │ facebook.com                        │               │
│  └─────────────────────────────────────┘               │
│                                                         │
│  [🚫 Start Blocking]  [🗑️ Clear All]                   │
│                                                         │
│  Blocked Websites:                                      │
│  ┌─────────────────────────────────────────────────────┐│
│  │ • facebook.com                                      ││
│  │ • youtube.com                                       ││
│  │ • twitter.com                                       ││
│  │ • instagram.com                                     ││
│  └─────────────────────────────────────────────────────┘│
│                          [Remove Selected]             │
└─────────────────────────────────────────────────────────┘
```

## 🛠 Installation

### Option 1: Direct Download
1. Download the `website_blocker.py` file
2. Ensure Python 3.7+ is installed
3. Run the application

### Option 2: Clone Repository
```bash
git clone https://github.com/yourusername/website-blocker.git
cd website-blocker
python website_blocker.py
```

### Option 3: Create Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name "Website Blocker" website_blocker.py

# Find executable in dist/ folder
```

## 💻 Usage

### Basic Website Blocking

1. **Launch the Application**:
   ```bash
   python website_blocker.py
   ```

2. **Add Websites**:
   - Enter website URL (e.g., `facebook.com`, `youtube.com`)
   - Click "Add Website" or press Enter
   - Website appears in the blocked list

3. **Start Blocking**:
   - Click "🚫 Start Blocking"
   - Grant admin privileges when prompted
   - Status indicator turns green

4. **Stop Blocking**:
   - Click "✅ Stop Blocking"
   - All blocked sites become accessible again

### Scheduled Blocking

1. **Go to Scheduling Tab**:
   - Click on "Scheduling" tab

2. **Set Time Range**:
   - Start Time: `09:00` (9 AM)
   - End Time: `17:00` (5 PM)

3. **Select Days**:
   - Choose specific weekdays
   - Multiple days supported

4. **Add Schedule**:
   - Click "Add Schedule"
   - Schedule appears in the list

### Configuration Management

1. **Backup Hosts File**:
   - Settings tab → "💾 Backup Hosts File"
   - Creates `hosts_backup.txt`

2. **Export Configuration**:
   - Settings tab → "📤 Export Config"
   - Creates timestamped JSON file

3. **Import Configuration**:
   - Settings tab → "📥 Import Config"
   - Select previously exported JSON file

## 📋 Requirements

### System Requirements
- **Python**: 3.7 or higher
- **Operating System**: Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+)
- **Memory**: 50MB RAM minimum
- **Storage**: 10MB free space

### Python Dependencies
```python
# Built-in modules (no additional installation needed)
tkinter          # GUI framework
json             # Configuration management
os               # Operating system interface
sys              # System-specific parameters
platform         # Platform identification
threading        # Background processing
time             # Time-related functions
datetime         # Date and time handling
webbrowser       # Web browser interface
pathlib          # Path handling
re               # Regular expressions
subprocess       # Process management
```

### Administrative Privileges
- **Windows**: Run as Administrator
- **macOS/Linux**: Run with `sudo`

## 🖥️ Platform-Specific Setup

### Windows Setup

1. **Install Python**:
   - Download from [python.org](https://python.org)
   - Ensure "Add to PATH" is checked

2. **Run as Administrator**:
   ```cmd
   # Right-click Command Prompt → "Run as Administrator"
   python website_blocker.py
   ```

3. **Hosts File Location**:
   ```
   C:\Windows\System32\drivers\etc\hosts
   ```

### macOS Setup

1. **Install Python** (if not already installed):
   ```bash
   # Using Homebrew
   brew install python

   # Or download from python.org
   ```

2. **Run with sudo**:
   ```bash
   sudo python3 website_blocker.py
   ```

3. **Hosts File Location**:
   ```
   /etc/hosts
   ```

### Linux Setup

1. **Install Python and tkinter**:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-tk

   # CentOS/RHEL/Fedora
   sudo yum install python3 python3-tkinter
   # or
   sudo dnf install python3 python3-tkinter

   # Arch Linux
   sudo pacman -S python python-tk
   ```

2. **Run with sudo**:
   ```bash
   sudo python3 website_blocker.py
   ```

3. **Hosts File Location**:
   ```
   /etc/hosts
   ```

## ⚙️ Configuration

### Configuration File Structure
The application creates a `blocker_config.json` file:

```json
{
    "blocked_sites": [
        "facebook.com",
        "youtube.com",
        "twitter.com"
    ],
    "scheduled_blocks": [
        {
            "start_time": "09:00",
            "end_time": "17:00",
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        }
    ],
    "version": "2.0",
    "created_by": "Umar J"
}
```

### Environment Variables
Set these for advanced configuration:

```bash
# Custom hosts file path (advanced users only)
export CUSTOM_HOSTS_PATH="/path/to/custom/hosts"

# Disable DNS flush (if causing issues)
export DISABLE_DNS_FLUSH=1
```

### URL Format Examples
```python
# Supported formats (auto-cleaned):
"facebook.com"           → "facebook.com"
"www.facebook.com"       → "facebook.com"  
"https://facebook.com"   → "facebook.com"
"http://www.facebook.com"→ "facebook.com"

# Invalid formats:
"facebook"               → Error
"facebook..com"          → Error
"192.168.1.1"           → Error (IP addresses not supported)
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Permission Denied Error
```
Error: Permission denied. Please run as administrator/root.
```
**Solution**:
- **Windows**: Right-click → "Run as Administrator"
- **macOS/Linux**: Use `sudo python3 website_blocker.py`

#### 2. Hosts File Not Found
```
Error: Could not locate hosts file
```
**Solution**:
- Verify OS compatibility
- Check if hosts file exists at standard location
- Run with administrative privileges

#### 3. GUI Not Displaying
```
ModuleNotFoundError: No module named '_tkinter'
```
**Solution**:
```bash
# Linux
sudo apt install python3-tk

# macOS with Homebrew
brew install python-tk

# Windows
# Reinstall Python with tkinter support
```

#### 4. Websites Still Accessible
```
Blocking activated but sites still load
```
**Solution**:
1. Clear browser cache
2. Restart browser
3. Try incognito/private mode
4. Check if VPN/proxy is bypassing blocks

#### 5. Schedule Not Working
```
Scheduled blocking not activating
```
**Solution**:
1. Verify system time is correct
2. Check schedule format (24-hour time)
3. Ensure application stays running
4. Check selected days are current

### Debug Mode

Enable debug logging:

```python
# Add at top of website_blocker.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Reset Configuration

```bash
# Remove configuration files to reset
rm blocker_config.json
rm hosts_backup.txt
```

### Manual Hosts File Editing

If application fails, manually edit hosts file:

**Location**:
- Windows: `C:\Windows\System32\drivers\etc\hosts`
- macOS/Linux: `/etc/hosts`

**Remove blocking entries**:
```
# Remove these lines
127.0.0.1 facebook.com
127.0.0.1 www.facebook.com
```

## 🔒 Security Considerations

### Data Privacy
- **No Network Communication**: All processing happens locally
- **No Data Collection**: No analytics or tracking
- **Config Files Local**: All settings stored on your device

### Hosts File Safety
- **Automatic Backup**: Creates backup before modifications
- **Safe Modifications**: Only adds/removes specific entries
- **Restore Function**: Easy restoration from backup

### Administrative Access
- **Minimal Privileges**: Only requests admin access when needed
- **Transparent Operations**: All file modifications are logged
- **No System Changes**: Only modifies hosts file

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Bug Reports
1. Check existing issues
2. Provide detailed description
3. Include system information
4. Add steps to reproduce

### Feature Requests
1. Describe the feature
2. Explain use case
3. Suggest implementation approach

### Code Contributions
1. Fork the repository
2. Create feature branch
3. Follow coding standards
4. Add tests if applicable
5. Submit pull request

### Coding Standards
```python
# Use descriptive variable names
blocked_websites = []  # Good
sites = []            # Avoid

# Add docstrings to functions
def validate_website(self, website):
    """Validate website URL format and return cleaned version."""
    pass

# Use type hints where possible
def add_website(self, website: str) -> bool:
    pass
```

## 📄 License

This project is licensed under the MIT License:

```
MIT License

Copyright (c) 2024 Umar J

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Author

**Umar J**
- **Role**: Python Developer & Software Engineer
- **Specialization**: Desktop Applications, Automation Tools
- **Portfolio**: [Your Portfolio URL]
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **LinkedIn**: [Your LinkedIn Profile](https://linkedin.com/in/yourprofile)
- **Email**: your.email@example.com

### Other Projects by Umar J
- 🔐 **SecureGen Password Generator** - Advanced password generation tool
- 🛠️ **System Utilities Suite** - Collection of system administration tools
- 📊 **Data Analysis Tools** - Python-based data processing applications

## 🙏 Acknowledgments

- **Python Community**: For excellent documentation and support
- **Tkinter Developers**: For the robust GUI framework
- **Open Source Contributors**: For inspiration and code examples
- **Beta Testers**: For valuable feedback and bug reports

## 📈 Roadmap

### Version 2.1 (Upcoming)
- [ ] Website category blocking (social media, news, etc.)
- [ ] Browser extension integration
- [ ] Network-level blocking option
- [ ] Parental control features

### Version 2.2 (Future)
- [ ] Cloud sync for configurations
- [ ] Mobile app companion
- [ ] Advanced analytics and reporting
- [ ] Team/organization management

### Version 3.0 (Long-term)
- [ ] AI-powered distraction detection
- [ ] Productivity score tracking
- [ ] Integration with productivity apps
- [ ] Web-based control panel

## 📊 Statistics

- **Lines of Code**: ~800
- **Functions**: 25+
- **Features**: 15+
- **Platforms Supported**: 3
- **Languages**: 1 (Python)
- **External Dependencies**: 0

## 🆘 Support

Need help? Here are your options:

1. **Documentation**: Read this README thoroughly
2. **Issues**: Check [GitHub Issues](https://github.com/yourusername/website-blocker/issues)
3. **Discussions**: Join [GitHub Discussions](https://github.com/yourusername/website-blocker/discussions)
4. **Email**: Contact directly at your.email@example.com

### Response Times
- **Bug Reports**: 24-48 hours
- **Feature Requests**: 3-5 days  
- **General Questions**: 1-2 days
- **Critical Issues**: Same day

---

**Made with ❤️ by Umar J | © 2024 | Python Desktop Application**

*Boost your productivity by eliminating digital distractions!*
