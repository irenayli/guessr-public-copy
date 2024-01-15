from flask import Flask, render_template, request, redirect, url_for
import os
import random
import folium

app = Flask(__name__)

# Define the bounding box for the University of Michigan campus
UMICH_BOUNDS = [(42.267, -83.752), (42.294, -83.677)]

# Dictionary to store image data (filename, location, coordinates)
# image_data
image_data = {
        'bbb.jpg': {'location': 'Bob and Betty Beyster Building', 'coordinates': (42.2930138, -83.7189469)},
        'cccb.jpg': {'location': 'Central Campus Classroom Building', 'coordinates': (42.2777056, -83.7368626)},
        'hatcher.jpg': {'location': 'Hatcher Graduate Library' , 'coordinates': (42.2763342,-83.7397316)},
        'hutchins.jpg': {'location': 'Hutchins Hall', 'coordinates': (42.2737477, -83.7430444)},
        'imsb.jpg': {'location': 'Intramural Sports Building', 'coordinates': (42.2694672, -83.7471273)},
        'kines.jpg': {'location': 'School of Kinesiology Building', 'coordinates': (42.2780916, -83.7415154)},
        'law.jpg': {'location': 'Law Library', 'coordinates': (42.273756, -83.7416469)},
        'lsabuilding.jpg': {'location': 'LSA Building', 'coordinates': (42.2762537, -83.743819)},
        'ruthven.jpg': {'location': 'Ruthven Building', 'coordinates': (42.2783111, -83.7376407)},
        'union.jpg': {'location': 'Michigan Union', 'coordinates': (42.2755472, -83.74192)}#,
        # 'filename.jpg': {'location': '', 'coordinates': ()},
        # Add more images and locations as needed
}

# Function to import image data from the images folder
def import_image_data(folder_path='static/images'):
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image_path = os.path.join(folder_path, filename)
            image_data[filename] = {'path': image_path}

# Route to display the form for manually adding location and coordinates
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        filename = request.form.get('filename')
        location = request.form.get('location')
        coordinates_str = request.form.get('coordinates')

        if filename and location and coordinates_str:
            coordinates = tuple(map(float, coordinates_str.split(',')))
            image_data[filename]['location'] = location
            image_data[filename]['coordinates'] = coordinates

    return render_template('upload.html')

# load image data: fixed set, so manual for now
# def load_image_data():
    


# Function to get a random image and its data
def get_random_image():
    image_data = {
        'bbb.jpg': {'location': 'Bob and Betty Beyster Building', 'coordinates': (42.2930138, -83.7189469)},
        'cccb.jpg': {'location': 'Central Campus Classroom Building', 'coordinates': (42.2777056, -83.7368626)},
        'hatcher.jpg': {'location': 'Hatcher Graduate Library' , 'coordinates': (42.2763342,-83.7397316)},
        'hutchins.jpg': {'location': 'Hutchins Hall', 'coordinates': (42.2737477, -83.7430444)},
        'imsb.jpg': {'location': 'Intramural Sports Building', 'coordinates': (42.2694672, -83.7471273)},
        'kines.jpg': {'location': 'School of Kinesiology Building', 'coordinates': (42.2780916, -83.7415154)},
        'law.jpg': {'location': 'Law Library', 'coordinates': (42.273756, -83.7416469)},
        'lsabuilding.jpg': {'location': 'LSA Building', 'coordinates': (42.2762537, -83.743819)},
        'ruthven.jpg': {'location': 'Ruthven Building', 'coordinates': (42.2783111, -83.7376407)},
        'union.jpg': {'location': 'Michigan Union', 'coordinates': (42.2755472, -83.74192)}#,
        # 'filename.jpg': {'location': '', 'coordinates': ()},
    }
    image_filename, image_data = random.choice(list(image_data.items()))
    return image_filename, image_data['location'], image_data['coordinates']

# Home route
@app.route('/')
def index():
    # load_image_data()

    image, location, coordinates = get_random_image()

    # Create a map centered on the U-M campus
    umich_map = folium.Map(location=[42.2808, -83.7382], zoom_start=15)
    
    # Add a rectangle representing the U-M campus bounding box
    folium.Rectangle(bounds=UMICH_BOUNDS, color='blue', fill=True, fill_color='blue', fill_opacity=0.2).add_to(umich_map)

    # Save the map as an HTML file
    map_html = os.path.join(app.static_folder, 'umich_map.html')
    umich_map.save(map_html)

    return render_template('index.html', image=image, location=location, coordinates=coordinates, map_html=map_html)

# Check user's guess
@app.route('/guess', methods=['POST'])
def guess():
    user_guess = request.form.get('user_guess')
    _, actual_location, actual_coordinates = get_random_image()

    # Check if the user's guess is close enough to the actual location
    if user_guess and UMICH_BOUNDS[0][0] <= float(user_guess.split(',')[0]) <= UMICH_BOUNDS[1][0] and UMICH_BOUNDS[0][1] <= float(user_guess.split(',')[1]) <= UMICH_BOUNDS[1][1]:
        result = "Correct!"
    else:
        result = f"Wrong! The actual location was within the U-M campus area. Try again."

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
