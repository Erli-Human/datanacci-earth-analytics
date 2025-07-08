import requests
from PIL import Image
import gradio as gr
import math
import io

# List of URLs (unchanged)
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
]

# Dictionary to hold URLs for each media type
media_types = {
    'images': [],
    'videos': []
}

def load_media(url):
    try:
        response = requests.get(url)
        if not response.ok:
            print(f"Error loading media from {url}: {response.status_code}")
            return None, f"Status code: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, "Request failed"
    
    try:
        if url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image = Image.open(io.BytesIO(response.content))
            return image
        elif url.endswith(('.mp4', '.webm')):
            return url  # Return the video URL directly
    except Exception as e:
        print(f"Failed to load media from {url}: {e}")
        return None, f"Loading error: {e}"

def create_columns():
    global media_types
    
    for i in range(len(urls)):
        if urls[i].endswith(('.jpg', '.jpeg', '.png', '.gif')):
            media_types['images'].append(urls[i])
        elif urls[i].endswith(('.mp4', '.webm')):
            media_types['videos'].append(urls[i])

create_columns()

# Create the Gradio interface
demo = gr.Blocks()
grid_columns = 4
grid_rows = -(-math.ceil(len(media_types['images']) / grid_columns))

with demo:
    for i in range(grid_rows):
        with gr.Row():
            for j in range(grid_columns):
                index = i * grid_columns + j
                if index < len(media_types['images']):
                    image_url = media_types['images'][index]
                    try:
                        image = load_media(image_url)
                        if image is not None:
                            gr.Image(value=image, label=f"Image {index+1}")
                    except Exception as e:
                        print(f"Failed to render image at index {index}: {e}")
                elif index - len(media_types['images']) < len(media_types['videos']):
                    video_url = media_types['videos'][index - len(media_types['images'])]
                    gr.Video(value=video_url, label=f"Video {index+1}")

# Launch the app
demo.launch()
