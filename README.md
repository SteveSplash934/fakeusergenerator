# Fake User Generator

![Logo](statics/NCtmcGFz1BWaPBRdbhEn60KPcdNqhQ_rO5K6s7TZj8o.webp)

This project is a Python-based fake user identity generator that fetches data from a website and generates fake user information, including basic details (name, address, SSN, etc.), email, phone, financial, personal, and work-related information. It also supports generating a QR code that contains all the extracted data.

## Features

- Fetches fake user data from **Fake Name Generator**.
- Generates **random SSN** and **email addresses**.
- Extracts and categorizes data into multiple sections (e.g., Basic Info, Online Info, Financial Info).
- Optionally **generates QR codes** containing the extracted data.
- Saves the extracted data in a **timestamped text file** and optionally as a **QR code image**.

## Requirements

Before you run the script, ensure you have the following libraries installed:

```bash
pip install requests beautifulsoup4 qrcode[pil]
```

- `requests`: For sending HTTP requests to fetch the fake user data.
- `beautifulsoup4`: For parsing and extracting data from the HTML page.
- `qrcode`: For generating QR codes with the extracted user data.

## Configuration

The program is configured using a `config.ini` file located in the same directory as the script. Here's an example configuration file:

### `config.ini`

```ini
[advanced_options]
name_set = us              # Name set to use (us, uk, etc.)
country = us               # Country to generate user data from
gen = 0                    # Gender (0 for random, 1 for male, 2 for female)
age_min = 18               # Minimum age of the generated user
age_max = 99               # Maximum age of the generated user

[qr_options]
generate_qr = On           # On or Off to enable/disable QR code generation
```

- `name_set`: Determines the set of names to use for the generated identity. (e.g., `us` for US names).
- `country`: The country from which the fake identity is generated.
- `gen`: Gender specification (`0` for random, `1` for male, `2` for female).
- `age_min`: Minimum age of the generated identity.
- `age_max`: Maximum age of the generated identity.
- `generate_qr`: Controls whether a QR code should be generated with the identity information.

## Running the Script

1. Clone this repository:

   ```bash
   git clone https://github.com/SteveSplash934/fakeusergenerator.git
   ```

2. Navigate to the project folder:

   ```bash
   cd fake-user-generator
   ```

3. Ensure all the dependencies are installed:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute the script:

   ```bash
   python fakeusergenerator.py
   ```

   This will fetch the fake identity data, extract the information, save it to a timestamped text file, and optionally generate a QR code containing the data.

## Example Output

The output will contain two files:

- **Text File**: A timestamped `.txt` file containing the extracted information. Example: `identity_info_2025-01-08_15-30-00.txt`.
- **QR Code Image**: If enabled in the `config.ini`, a PNG file containing the QR code will also be saved. Example: `identity_info_2025-01-08_15-30-00.png`.

The text file will have data like this:

```
Basic Info:
  Name: Carolyn T. Benavides
  Address: 123 Fake St, Springfield, IL 62701
  ...

Online Info:
  Email Address: carolyntbenavides@teleworm.us (INBOX: https://www.fakemailgenerator.com/#/teleworm.us/carolyntbenavides/)
  Username: carolyntbenavides
  Password: secretpassword123
  ...

Phone Info:
  Phone: (555) 123-4567
  Country Code: +1

Financial Info:
  Mastercard: 1234-5678-9876-5432
  Expiry: 12/23
  CVC2: 123
  ...

Personal Info:
  Height: 5'6"
  Weight: 135 lbs
  Blood Type: O+
  ...

Work Info:
  Company: Fake Corp
  Occupation: Software Engineer
  ...

Shipping Info:
  UPS Tracking Number: 1Z999AA10123456789
  QR Code: https://www.fakenamegenerator.com/#/teleworm.us/carolyntbenavides/
  ...
```

## QR Code Generation

If the `generate_qr` option is set to `On` in the `config.ini` file, the script will generate a QR code containing all the extracted identity information. This QR code will be saved as a `.png` file (or any image format you prefer) in the `output/` directory.

The QR code can be scanned with any QR code reader to view the encoded data.

## Troubleshooting

### Program not runing normally:

If config fail and script abort unsuccessfully, remove the comments '# ...', example, your config file should now look like this:

```ini
[advanced_options]
name_set = us
country = us
gen = 0
age_min = 18
age_max = 99

[qr_options]
generate_qr = On
```

### Missing `qrcode` library:

If you get an error about the `qrcode` library not being installed, make sure you have the required library:

```bash
pip install qrcode[pil]
```

### Fetching Errors:

If the script fails to fetch the HTML content from the website, it could be due to:

- Invalid URL parameters.
- Network issues (e.g., no internet connection).
- Temporary issues with the website.

The script will print an error message if it fails to fetch the data.

## Future Enhancements

- **Integrate with Telegram bot**: Add support for sending generated user info via a Telegram bot.
- **Integrate with Discord bot**: Add support for sending generated user info via a Discord bot.
- **Make it a free API**: Expose an API for generating fake user data programmatically.

## Credits

This project makes use of the following website for generating fake user data:

- [Fake Name Generator](https://www.fakenamegenerator.com)

Special thanks to the creators of this tool for providing such a comprehensive and useful service.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
