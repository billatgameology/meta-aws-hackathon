import json
import base64

# Function to read base64 string from a text file and save it as an image
def convert_base64_to_image(input_file, output_file):
    # Read the base64 string from the text file
    with open(input_file, 'r') as file:
        base64_image_data = file.read().strip()

    # Decode the base64 string
    image_bytes = base64.b64decode(base64_image_data)

    # Save the decoded bytes as an image file
    with open(output_file, 'wb') as image_file:
        image_file.write(image_bytes)
    
    print(f"Image saved as '{output_file}'")

if __name__ == '__main__':
    # Specify the input text file containing the base64 string and the output image file
    input_file = 'commands.txt'
    output_file = 'generated_image.png'
    
    # Convert the base64 string to an image
    convert_base64_to_image(input_file, output_file)