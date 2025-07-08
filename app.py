import gradio as gr
from PIL import Image
import requests
import io

# Define the URLs
urls = [
    "https://sosrff.tsu.ru/new/shm.jpg",  # Resonance
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
    grid_columns = 2
    grid_rows = -(-3 // grid_columns)  # Calculate the number of rows needed
    
    grid = []
    
    for i in range(grid_rows):
        row = []
        
        for j in range(grid_columns):
            if i < len(urls) and (j == 0 or j == grid_columns - 1):  # Check if this is the first column
                url_index = i * grid_columns + j
                if url_index >= len(urls):
                    break
                
                image = load_media(urls[url_index])
                
                if image:
                    row.append(gr.Image(image))
            elif j != 0:  # Add a video or another image to this row
                for k in range(3):  # Up to three videos per row
                    url = urls[i * grid_columns + j]
                    
                    if url.endswith('.mp4') or url.endswith('.webm'):  # Check the URL type
                        row.append(gr.Video(url))
                    else:
                        image = load_media(url)
                        
                        if image:
                            row.append(gr.Image(image))
        
        grid.append(gr.Row(*row))  # Add each row to the grid

demo.launch()
