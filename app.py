import gradio as gr
from PIL import Image
import requests
import io

# Define the URLs
urls = [
    "https://sosrff.tsu.ru/new/shm.jpg",  
    "https://volcanodiscovery.de/fileadmin/charts/seismic-activity-level.png",
    "https://spaceweather.gfz-potsdam.de/fileadmin/rbm-forecast/Forecast_UTC_E_1_MeV_PA_50_latest_scatter_smooth_short.mp4",
    "https://spaceweather gfz.de/fileadmin/Aurora-Forecast/aurora_forecast_browser.webm",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest1080.jpg",
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/Ic_flat_2d.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/M_color_2d.mp4"
]

def load_media(url):
    """Loads media from a URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error loading media from {url}: {e}")
        return None
    if url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        image = Image.open(io.BytesIO(response.content))
        return image
    elif url.endswith(('.mp4', '.webm')):
        return url  # Return the URL for video

def create_iframe_html(url, width, height):
    """Creates the HTML for an iframe."""
    return f'<iframe src="{url}" width="{width}" height="{height}" frameborder="0" allowfullscreen></iframe>'

with gr.Blocks() as demo:
    grid = gr.Grid(systems=[1, 3])
    
    # Resonance
    resonance_image = load_media(urls[0])
    if resonance_image:
        grid.add(Image(resonance_image))
        
    # Geomagnetic Activity (Seismic)
    geomagnetic_image = load_media(urls[2])
    if geomagnetic_image:
        grid.add(Image(geomagnetic_image))
    
    # Aurora Forecast
    aurora_image = load_media(urls[1])
    if aurora_image:
        grid.add(Image(aurora_image))
        
    # SDO 1080p
    sdo_image_1 = load_media(urls[3])
    if sdo_image_1:
        grid.add(Image(sdo_image_1))
        
    # Videos (SOLAR, JSOC)
    video_url_1 = urls[4]
    gr.Video(load_media(video_url_1), label="Solar Dynamics Observatory")
    
    video_url_2 = urls[7]
    gr.Video(load_media(video_url_2), label="JSOC 1")

demo.launch()
