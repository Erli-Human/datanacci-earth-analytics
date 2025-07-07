import gradio as gr
import requests
from PIL import Image
import io
import os

# Define the URLs
urls = [
    "https://sosrff.tsu.ru/new/shm.jpg",  # Resonance
    "https://volcanodiscovery.de/fileadmin/charts/seismic-activity-level.png", #Geomagnetic
    "https://spaceweather.gfz-potsdam.de/fileadmin/rbm-forecast/Forecast_UTC_E_1_MeV_PA_50_latest_scatter_smooth_short.mp4", #Geomagnetic
    "https://spaceweather.gfz.de/fileadmin/Aurora-Forecast/aurora_forecast_browser.webm", #Geomagnetic
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0193.mp4", # Sun
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0304.mp4", # Sun
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0131.mp4", # Sun
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0171.mp4", # Sun
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg", # Sun
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/Ic_flat_2d.mp4", # Sun
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIBC.jpg", # Sun
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/M_color_2d.mp4", # Sun
    "https://www.solarsystemscope.com/" # Universe Console
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

# Categorize URLs
resonance_images = [urls[0]]
geomagnetic_data = [urls[1], urls[2], urls[3]]
sun_images = [urls[4], urls[5], urls[6], urls[7], urls[8], urls[9], urls[10], urls[11]]
universe_console = [urls[12]]

with gr.Blocks(css="body {background-color: black; color: silver;}") as demo:
    gr.Markdown("# Datanacci Earth Monitoring System")

    with gr.Tab("Resonance Images"):
        for url in resonance_images:
            gr.Image(display_content(url))

    with gr.Tab("Geomagnetic Data"):
        for url in geomagnetic_data:
            if url.endswith((".mp4", ".webm")):
                gr.Video(url)
            else:
                gr.Image(display_content(url))

    with gr.Tab("Sun Images"):
        for url in sun_images:
            if url.endswith((".mp4", ".webm")):
                gr.Video(url)
            else:
                gr.Image(display_content(url))

    with gr.Tab("Universe Console"):
        for url in universe_console:
            gr.HTML(f'<iframe src="{url}" width="600" height="400"></iframe>')

demo.launch()
