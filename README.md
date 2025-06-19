# how - Your Personal Swiss Army Knife CLI Tool

A powerful command-line tool that provides various utilities for different operating systems. how is designed to be your go-to tool for system management, file operations, and development tasks across Windows, Linux, and macOS.

## Features

- **File Management**
  - Download and extract files with virus scanning
  - Advanced file search capabilities
  - Directory navigation with shell integration
  - Archive handling (zip, tar, etc.)

- **System Utilities**
  - Detailed system information display
  - Package management integration
  - Cross-platform support
  - System cleanup tools
  - Network utilities

- **Development Tools**
  - Git integration
  - Project scaffolding
  - Code testing utilities
  - Development environment management

- **Security Features**
  - Multiple execution modes (safe, dangerous, sudo)
  - ClamAV integration for file scanning
  - Path safety checks
  - Permission management

- **Cross-Platform Support**
  - Native Windows support via Wine
  - Android APK management
  - ChromeOS support
  - Multiple Linux distribution support

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/tolazytomakeausername/how.git
   cd how
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the main script:
   ```bash
   # Make how.py executable
   chmod +x how.py
   ```

4. Set up wrapper scripts (optional but recommended):
   ```bash
   # Create HOW and sHOW wrappers
   ln -s how.py HOW
   ln -s how.py sHOW
   ```

5. Add the scripts to your PATH:
   ```bash
   # Add to your PATH (example for Linux)
   export PATH=$PATH:/path/to/how
   ```

## Usage

### Basic Usage
```bash
how <command> [arguments]
```

### Modes
- `how`: Safe mode (default)
- `HOW`: Dangerous mode (for system operations)
- `sHOW`: Dangerous + Sudo mode (for admin tasks)

### Commands
- `get`: Download and extract files with virus scanning
- `go`: Directory navigation with shell integration
- `worship`: Sheet music downloader
- `sysinfo`: Detailed system information
- `wine`: Run Windows executables
- `git`: Git operations
- `android`: Android APK management
- `clean`: System cleanup and maintenance
- `dev`: Development tools and utilities
- `run`: Intelligent command execution
- `unzip`: Archive extraction
- `file`: File management
- `find`: Advanced file search
- `self-test`: Diagnostic tools

### Examples
```bash
# Download a file with custom name
how get https://example.com/file.zip -q my-custom-name

# Change directory with go command
how go /path/to/dir
# Change directory and actually cd (requires shell integration)
how go /path/to/dir -c

# Run in dangerous mode
HOW dangerous_command

# Run with sudo privileges
sHOW command
```

## Configuration

The tool uses a configuration file located at:
- Linux: `~/.config/how/config.json`
- Windows: `%APPDATA%/how/config.json`
- macOS: `~/Library/Application Support/how/config.json`

You can find an example configuration file in the `config` directory of this repository.

## Shell Integration

For the `go -c` command to work properly, you need to add a shell function to your shell configuration file:

```bash
# Add this to your ~/.bashrc or ~/.zshrc
how go --shell-function
```

## Credits

This project uses the following third-party components:

1. Core Dependencies
   - Requests (MIT License)
     - https://github.com/psf/requests
     - Copyright 2019 Kenneth Reitz
   - BeautifulSoup 4 (MIT License)
     - https://www.crummy.com/software/BeautifulSoup/bs4/doc/
     - Copyright 2004-2025 Leonard Richardson
   - Pillow (PIL Fork) (HPND License)
     - https://github.com/python-pillow/Pillow
     - Copyright 2010-2025 Alex Clark and Contributors

2. System and File Management
   - psutil (BSD License)
     - https://github.com/giampaolo/psutil
     - Copyright 2009-2025 Giampaolo Rodola'
   - pathlib (PSF License)
     - Part of Python Standard Library
     - Copyright Python Software Foundation

3. Package Management
   - packaging (Apache License 2.0)
     - https://github.com/pypa/packaging
     - Copyright 2014 Donald Stufft and individual contributors

4. Network Utilities
   - netifaces (LGPL License)
     - https://github.com/al45tair/netifaces
     - Copyright 2010 Alastair Houghton

5. Archive Handling
   - patool (GPL License)
     - https://github.com/wummel/patool
     - Copyright 2004-2025 Bastian Kleineidam

6. Security and Scanning
   - pyclamd (GPL License)
     - https://github.com/jim-daly/pyclamd
     - Copyright 2010-2025 Jim Daly

7. Development Tools
   - pytest (MIT License)
     - https://github.com/pytest-dev/pytest
     - Copyright 2004-2025 Holger Krekel and others
   - black (MIT License)
     - https://github.com/psf/black
     - Copyright 2018-2025 Łukasz Langa and others
   - isort (MIT License)
     - https://github.com/PyCQA/isort
     - Copyright 2013-2025 Tim Hatch
   - mypy (MIT License)
     - https://github.com/python/mypy
     - Copyright 2012-2025 Jukka Lehtosalo and others

8. Documentation
   - Sphinx (BSD License)
     - https://github.com/sphinx-doc/sphinx
     - Copyright 2007-2025 Georg Brandl and others
   - sphinx-rtd-theme (MIT License)
     - https://github.com/readthedocs/sphinx_rtd_theme
     - Copyright 2013-2025 Read the Docs, Inc.

9. Version Control
   - GitPython (BSD License)
     - https://github.com/gitpython-developers/GitPython
     - Copyright 2010-2025 Sebastian Thiel and others

10. Other Utilities
    - python-dateutil (PSF License)
      - https://github.com/dateutil/dateutil
      - Copyright 2003-2025 Paul Ganssle and others
    - colorama (BSD License)
      - https://github.com/tartley/colorama
      - Copyright 2013-2025 Jonathan Hartley
    - rich (MIT License)
      - https://github.com/willmcgugan/rich
      - Copyright 2020-2025 Will McGugan

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

[Add contribution guidelines here]
