"""
This script generates fake user information from a specified API, 
such as name, address, email, and more. The data can be saved in 
text files and QR codes can be generated. 
"""

import os
import random
from datetime import datetime
import configparser
import urllib.parse
import requests
from bs4 import BeautifulSoup
import qrcode

# List of common user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 Edge/17.17134"
]

# Unwanted phrases to remove
UNWANTED_PHRASES = [
    "You should click here to find out if your SSN is online.",
    "This is a real email address. Click here to activate it!"
]

def fetch_html_with_random_ua(url):
    """Fetch the HTML content of a URL using a random User-Agent."""
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    print(f"Fetching URL: {url}")    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if not response.status_code == 200:
            return None
        return response.text
        # else:
        #     print(f"Error: Failed to retrieve page (status code: {response.status_code})")
        #     return None
    except requests.RequestException as e:
        print(f"Error: An exception occurred while fetching the page: {e}")
        return None

def remove_unwanted_phrases(text):
    """Remove any unwanted phrases from the given text."""
    for phrase in UNWANTED_PHRASES:
        text = text.replace(phrase, "").strip()
    return text

def generate_random_ssn_last_digits():
    """Generate a random 4-digit number to complete the SSN."""
    return str(random.randint(1000, 9999))

def load_config(config_file='config.ini'):
    """Load the configuration from a .ini file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def construct_url(config):
    """Construct the URL based on the config values."""
    name_set = config.get('advanced_options', 'name_set', fallback='us')
    country = config.get('advanced_options', 'country', fallback='us')
    gen = config.get('advanced_options', 'gen', fallback='0')
    age_min = config.get('advanced_options', 'age_min', fallback='18')
    age_max = config.get('advanced_options', 'age_max', fallback='99')
    url_base = "https://www.fakenamegenerator.com/advanced.php?t=country"
    params = {
        'n[]': name_set,
        'c[]': country,
        'gen': gen,
        'age-min': age_min,
        'age-max': age_max
    }
    url = url_base + '&' + urllib.parse.urlencode(params, doseq=True)
    return url

def construct_email_url(email):
    """Generate the URL for the fake email inbox."""
    domain = email.split('@')[1]
    username = email.split('@')[0]
    return f"https://www.fakemailgenerator.com/#/{domain}/{username}/"

def generate_qr_code(data, output_dir='output', config=None):
    """Generate a QR code from the provided data and save it as an image."""
    # Check if QR code generation is enabled in the config
    if config and config.get('qr_options', 'generate_qr', fallback='Off') == 'On':
        # Create a QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Construct the filename using a timestamp for uniqueness
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        img_path = os.path.join(output_dir, f'identity_info_{timestamp}.png')  # Save as PNG by default
        img.save(img_path)
        print(f"QR code saved at: {img_path}")
        return img_path
    
    print("QR code generation is disabled.")
    return None

def extract_identity_info(html_content, output_dir='output', config=None):
    """Extract the identity information and generate a QR code for the email URL if enabled."""

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the name and address
    address_section = soup.find('div', class_='address')
    name = address_section.find('h3').get_text(strip=True)
    address = address_section.find('div', class_='adr').get_text(strip=True).replace("\n", " ").strip()
    
    # Initialize a dictionary to categorize the extracted data
    categorized_data = {
        'Basic Info': {},
        'Online Info': {},
        'Phone Info': {},
        'Financial Info': {},
        'Personal Info': {},
        'Work Info': {},
        'Shipping Info': {}
    }
    
    # Basic Info: Name, SSN, Mother's maiden name, Birthday, Age, Tropical zodiac, Geo coordinates
    categorized_data['Basic Info']['Name'] = name
    categorized_data['Basic Info']['Address'] = address

    # Extract information from <dl class="dl-horizontal">
    dl_sections = soup.find_all('dl', class_='dl-horizontal')
    for dl in dl_sections:
        dt = dl.find('dt')
        dd = dl.find('dd')
        
        if dt and dd:
            key = dt.get_text(strip=True)            
            value = dd.get_text(separator=" ", strip=True)            
            value = remove_unwanted_phrases(value)            
            if key.lower() == 'ssn':
                value = value.split('-')[0] + '-' + value.split('-')[1] + '-' + generate_random_ssn_last_digits()
            
            # Categorize based on the key
            if key.lower() in ['ssn', 'mother\'s maiden name', 'birthday', 'age', 'tropical zodiac', 'geo coordinates']:
                categorized_data['Basic Info'][key] = value
            elif key.lower() in ['email address', 'username', 'password', 'website', 'browser user agent']:
                categorized_data['Online Info'][key] = value
            elif key.lower() in ['phone', 'country code']:
                categorized_data['Phone Info'][key] = value
            elif key.lower() in ['mastercard', 'expires', 'cvc2', 'western union mtcn', 'moneygram mtcn']:
                categorized_data['Financial Info'][key] = value
            elif key.lower() in ['height', 'weight', 'blood type', 'favorite color', 'vehicle']:
                categorized_data['Personal Info'][key] = value
            elif key.lower() in ['company', 'occupation']:
                categorized_data['Work Info'][key] = value
            elif key.lower() in ['ups tracking number', 'guid', 'qr code']:
                categorized_data['Shipping Info'][key] = value
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = os.path.join(output_dir, f'identity_info_{timestamp}.txt')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for category, items in categorized_data.items():
            f.write(f"{category}:\n")
            for key, value in items.items():
                f.write(f"  {key}: {value}\n")
            f.write("\n")
    
    print(f"Identity information saved to {output_file}")

    # Generate a QR code with the entire extracted information
    full_data = "\n".join(
        [f"{category}: {dict(items)}" for category, items in categorized_data.items()]
        )
    generate_qr_code(full_data, output_dir=output_dir, config=config)

def main():
    """Main function to fetch the identity information and save it to a file."""

    # Load the config file
    config = load_config()

    # Construct the URL based on the config
    url = construct_url(config)

    # Fetch the HTML content from the generated URL
    html_content = fetch_html_with_random_ua(url)

    if html_content:
        # Extract the identity information and save it to a file, including QR code if enabled
        extract_identity_info(html_content, config=config)
    else:
        print("Failed to fetch HTML content.")


if __name__ == "__main__":
    main()
