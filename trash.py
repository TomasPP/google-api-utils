import os
import pickle
import requests


def test_one_photo():
    # global image_dir, upload_url, token, response, request_body, upload_response
    # step 1: Upload byte data to Google Server
    image_dir = os.path.join(os.getcwd(), 'Images To Upload')
    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
    token = pickle.load(open('token_photoslibrary_v1.pickle', 'rb'))
    headers = {
        'Authorization': 'Bearer ' + token.token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw'
    }
    image_file = os.path.join(image_dir, 'Kuma.jpg')
    headers['X-Goog-Upload-File-Name'] = 'Kuma_The_Corgi.jpg'
    img = open(image_file, 'rb').read()
    response = requests.post(upload_url, data=img, headers=headers)
    request_body = {
        'newMediaItems': [
            {
                'description': 'Kuma the corgi',
                'simpleMediaItem': {
                    'uploadToken': response.content.decode('utf-8')
                }
            }
        ]
    }
    upload_response = service.mediaItems().batchCreate(body=request_body).execute()
