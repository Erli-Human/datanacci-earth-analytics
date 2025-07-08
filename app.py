import gradio as gr
import requests
from PIL import Image

def infer_type(url):
    """Infers the type of content from the URL."""
    if url.endswith((".jpg", ".jpeg", ".png")):
        return "Image", url
    elif url.endswith((".mp4", ".webm")):
        return "Video", url
    elif url.endswith(".html") or url.endswith("/"):
        return "Website", url
    else:
        return "Unknown", url

def display_content(url):
    """Displays the content based on the URL with error handling."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        if url.endswith((".jpg", ".jpeg", ".png")):
            image = Image.open(response.raw)
            return image
        elif url.endswith((".mp4", ".webm")):
            return url
        else:
            return url

    except requests.exceptions.RequestException as e:
        print(f"Error loading content from {url}: {e}")
        return "Error loading content"

# ... your code ...

if __name__ == "__main__":
    demo.launch(share=True, server_timeout=600)
