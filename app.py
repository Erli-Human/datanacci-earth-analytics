import gradio as gr
from PIL import Image
import requests
import io
import math

# Define the URLs
urls = [
    "https://sosrff.tsu.ru/new/shm.jpg",  # Resonance
    "https://volcanodiscovery.de/fileadmin/charts/seismic-activity-level.png",  # Geomagnetic
    "https://spaceweather.gfz-potsdam.de/fileadmin/rbm-forecast/Forecast_UTC_E_1_MeV_PA_50_latest_scatter_smooth_short.mp4",
    "https://spaceweather.gfz.de/fileadmin/Aurora-Forecast/aurora_forecast_browser.webm",  # Aurora
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest1080.jpg",  # SDO Image
    "https://sso.org/images/events/nasional-dagang.png",  # SSO Image
    "https://spaceweather.gfz.de/fileadmin/rbm-forecast/Forecast_UTC_E_1_MeV_PA_50_latest_scatter_smooth_short.mp4",
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/Ic_flat_2d.mp4",  # JSOC 1 Image
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",  # SDO HMI Image
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/M_color_2d.mp4",  # JSOC 1 Video
    "https://sso.org/images/events/20220830.png",  # SSO Image
    "https://spaceweather.gfz.de/fileadmin/Aurora-Forecast/aurora_forecast_browser2.webm",  # Aurora Forecast 2
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIBC.jpg",  # SDO HMIC Image
    "https://sso.org/images/events/20220825.png",  # SSO Image
]

# Define a dictionary to hold the URLs for each type of media
media_types = {
    'images': [],
    'videos': []
}

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

def create_columns():
    global media_types
    
    for i in range(len(urls)):
        if urls[i].endswith(('.jpg', '.jpeg', '.png', '.gif')):
            media_types['images'].append(urls[i])
        else:
            media_types['videos'].append(urls[i])

create_columns()

# Create the grid with separate columns
demo = gr.Blocks()
grid_columns = 4
grid_rows = -(-math.ceil(len(media_types['images']) / grid_columns))  # Calculate the number of rows needed

for i in range(grid_rows):
    row = []
    
    for j in range(grid_columns):
        if media_types['images']:
            image_url = media_types['images'][i * grid_columns + j]
            row.append(gr.Image(image=load_media(image_url)))
        
        elif len(media_types['videos']) > 0:
            video_url = media_types['videos'][i * grid_columns + j]
            row.append(gr.Video(url=video_url))
    
    if len(row) == grid_columns:
        demo.add_row(*row)

demo.launch()
