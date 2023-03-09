from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

def create_image(csv_file, red_field, green_field, blue_field):
    
    data = pd.read_csv(csv_file, usecols=[red_field, green_field, blue_field])

    # Read the CSV file into a NumPy array
    data_array = np.array(data)
    
    # Normalize the data to be between 0 and 255
    data_array = (data_array - data_array.min()) * 255 / (data_array.max() - data_array.min())

    # Convert the data to uint8 format
    data_array = data_array.astype(np.uint8)

    # Reshape the data array into an image  
    image = data_array.reshape(-1, 1, 3)

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB);
    # print(img)
    # Return the image
    return img

@app.route('/home', methods=['POST',"GET"])
def handle_create_image():
    if request.method == 'POST':
        # Get the CSV file and field names from the request
        csv_file = request.files['csv_file']
        red_field = request.form['red_field']
        green_field = request.form['green_field']
        blue_field = request.form['blue_field']

        # print(csv_file)
        # print(red_field)
        # print(green_field)
        # print(blue_field)
        # Call the create_image function
        image = create_image(csv_file, red_field, green_field, blue_field)
        img_resize = cv2.resize(image,(500,500))


        # Add path where you want to create saveimage.jpg in path variable
        path = r'C:\Users\Sankalp\OneDrive\Desktop\gsoc_2023\code_challenge_attempt2\static\Images'
        cv2.imwrite(os.path.join(path , 'saveimage.jpg'), img_resize)

    return render_template("index.html")


app.run(port=5000)
