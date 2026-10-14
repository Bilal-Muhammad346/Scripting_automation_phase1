#!/usr/bin/env python3

"""
IOC Extractor
-------------
A simple Python cybersecurity tool that extracts indicators
of compromise from a text file.

Supported indicators:
    - IPv4 addresses
    - URLs
    - Domain names
    - MD5 hashes
    - SHA-1 hashes
    - SHA-256 hashes

The tool can display results and optionally save them as JSON.
"""

import argparse
import ipaddress
import json
import re
import sys

from pathlib import Path
from urllib.parse import urlsplit


# --------------------------------------------------
# 1. Define regular expressions for IOC detection
# --------------------------------------------------

# Detect URL-like strings beginning with http:// or https://.
URL_PATTERN = re.compile(
    r"https?://[^\s<>\"']+",
    re.IGNORECASE
)

# Match strings that resemble IPv4 addresses.
IP_PATTERN = re.compile(
    r"(?<![\w.])"
    r"(?:\d{1,3}\.){3}\d{1,3}"
    r"(?![\w.])"
)

# Match MD5, SHA-1, and SHA-256 hexadecimal hashes.
HASH_PATTERN = re.compile(
    r"(?<![0-9a-fA-F])"
    r"(?:[0-9a-fA-F]{64}|"
    r"[0-9a-fA-F]{40}|"
    r"[0-9a-fA-F]{32})"
    r"(?![0-9a-fA-F])"
)

# Match domain-like names, including subdomains.
DOMAIN_PATTERN = re.compile(
    r"(?<![\w.-])"
    r"(?:[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,63}"
    r"(?![\w.-])"
)


# --------------------------------------------------
# 2. Read the input file
# --------------------------------------------------

def read_file(file_path):
    """
    Read a text file and return its contents.

    Raises an error if the file cannot be read.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"The input path is not a file: {file_path}"
        )

    # Read text while replacing invalid UTF-8 characters.
    return path.read_text(
        encoding="utf-8",
        errors="replace"
    )


# --------------------------------------------------
# 3. Extract and validate IPv4 addresses
# --------------------------------------------------

def extract_ips(text):
    """
    Find IPv4-like strings and validate their addresses.
    """

    results = set()

    for candidate in IP_PATTERN.findall(text):

        try:
            # Reject invalid addresses such as 999.999.1.1.
            address = ipaddress.ip_address(candidate)

            if address.version == 4:
                results.add(str(address))

        except ValueError:
            # Ignore strings that are not valid IP addresses.
            continue

    return sorted(results)


# --------------------------------------------------
# 4. Extract URLs
# --------------------------------------------------

def extract_urls(text):
    """
    Extract HTTP and HTTPS URLs.

    Remove common trailing punctuation from matched URLs.
    """

    results = set()

    for candidate in URL_PATTERN.findall(text):

        # Remove punctuation commonly found after a URL
        # in a sentence.
        candidate = candidate.rstrip(".,;:!?)]}")

        try:
            parsed = urlsplit(candidate)

            # Require a hostname and an HTTP(S) scheme.
            if parsed.scheme.lower() not in ("http", "https"):
                continue

            if not parsed.hostname:
                continue

            results.add(candidate)

        except ValueError:
            # Ignore malformed URLs.
            continue

    return sorted(results)


# --------------------------------------------------
# 5. Extract domain names
# --------------------------------------------------

def extract_domains(text):
    """
    Extract domain-like names from text.

    URLs are handled separately to avoid including
    their hostnames twice.
    """

    # Remove URLs before searching for standalone domains.
    text_without_urls = URL_PATTERN.sub(" ", text)

    results = set()

    for candidate in DOMAIN_PATTERN.findall(text_without_urls):

        domain = candidate.lower().rstrip(".")

        # Avoid accepting strings that are actually IPv4
        # addresses or malformed IP-like values.
        try:
            ipaddress.ip_address(domain)
            continue

        except ValueError:
            pass

        results.add(domain)

    return sorted(results)


# --------------------------------------------------
# 6. Extract file hashes
# --------------------------------------------------

def extract_hashes(text):
    """
    Extract hexadecimal strings that resemble common hashes.
    """

    results = {
        "MD5": set(),
        "SHA-1": set(),
        "SHA-256": set()
    }

    for candidate in HASH_PATTERN.findall(text):

        length = len(candidate)
        candidate = candidate.lower()

        if length == 32:
            results["MD5"].add(candidate)

        elif length == 40:
            results["SHA-1"].add(candidate)

        elif length == 64:
            results["SHA-256"].add(candidate)

    # Convert sets into sorted lists for consistent output.
    return {
        hash_type: sorted(values)
        for hash_type, values in results.items()
    }


# --------------------------------------------------
# 7. Extract all supported IOC types
# --------------------------------------------------

def extract_iocs(text):
    """
    Run all IOC extraction functions and combine results.
    """

    return {
        "ipv4_addresses": extract_ips(text),
        "urls": extract_urls(text),
        "domains": extract_domains(text),
        "hashes": extract_hashes(text)
    }


# --------------------------------------------------
# 8. Display results
# --------------------------------------------------

def display_results(results):
    """
    Display extracted IOCs in a readable format.
    """

    print("\n" + "=" * 50)
    print("             IOC EXTRACTION REPORT")
    print("=" * 50)

    categories = [
        ("IPv4 Addresses", results["ipv4_addresses"]),
        ("URLs", results["urls"]),
        ("Domains", results["domains"]),
        ("MD5 Hashes", results["hashes"]["MD5"]),
        ("SHA-1 Hashes", results["hashes"]["SHA-1"]),
        ("SHA-256 Hashes", results["hashes"]["SHA-256"])
    ]

    total = 0

    for title, indicators in categories:

        print(f"\n{title}:")

        if indicators:
            for indicator in indicators:
                print(f"  - {indicator}")

            total += len(indicators)

        else:
            print("  No indicators found.")

    print("\n" + "-" * 50)
    print(f"Total extracted indicators: {total}")
    print("=" * 50)


# --------------------------------------------------
# 9. Save results to a JSON file
# --------------------------------------------------

def save_report(results, output_path):
    """
    Save the extracted indicators in JSON format.
    """

    path = Path(output_path)

    # Do not overwrite an existing report accidentally.
    if path.exists():
        raise FileExistsError(
            f"Output file already exists: {output_path}"
        )

    with path.open("x", encoding="utf-8") as report_file:
        json.dump(
            results,
            report_file,
            indent=4
        )

        report_file.write("\n")

    print(f"\nReport saved successfully: {path}")


# --------------------------------------------------
# 10. Main program
# --------------------------------------------------

def main():
    """
    Parse command-line arguments and run the extractor.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Extract IPv4 addresses, URLs, domains, "
            "and common file hashes from a text file."
        )
    )

    parser.add_argument(
        "input_file",
        help="Path to the text file to analyze"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Optional path for saving a JSON report"
    )

    args = parser.parse_args()

    try:
        # Read the file.
        text = read_file(args.input_file)

        # Extract supported indicators.
        results = extract_iocs(text)

        # Print the results.
        display_results(results)

        # Save a JSON report if requested.
        if args.output:
            save_report(results, args.output)

    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


# Run the program only when executed directly.
if __name__ == "__main__":
    sys.exit(main())