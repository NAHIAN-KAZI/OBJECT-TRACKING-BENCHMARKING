import json

# Load the input JSON data
input_json_file = 'groundtruth_all.json'  # Path to your input JSON file
output_json_file = 'main_groundtruth.json'  # Path to your output JSON file

# Video resolution
resolution_width = 3840
resolution_height = 2160

# Function to convert percentile values to pixel values
def convert_to_pixels(x, y, width, height):
    x_pixel = (x / 100) * resolution_width
    y_pixel = (y / 100) * resolution_height
    width_pixel = (width / 100) * resolution_width
    height_pixel = (height / 100) * resolution_height
    return x_pixel, y_pixel, width_pixel, height_pixel

# Load the input JSON file
with open(input_json_file, 'r') as f:
    data = json.load(f)

# Iterate through the data and convert the coordinates for each frame
for video in data:
    for box in video['box']:
        for frame_data in box['sequence']:
            # Convert the coordinates from percent to pixels
            x_pixel, y_pixel, width_pixel, height_pixel = convert_to_pixels(
                frame_data['x'], frame_data['y'], frame_data['width'], frame_data['height']
            )
            
            # Update the frame data with the pixel values
            frame_data['x'] = x_pixel
            frame_data['y'] = y_pixel
            frame_data['width'] = width_pixel
            frame_data['height'] = height_pixel

# Save the updated data into a new JSON file
with open(output_json_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Updated JSON file saved to {output_json_file}")
