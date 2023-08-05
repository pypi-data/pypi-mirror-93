import os
import certifi
import requests
import logging

from requests.exceptions import SSLError
from pathlib import Path

test_url = "https://design.dataiku.vestas.net/"
certificate_dir = os.path.join(Path(__file__).parent, "certificates")


def add_certificates():
    path = certifi.where()
    # Get current certificates.
    with open(path, 'r') as f:
        certs = f.readlines()
    with open(path + ".bak", 'w') as f:
        f.writelines(certs)
    # Add Vestas certificates.
    for item in os.listdir(certificate_dir):
        certs.append("\n")
        certs.append("# Source: " + item)
        certs.append("\n")
        with open(os.path.join(certificate_dir, item), 'r') as f:
            cert = f.readlines()
            certs.extend(cert)
    # Write the result.
    with open(path, 'w') as f:
        f.writelines(certs)


def fix_ssl_error():
    try:
        r = requests.get(test_url)
    except SSLError:
        logging.info("Trying to fix SSL error.")
        add_certificates()
        # Check if the fix worked.
        try:
            r = requests.get(test_url)
            logging.info("SSL fix worked.")
        except SSLError:
            logging.info("SSL fix failed.")
