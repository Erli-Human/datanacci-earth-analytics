import gradio as gr
import requests
from PIL import Image
import io
import os

# Define the URLs
urls = [
    "https://sosrff.tsu.ru/new/shm.jpg",
    "https://volcanodiscovery.de/fileadmin/charts/seismic-activity-level.png",
    "https://spaceweather.gfz-potsdam.de/fileadmin/rbm-forecast/Forecast_UTC_E_1_MeV_PA_50_latest_scatter_smooth_short.mp4",
    "https://spaceweather.gfz.de/fileadmin/Aurora-Forecast/aurora_forecast_browser.webm",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0193.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0304.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0131.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0171.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/Ic_flat_2d.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIBC.jpg",
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/M_color_2d.mp4",
    "https://www.solarsystemscope.com/"
]

def infer_type(url):
    """Infers the type of content from the URL."""
    if url.endswith(".jpg") or url.endswith(".png"):
        return "Image", url
    elif url.endswith(".mp4") or url.endswith(".webm"):
        return "Video", url
    elif url.endswith(".html") or url.endswith("/"):
        return "Website", url
    else:
        return "Unknown", url

def display_content(url):
    """Displays the content based on its type."""
    content_type, actual_url = infer_type(url)

    if content_type == "Image":
        try:
            response = requests.get(actual_url, stream=True)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            image = Image.open(io.BytesIO(response.content))
            return image
        except requests.exceptions.RequestException as e:
            return f"Error loading image: {e}"

    elif content_type == "Video":
        return actual_url  # Directly return the URL for Gradio to handle

    elif content_type == "Website":
        return actual_url # Directly return the URL for Gradio to handle
    else:
        return "Unsupported content type"

# Organize content into categories
images = [url for url in urls if url.endswith((".jpg", ".png"))]
videos = [url for url in urls if url.endswith((".mp4", ".webm"))]
websites = [url for url in urls if url.endswith((".html", "/"))]

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Datanacci Earth Monitoring System")  # Application Name

    with gr.Tab("Images"):
        with gr.Row():
            for i, url in enumerate(images):
                with gr.Column():
                    gr.Image(display_content(url), label=f"Image {i+1}")

    with gr.Tab("Videos"):
        with gr.Row():
            for i, url in enumerate(videos):
                with gr.Column():
                    gr.Video(url, label=f"Video {i+1}")

    with gr.Tab("Websites"):
        with gr.Row():
            for i, url in enumerate(websites):
                with gr.Column():
                    gr.HTML(f'<iframe src="{url}" width="600" height="400"></iframe>', label=f"Website {i+1}")


demo.launch()
