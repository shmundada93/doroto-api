import requests
import base64
import json
import os
import glob
from flask import current_app

redaction_request = {
  "imageData":"",
  "imageType":"image/png",
  "imageRedactionConfigs":[
    {
      "infoType":{
        "name":"PHONE_NUMBER"
      },
      "redactionColor":{
        "blue":0.93,
        "green":0.93,
        "red":0.93
      }
    },
    {
      "infoType":{
        "name":"FIRST_NAME"
      },
      "redactionColor":{
        "blue":0.93,
        "green":0.93,
        "red":0.93
      }
    },
    {
      "infoType":{
        "name":"LAST_NAME"
      },
      "redactionColor":{
        "blue":0.93,
        "green":0.93,
        "red":0.93
      }
    },
    {
      "infoType":{
        "name":"EMAIL_ADDRESS"
      },
      "redactionColor":{
        "blue":0.93,
        "green":0.93,
        "red":0.93
      }
    }
  ],
  "inspectConfig":{
    "excludeInfoTypes": False,
    "infoTypes":[
      {
        "name":"PHONE_NUMBER"
      },
      {
        "name":"FIRST_NAME"
      },
      {
        "name":"LAST_NAME"
      },
      {
        "name":"EMAIL_ADDRESS"
      }
    ],
    "minLikelihood": "POSSIBLE"
  }
}

def convertPDFToImages(folder, filename):
    print("Coverting pdf to images....")
    command = "cd {}; pdf-redact-tools --explode {}".format(folder, filename)
    print(command)
    os.system(command)

def convertImagesToPDF(folder, filename):
    print("Coverting images to pdf....")
    command = "cd {}; pdf-redact-tools --merge {}".format(folder, filename)
    print(command)
    os.system(command)

def redactImage(filepath):
    with open(filepath, "rb") as image_file:
        b_encoded_string = base64.b64encode(image_file.read())
        encoded_string = b_encoded_string.decode('ascii')
    redaction_request["imageData"] = encoded_string
    r = requests.post("https://dlp.googleapis.com/v2beta2/projects/solid-future-198322/image:redact?key={}".format(current_app.config['GOOGLE_CLOUD_KEY']), data=json.dumps(redaction_request))
    response = r.json()
    print(r.status_code)
    redacted_string = response['redactedImage']
    with open(filepath, "wb") as fh:
        fh.write(base64.b64decode(redacted_string))

def redactPDF(filename):
    folder = current_app.config['UPLOAD_FOLDER']
    extension = '.pdf'
    print("Exploding PDF to images..")
    convertPDFToImages(folder, filename + extension)
    images_list = glob.glob("{}{}_pages/*.png".format(folder, filename))
    print("PDF exploded in {} images".format(str(len(images_list))))
    for image in images_list:
        print("Redacting image: " + image)
        redactImage(image)
    print("Combining images back to PDF..")
    convertImagesToPDF(folder, filename + extension)
    print("Redaction complete..")