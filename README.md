# Password Transfering

Simple and convenient migration tool for transferring passwords from Kaspersky Password Manager to Apple Passwords.


## Usage

1. Export your passwords from Kaspersky Password Manager to a text file
2. Update the `INPUT_FILE` variable in `main.py` to point to your exported file (default: `kasperesky_passwords.txt`)
3. Install dependencies and run the script:

```bash
uv sync
uv run main.py
```

4. The script will generate `apple_passwords.csv` in the current directory
5. Import the CSV file into Apple Passwords
