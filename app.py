import random
import gradio as gr
import requests
from PIL import Image
import io

# Define the URLs
urls = [
    "https://sosrff.tsu.ru/new/shm.jpg",  # Resonance
    "https://volcanodiscovery.de/fileadmin/charts/seismic-activity-level.png",  # Geomagnetic
    "https://spaceweather.gfz-potsdam.de/fileadmin/rbm-forecast/Forecast_UTC_E_1_MeV_PA_50_latest_scatter_smooth_short.mp4",  # Geomagnetic
    "https://spaceweather.gfz.de/fileadmin/Aurora-Forecast/aurora_forecast_browser.webm",  # Geomagnetic
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest1080.jpg",  # SDO 1080p
    "https://www.nasa.gov/sites/default/files/thumbnails/image/sdo_hmi_full_disk_20240515.jpg",
    "https://spaceweather.com/images2024/15may24/aurora_johndoe_big.jpg",
    "https://www.nasa.gov/sites/default/files/thumbnails/image/pia25696.jpg",  # Added an additional URL for testing.
]

def load_media(url):
    """Loads media from a URL, handling potential errors."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses

        if url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image = Image.open(io.BytesIO(response.content))
            return image
        elif url.endswith(('.mp4', '.webm')):
            return url  # Return the URL for video (Gradio handles video URLs)
        else:
            print(f"Unsupported file format: {url}")  # added print statement
            return None  # Unsupported format
    except requests.exceptions.RequestException as e:
        print(f"Error loading media from {url}: {e}")
        return None

def generate_star_background(width, height, num_images=30, star_density=0.003):
    """Generates a list of images for a star background animation."""
    images = []
    for _ in range(num_images):
        img = Image.new('RGB', (width, height), (0, 0, 0))
        pixels = img.load()
        for i in range(width):
            for j in range(height):
                if random.random() < star_density:
                    pixels[i, j] = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        images.append(img)
    return images

def create_iframe_html(url, width, height):
    """Creates the HTML for an iframe."""
    return f'<iframe src="{url}" width="{width}" height="{height}" frameborder="0" allowfullscreen></iframe>'

with gr.Blocks() as demo:
    gr.Markdown("# Datanacci Earth Analytics")

    # Star Background Animation
    star_images = generate_star_background(800, 600)
    with gr.Column():
        gr.Markdown("## Background Animation")
        with gr.Gallery(layout="grid", columns=1, object_fit="contain") as gallery:
            for img in star_images:
                gallery.add(img)

    # Content Blocks
    with gr.Column():
        gr.Markdown("## Data Streams")

        # Resonance
        resonance_url = urls[0]
        resonance_image = load_media(resonance_url)
        if resonance_image:
            gr.Image(resonance_image, label="Resonance Data")
        else:
            gr.Text("Error loading Resonance Data")

        # Example using multiple URLs
        for i in range(1, min(len(urls), 4)):  # Display up to 3 more images
            image_url = urls[i]
            image = load_media(image_url)
            if image:
                gr.Image(image, label=f"Image {i+1}")
            else:
                gr.Text(f"Error loading Image {i+1}")

        # Example Video
        video_url = urls[4]
        video_image = load_media(video_url)
        if video_image:
            gr.Video(video_image, label="Solar Dynamics Observatory")
        else:
            gr.Text("Error loading SDO Video")

demo.launch()
