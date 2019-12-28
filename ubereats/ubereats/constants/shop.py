BASE_DOMAIN = "www.ubereats.com"
BASE_URL = "https://" + BASE_DOMAIN
BASE_URL_JP = BASE_URL + "/ja-JP/"
SHOP_BASE_URL = BASE_URL_JP + "feed/?pl="

MUSASHINAKAHARA_PLID = "JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFNiVBRCVBNiVFOCU5NCVCNSVFNCVCOCVBRCVFNSU4RSU5RiVFOSVBNyU4NSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpkYXpMbUtMMUdHQVJHSjFYRzlJZVpWWSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzNS41ODA3MTQzJTJDJTIybG9uZ2l0dWRlJTIyJTNBMTM5LjY0MjEwNyU3RA%3D%3D"  # noqa
MUSASHINAKAHARA_SHOP_URL = SHOP_BASE_URL + MUSASHINAKAHARA_PLID

MUSASHINAKAHARA_CARID = "eyJwbHVnaW4iOiJyZWNvbW1lbmRhdGlvbkZlZWRQbHVnaW4iLCJyZWNvbW1UeXBlIjoidG9wX3N0b3Jlc19ieV9jaXR5X3YyIn0%3D"  # noqa
POPULAR_BASE_URL = BASE_URL_JP + "search/?carid="

MUSASHINAKAHARA_POPULAR_URL = POPULAR_BASE_URL + MUSASHINAKAHARA_CARID + "&pl=" + MUSASHINAKAHARA_PLID  # noqa

MUSASHINAKAHARA_SEARCH_NAKAHARA_URL = MUSASHINAKAHARA_SHOP_URL + "&q=武蔵中原"
MUSASHINAKAHARA_SEARCH_SHINJO_URL = MUSASHINAKAHARA_SHOP_URL + "&q=武蔵新城"
MUSASHINAKAHARA_SEARCH_KOSUGI_URL = MUSASHINAKAHARA_SHOP_URL + "&q=武蔵小杉"

MIZONOKUCHI_PLID = "JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFNiVBRCVBNiVFOCU5NCVCNSVFNiVCQSU5RCVFMyU4MyU4RSVFNSU4RiVBMyVFOSVBNyU4NSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUo0eTVNRWlmMEdHQVJ3alFsMUtPVDRKNCUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzNS41OTkwNzIxOTk5OTk5OSUyQyUyMmxvbmdpdHVkZSUyMiUzQTEzOS42MTEwMTAyJTdE"  # noqa
MIZONOKUCHI_SHOP_URL = SHOP_BASE_URL + MIZONOKUCHI_PLID
