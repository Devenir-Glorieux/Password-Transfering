import csv
import re
from pathlib import Path
from structlog import get_logger


INPUT_FILE = Path("kasperesky_passwords.txt")
OUTPUT_FILE = Path("apple_passwords.csv")


logger = get_logger()


def parse_password_entry(text: str) -> dict[str, str]:
    entry: dict[str, str] = {
        "Title": "",
        "URL": "",
        "Username": "",
        "Password": "",
        "Notes": "",
        "OTPAuth": ""
    }

    website_name_match = re.search(r"Website name:\s*(.+)", text, re.IGNORECASE)
    application_match = re.search(r"Application:\s*(.+)", text, re.IGNORECASE)
    account_name_match = re.search(r"Account name:\s*(.+)", text, re.IGNORECASE)
    
    if website_name_match:
        entry["Title"] = website_name_match.group(1).strip()
    elif application_match:
        entry["Title"] = application_match.group(1).strip()
    elif account_name_match:
        entry["Title"] = account_name_match.group(1).strip()

    url_match = re.search(r"Website URL:\s*(.+)", text, re.IGNORECASE)
    if url_match:
        entry["URL"] = url_match.group(1).strip()

    login_match = re.search(r"Login:\s*(.+)", text, re.IGNORECASE)
    login_name_match = re.search(r"Login name:\s*(.+)", text, re.IGNORECASE)
    
    if login_match:
        entry["Username"] = login_match.group(1).strip()
    elif login_name_match:
        entry["Username"] = login_name_match.group(1).strip()
    
    password_match = re.search(r"Password:\s*(.+)", text, re.IGNORECASE)
    if password_match:
        entry["Password"] = password_match.group(1).strip()
    
    comment_match = re.search(r"Comment:\s*(.+)", text, re.IGNORECASE)
    if comment_match:
        comment = comment_match.group(1).strip()
        if comment: 
            entry["Notes"] = comment
    
    return entry


def parse_password_file(file_path: Path) -> list[dict[str, str]]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    entries_text = content.split("---")
    entries: list[dict[str, str]] = []
    for entry_text in entries_text:
        entry_text = entry_text.strip()
        if not entry_text or entry_text.lower() in ("websites", "other accounts"):
            continue
        entry = parse_password_entry(entry_text)
        if entry["Title"] or entry["URL"]:
            entries.append(entry)
    return entries


def write_csv(entries: list[dict[str, str]], output_path: Path) -> None:
    fieldnames = ["Title", "URL", "Username", "Password", "Notes", "OTPAuth"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)


def main():
    try:
        entries = parse_password_file(INPUT_FILE)
        if not entries:
            logger.warning("No password entries found in the file!")
            return
        
        logger.info(f"Found {len(entries)} password entries")
        write_csv(entries, OUTPUT_FILE)
        
        logger.info("Successfully converted to CSV", output_file=OUTPUT_FILE)
        logger.info(f"Entries converted: {len(entries)}")
        
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise


if __name__ == "__main__":
    main()
