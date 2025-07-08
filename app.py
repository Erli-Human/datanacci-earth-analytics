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

# Define your URLs here
urls = [
    "https://www.easygifanimator.net/images/samples/video-to-gif-sample.gif",
    "https://www.nasa.gov/sites/default/files/thumbnails/image/j22-00470.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
]

# Create the Gradio interface using gr.Blocks
with gr.Blocks() as demo:
    for url in urls:
        try:
            if url.endswith((".jpg", ".jpeg", ".png")):
                image = Image.open(requests.get(url, stream=True).raw)
                gr.Image(value=image, label=url)
            elif url.endswith((".mp4", ".webm")):
                gr.Video(url, label=url)
            else:
                gr.HTML(f"<h1>{url}</h1>")
        except Exception as e:
            gr.HTML(f"<h1>Error loading {url}: {e}</h1>")

# Launch the interface
if __name__ == "__main__":
    demo.launch(share=False)
