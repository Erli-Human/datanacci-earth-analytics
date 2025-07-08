import gradio as gr
import requests
from PIL import Image
import io
import os
import random

# Define the URLs (same as before)
urls = [
    "https://sosrff.tsu.ru/new/shm.jpg",  # Resonance
    "https://volcanodiscovery.de/fileadmin/charts/seismic-activity-level.png",  # Geomagnetic
    "https://spaceweather.gfz-potsdam.de/fileadmin/rbm-forecast/Forecast_UTC_E_1_MeV_PA_50_latest_scatter_smooth_short.mp4",  # Geomagnetic
    "https://spaceweather.gfz.de/fileadmin/Aurora-Forecast/aurora_forecast_browser.webm",  # Geomagnetic
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/1024/0197.mp4",  # Using a valid mp4 for testing
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/1024/0197.mp4",  # Geomagnetic
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/1024/0197.mp4",  # Geomagnetic
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/1024/0197.mp4",  # Geomagnetic
]

def process_image(image):
    # Placeholder for image processing if needed
    return image

def create_gallery(urls):
    gallery = []
    for url in urls:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            image = Image.open(io.BytesIO(response.content))
            gallery.append(image)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image from {url}: {e}")
        except Exception as e:
            print(f"Error processing image from {url}: {e}")
    return gallery

with gr.Blocks() as demo:
    gallery_images = create_gallery(urls)

    with gr.Gallery(images=gallery_images, columns=1, object_fit="contain") as gallery:
        pass  # Gallery is created above

demo.launch()
