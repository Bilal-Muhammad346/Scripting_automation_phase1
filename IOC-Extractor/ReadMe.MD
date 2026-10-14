# Python IOC Extractor

## 1. Tool Name
Python IOC Extractor

## 2. Objective
The objective of this project is to develop a Python-based cybersecurity tool that extracts Indicators of Compromise (IOCs) from text files. It helps identify potentially useful security indicators for further investigation.

## 3. Features
- Extracts IPv4 addresses.
- Extracts HTTP and HTTPS URLs.
- Extracts domain names.
- Identifies MD5 hashes.
- Identifies SHA-1 hashes.
- Identifies SHA-256 hashes.
- Removes duplicate indicators within each category.
- Validates IPv4 addresses.
- Displays results in a categorized report.
- Saves results in JSON format.
- Handles basic errors.
- Provides a command-line help option.
- Uses Python's built-in libraries.

## 4. Requirements
- Python 3.9 or later recommended.
- Windows, Linux, or macOS.
- A text file containing data to analyze.
- No additional Python packages required.

## 5. How to Run

### Step 1: Clone the Repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

### Step 2: Open the Project Directory

```bash
cd Python-Tool
```

### Step 3: Check Python Installation

```bash
python --version
```

On Linux, you may need:

```bash
python3 --version
```

### Step 4: Run the Tool

```bash
python ioc-extractor.py sample.txt
```

On Linux:

```bash
python3 ioc-extractor.py sample.txt
```

### Step 5: Display Help

```bash
python ioc-extractor.py --help
```

### Step 6: Generate a JSON Report

```bash
python ioc-extractor.py sample.txt --output report.json
```

The extracted indicators will be displayed in the terminal and saved to a JSON report.

Note: The program does not overwrite an existing output file.

## 6. Example Usage

Create a file named `sample.txt` containing:

```text
Security Investigation Sample

IP Addresses:
192.168.1.10
8.8.8.8
999.999.999.999

Domains:
example.com
sub.example.org

URLs:
https://example.com/login
http://example.org/download

MD5:
d41d8cd98f00b204e9800998ecf8427e

SHA-1:
da39a3ee5e6b4b0d3255bfef95601890afd80709

SHA-256:
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Run the command:

```bash
python ioc-extractor.py sample.txt
```

These are illustrative test values, not confirmed malicious indicators.

## 7. Example Output

The output will be similar to:

```text
==================================================
             IOC EXTRACTION REPORT
==================================================

IPv4 Addresses:
  - 8.8.8.8
  - 192.168.1.10

URLs:
  - http://example.org/download
  - https://example.com/login

Domains:
  - example.com
  - example.org
  - sub.example.org

MD5 Hashes:
  - d41d8cd98f00b204e9800998ecf8427e

SHA-1 Hashes:
  - da39a3ee5e6b4b0d3255bfef95601890afd80709

SHA-256 Hashes:
  - e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

--------------------------------------------------
Total extracted indicators: 8
==================================================
```

The actual output may vary depending on the input file.

## 8. Challenges Faced

- Developing regular expressions to identify different IOC types.
- Validating IPv4 addresses and ignoring invalid addresses.
- Separating URL extraction from domain extraction.
- Identifying hashes based on hexadecimal character length.
- Handling missing input files and output errors.
- Organizing the results into readable categories.

## 9. Future Improvements

- Support defanged indicators such as `hxxps://example[.]com`.
- Add CSV report generation.
- Display line numbers for extracted indicators.
- Improve domain validation.
- Support additional file formats.
- Integrate threat intelligence APIs for further investigation.

## 10. Responsible Use

This tool is intended for educational and authorized cybersecurity analysis.

Extracted indicators should be investigated further. Finding an IP address, domain, URL, or hash does not automatically mean that it is malicious.

## 11. Learning Outcomes

This project demonstrates practical knowledge of:

- Python functions
- Regular expressions
- File handling
- Command-line arguments
- IPv4 validation
- JSON report generation
- Error handling
- Basic cybersecurity automation