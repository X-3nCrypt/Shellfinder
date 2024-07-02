# Shell Finder

Shell Finder is a tool designed to detect webshell or backdoor files on a website. It uses a list of common paths and file name combinations to detect malicious files.

## Features

- **Dictionary-based Path Scanning**: Uses a list of common paths and filename combinations to detect malicious files.
- **Heuristic Analysis**: Performs heuristic analysis to detect signs of a webshell or backdoor.
- **Multi-threading**: Uses multi-threading to speed up the scanning process.
- **Error Handling**: Handles various types of network errors with informative messages.

## Installation

1. Clone this repository:
    ```
    https://github.com/X-3nCrypt/Shellfinder.git
    cd shellfinder
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script with the following command:
```bash
python3 shellfinder.py
