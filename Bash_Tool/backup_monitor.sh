#!/bin/bash

# Backup and Monitoring Tool
# Phase 1 - Bash Cybersecurity/Automation Tool
# This tool creates backups and displays basic system information.

show_help() {
    echo "======================================"
    echo "      Backup and Monitoring Tool"
    echo "======================================"
    echo
    echo "Usage:"
    echo "  $0 backup <source> <destination>"
    echo "  $0 monitor"
    echo "  $0 --help"
    echo
    echo "Examples:"
    echo "  $0 backup ~/Documents ~/Backups"
    echo "  $0 monitor"
}

monitor_system() {
    echo "======================================"
    echo "          SYSTEM MONITOR"
    echo "======================================"

    echo "Hostname: $(hostname)"
    echo "Current User: $(whoami)"
    echo "Date/Time: $(date)"

    echo
    echo "Disk Usage:"
    df -h

    echo
    echo "Memory Usage:"
    free -h

    echo
    echo "System Uptime:"
    uptime
}

create_backup() {

    SOURCE="$1"
    DESTINATION="$2"

    if [ ! -d "$SOURCE" ]; then
        echo "Error: Source directory does not exist."
        exit 1
    fi

    if [ ! -d "$DESTINATION" ]; then
        echo "Backup directory does not exist."
        echo "Creating: $DESTINATION"
        mkdir -p "$DESTINATION"
    fi

    TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

    SOURCE_NAME=$(basename "$SOURCE")

    BACKUP_FILE="${DESTINATION}/${SOURCE_NAME}_${TIMESTAMP}.tar.gz"

    echo
    echo "Starting backup..."
    echo "Source: $SOURCE"
    echo "Destination: $BACKUP_FILE"

    tar -czf "$BACKUP_FILE" -C "$(dirname "$SOURCE")" "$SOURCE_NAME"

    if [ $? -eq 0 ]; then
        echo
        echo "Backup completed successfully."
        echo "Backup file: $BACKUP_FILE"
        echo
        echo "Backup size:"
        du -h "$BACKUP_FILE"
    else
        echo
        echo "Error: Backup failed."
        exit 1
    fi
}

case "$1" in

    backup)
        if [ "$#" -ne 3 ]; then
            echo "Error: Backup requires source and destination."
            echo
            show_help
            exit 1
        fi

        create_backup "$2" "$3"
        ;;

    monitor)
        monitor_system
        ;;

    --help|-h)
        show_help
        ;;

    *)
        echo "Error: Invalid option."
        echo
        show_help
        exit 1
        ;;

esac