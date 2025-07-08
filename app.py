import gradio as gr
import requests
from PIL import Image
from io import BytesIO
import math

# List of URLs for images and videos
urls = [
    "https://sosrff.tsu.ru/new/shm.jpg",
    "https://volcanodiscovery.de/fileadmin/charts/seismic-activity-level.png",
    "https://spaceweather.gfz-potsdam.de/fileadmin/rbm-forecast/Forecast_UTC_E_1_MeV_PA_50_latest_scatter_smooth_short.mp4",
    "https://spaceweather.gfz-de/fileadmin/Aurora-Forecast/aurora_forecast_browser.webm",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0193.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0304.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0131.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_1024_0171.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/Ic_flat_2d.mp4",
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIBC.jpg",
    "https://jsoc1.stanford.edu/data/hmi/movies/latest/M_color_2d.mp4"
]

# Define a dictionary to hold the URLs for each type of media
media_types = {
    'images': [],
    'videos': []
}

def load_media(url):
    """Loads media from a URL."""
    try:
        response = requests.get(url)
        if not response.ok:
            print(f"Error loading media from {url}: {response.status_code}")
            return None, "Failed to retrieve"
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, f"An error occurred with the request: {e}"

    try:
        if url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image = Image.open(io.BytesIO(response.content))
            return image
        elif url.endswith(('.mp4', '.webm')):
            return url  # Return the URL for video
    except Exception as e:
        print(f"Failed to load media from {url}: {e}")
        return None, f"Failed to load media: {e}"

def create_columns():
    global media_types
    
    # Populate images and videos lists
    for i in range(len(urls)):
        if urls[i].endswith(('.jpg', '.jpeg', '.png', '.gif')):
            media_types['images'].append(urls[i])
        elif urls[i].endswith(('.mp4', '.webm')):
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
            response, result = load_media(image_url)
            
            if response:
                row.append(gr.Image(image=response))
        
        elif len(media_types['videos']) > 0:
            video_url = media_types['videos'][i * grid_columns + j]
            row.append(gr.Video(url=video_url))
    
    if len(row) == grid_columns:
        demo.add_row(*row)

# Launch the application
demo.launch()
