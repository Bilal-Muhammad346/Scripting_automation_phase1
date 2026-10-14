# Backup and Monitoring Tool

## Tool Name

Backup and Monitoring Tool

## Objective

The objective of this Bash tool is to provide a simple Linux automation utility for creating compressed backups of directories and monitoring basic system information.

The tool is designed as a practical Bash scripting exercise for cybersecurity and automation.

## Features

 Create compressed `.tar.gz` backups of directories
 Automatically create the backup destination directory if it does not exist
 Add a timestamp to backup filenames
 Display basic system information
 Display hostname
 Display current user
 Display date and time
 Display disk usage
 Display memory usage
 Display system uptime
 Provide a simple helpusage option
 Handle basic errors such as missing source directories and invalid commands

## Requirements

 Linux operating system
 Bash shell
 `tar`
 `df`
 `free`
 `uptime`

The tool uses standard Linux command-line utilities.

## How to Run

Make the script executable

```bash
chmod +x tool.sh
```

### Display Help

```bash
.tool.sh --help
```

### Monitor System

```bash
.tool.sh monitor
```

### Create a Backup

```bash
.tool.sh backup source_directory backup_directory
```

Example

```bash
.tool.sh backup ~Documents ~Backups
```

## Example Usage

### System Monitoring

```bash
.tool.sh monitor
```

The tool displays information including the hostname, current user, datetime, disk usage, memory usage, and system uptime.

### Directory Backup

```bash
.tool.sh backup test_data backups
```

The tool creates a timestamped compressed backup such as

```text
backupstest_data_2026-10-11_12-30-00.tar.gz
```

## Example Output

Example monitoring output

```text
======================================
          SYSTEM MONITOR
======================================
Hostname kali
Current User kali
DateTime Sun Oct 11 123000 PKT 2026

Disk Usage
...

Memory Usage
...

System Uptime
...
```

Example backup output

```text
Starting backup...
Source test_data
Destination backupstest_data_2026-10-11_12-30-00.tar.gz

Backup completed successfully.
Backup file backupstest_data_2026-10-11_12-30-00.tar.gz

Backup size
...
```

## Challenges Faced

Some challenges during development included understanding Bash command-line arguments, handling directories and file paths, creating compressed archives with `tar`, checking whether directories exist, and implementing basic error handling.

Another challenge was understanding how Bash functions and the `case` statement can be used to organize different tool modes.

## Future Improvements

Possible future improvements include

 Add automatic scheduled backups
 Add backup retention and deletion of old backups
 Add logging of backup activities
 Add monitoring alerts when disk usage becomes high
 Add CPU usage monitoring
 Add backup verification
 Add configuration options
 Add email or notification support
 Add more detailed system health checks
