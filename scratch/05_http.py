"""Day 1, script 5 of 5 — httpx.

TASK
  GET https://httpbin.org/json with httpx.
  Print the status code and one field from the JSON body.
  Then request a URL that 404s and handle it without a traceback.

WHAT TO NOTICE
  httpx does NOT raise on a 4xx by default. You either check .status_code
  or call .raise_for_status() yourself. Decide which you want and know why.

DONE WHEN
  The happy path prints, and the 404 is handled rather than crashing.
"""

import httpx

# TODO: your code here
response = httpx.get("https://httpbin.org/json")
print(f"Status code: {response.status_code}")
data = response.json()
print(f"Slideshow title: {data['slideshow']['title']}")

# Handle a 404
try:
    response = httpx.get("https://httpbin.org/status/404")
    response.raise_for_status()
except httpx.HTTPError as e:
    print(f"HTTP error occurred: {e}")