import base64
import requests


def encodeIt(plainText):
    # Encode the string as bytes, then to Base64
    encoded = base64.b64encode(plainText.encode("utf-8"))
    # Convert back to string for display
    return encoded


def decodeIt(encodedText):
    # Decode Base64 to original bytes
    decoded = base64.b64decode(encodedText)
    # Convert bytes back to string
    return decoded.decode("utf-8")


if __name__ == "__main__":
    r = requests.get("https://www.gutenberg.org/cache/epub/74614/pg74614.txt")

    print(r.text)

    encoded = encodeIt(r.text)
    print(encoded)

    decoded = decodeIt(encoded)
    print(decoded)
