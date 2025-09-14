# Kemono Manual URL Tracker

A PyQt6-based desktop application for tracking and managing Kemono URLs.

## Features

- Two-pane interface for user and URL management
- Persistent window state and layout
- Comprehensive logging
- Modern PyQt6 interface with menu bar and status bar
- Error handling and user feedback

## Requirements

- Python 3.8+
- PyQt6

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python app.py
```

## Project Structure

```
kemono-watcher/
├── app.py              # Main application entry point
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── controller/         # Application controllers
├── model/             # Data models
├── view/              # UI components
│   ├── left_pane/     # Left pane components
│   └── right_pane/    # Right pane components
└── assets/            # Application assets (icons, etc.)
```

## Development

The application follows an MVC architecture pattern with separate directories for models, views, and controllers.