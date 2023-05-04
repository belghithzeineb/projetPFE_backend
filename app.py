import os
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, send_file
import fitz
import time

app = Flask(__name__)

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.ERROR)
app.logger.addHandler(handler)

import base64
from flask import Flask, request, send_file
import io


app = Flask(__name__)

@app.route('/print_image', methods=['POST', 'GET'])
def print_image():
  try:
    base64_str = request.json['image']
    image_bytes = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(image_bytes))
    pdf_bytes = io.BytesIO()
    image.save(pdf_bytes, format='PDF')
    pdf_bytes.seek(0)
    return send_file(pdf_bytes, as_attachment=True, attachment_filename='image.pdf', mimetype='application/pdf')
  except Exception as e:
    print(e) 
    return "Error: " + str(e), 500


@app.route("/")
def add_page():
    try:
        # Get the full path to the PDF file
        pdf_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'a.pdf')

        doc = fitz.open(pdf_path)
        app.logger.info(f"{pdf_path} opened successfully with {len(doc)} pages")

        with open('a.json', 'r') as f:
            input_data = json.load(f)

        with open('b.json', 'r') as k:
            data = json.load(k)

        for item in input_data:
            for field in item['ids']:
                # Skip this field if it does not have an 'x' value
                if 'x' not in field:
                    continue
                  
                x = field['x']
                y = field['y']
                z = field['lines']
                print(data[z])

                # Define the color for text fields
                color = (field['color']['r'], field['color']['g'], field['color']['b'])

                page = doc[0]

                if field['visibility'] == 'Oui':  
                    app.logger.info(f"Processing {field['fieldType']} field at ({x}, {y})")

                    if field['fieldType'] == 'image':
                        img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '4.JPG')
                        image_rect = fitz.Rect(x, y, x + 100, y + 100)
                        page.insert_image(image_rect, filename=img_path)

                    elif field['fieldType'] == 'Text':
                        text = f" {data[z]}"
                        font = field['fontFamily'] 
                        size = field['size']
                        page.insert_text((x, y), text, fontname=font, fontsize=size, fill=color)

                    elif field['fieldType'] == 'Check':
                        img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'check1.png')
                        image_rect = fitz.Rect(x, y, x + 100, y + 100)
                        page.insert_image(image_rect, filename=img_path)

                    elif field['fieldType'] == 'Phone':
                        text = f" {data[z][:8]}"
                        font = field['fontFamily'] 
                        size = field['size']
                        page.insert_text((x, y), text, fontname=font, fontsize=size, fill=color)

                    elif field['fieldType'] == 'IBAN':
                        text = f" {data[z][:24]}"
                        font = field['fontFamily'] 
                        size = field['size']
                        page.insert_text((x, y), text, fontname=font, fontsize=size, fill=color)

                    elif field['fieldType'] == 'BIC':
                        text = f" {data[z][:11]}"
                        font = field['fontFamily'] 
                        size = field['size']
                        page.insert_text((x, y), text, fontname=font, fontsize=size, fill=color)

        # Save the modified PDF
        timestamp = int(time.time())
        output_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'modified_{timestamp}.pdf')
        doc.save(output_path)
        app.logger.info(f"{output_path} saved successfully")

        
        return send_file(output_path)

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return "An error occurred while processing your request."

if __name__ == '__main__':
    app.run(debug=True , port=5000, host='0.0.0.0') 