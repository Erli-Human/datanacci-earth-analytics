import requests
from PIL import Image
import io

def process_image(image_url):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Check if the URL points to an image (jpg, png, jpeg)
        if not image_url.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Skipping video or unsupported file: {image_url}")
            return None

        image = Image.open(io.BytesIO(response.content))
        return image

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or processing image from {image_url}: {e}")
        return None
    except Exception as e:
        print(f"Error processing image from {image_url}: {e}")
        return None

def create_gallery(urls):
    gallery_images = []
    for url in urls:
        image = process_image(url)
        if image:
            gallery_images.append(image)
    return gallery_images

# List of URLs
urls = [
    "https://spaceweather.gfz-potsdam.de/fileadmin/rbm-forecast/Forecast_UTC_E_1_MeV_PA_50_latest_scatter_smooth_short.mp4",
    "https://spaceweather.gfz.de/fileadmin/Aurora-Forecast/aurora_forecast_browser.webm",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/1024/0197.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/1024/0197.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/1024/0197.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/1024/0197.mp4",
    "https://www.nasa.gov/sites/default/files/thumbnails/image/sdo_hmi_full_disk.jpg",
    "https://www.nasa.gov/sites/default/files/thumbnails/image/pia25329.jpg",
    "https://www.nasa.gov/sites/default/files/thumbnails/image/sdo_hmi_full_disk.jpg"

]

gallery_images = create_gallery(urls)

import gradio as gr

with gr.Blocks() as demo:
    with gr.Gallery(images=gallery_images, columns=1, object_fit="contain") as gallery:
        pass

demo.launch()
