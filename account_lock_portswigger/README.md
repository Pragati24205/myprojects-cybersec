## Description
This script automates a PortSwigger-style authentication lab
demonstrating username enumeration via account lock behavior.

## Vulnerability
Account lock is applied only to valid usernames, causing a
different error message after repeated failed attempts.

## Detection Method
- Response length comparison
- Valid usernames trigger longer responses after lock
- Valid passwords produce the shortest response

## Scope
This script is lab-specific and not intended for real-world targets.
Behavior-based exploitation requires per-target adaptation.

## Learning Outcome
- Understanding stateful authentication logic
- Mapping Burp Intruder behavior to Python automation
