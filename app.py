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
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0193.mp4",  # Sun
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0304.mp4",  # Sun
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0131.mp4",  # Sun
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0171.mp4",  # Sun
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",  # Sun
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/Ic_flat_2d.mp4",  # Sun
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIBC.jpg",  # Sun
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/M_color_2d.mp4",  # Sun
    "https://www.solarsystemscope.com/"  # Universe Console
]

def infer_type(url):
    """Infers the file type from the URL."""
    if url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return 'image'
    elif url.endswith(('.mp4', '.webm')):
        return 'video'
    else:
        return 'other'

def load_media(url):
    """Loads media from a URL, handling errors."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses

        if url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image = Image.open(io.BytesIO(response.content))
            return image
        elif url.endswith(('.mp4', '.webm')):
            return url  # Return the URL for video (Gradio handles video URLs)
        else:
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
    gr.Markdown("# Datanacci Earth Observation Station")

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
        resonance_type = infer_type(resonance_url)
        resonance_image = load_media(resonance_url)
        if resonance_image:
            if resonance_type == 'image':
                gr.Image(resonance_image, label="Resonance Data")
            elif resonance_type == 'video':
                gr.Video(resonance_url, label="Resonance Data")
            else:
                gr.Text("Resonance Data (Unsupported Format)")
        else:
            gr.Text("Error loading Resonance Data")

        # Universe Console (Iframe)
        universe_url = urls[12]
        iframe_html = create_iframe_html(universe_url, 600, 400)
        gr.HTML(iframe_html)

demo.launch()
