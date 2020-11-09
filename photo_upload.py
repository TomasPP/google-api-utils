# Code Adapted from https://learndataanalysis.org/upload-media-items-google-photos-api-and-python-part-4/
# and https://github.com/eshmu/gphotos-upload

import requests
import argparse
import auth_util


def parse_args(arg_input=None):
    parser = argparse.ArgumentParser(description='Upload photos using Google Photos API.')
    parser.add_argument("--secrets", default=CLIENT_SECRETS_JSON, required=False,
                        help="Google API OAuth client secrets file path.")
    parser.add_argument('--album_id', required=False,
                        help='Google Photos Album Id. If specified photos are added to this album.')
    parser.add_argument("--first-in-album", required=False, action="store_true",
                        help="Add each photo at index 0 in album.")
    parser.add_argument('photos', metavar='photo', type=str, nargs='*',
                        help='file names of photos to upload')
    return parser.parse_args(arg_input)


def upload_image(image_path, upload_file_name, token):
    headers = {
        'Authorization': 'Bearer ' + token.token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw',
        'X-Goog-Upload-File-Name': upload_file_name
    }

    img = open(image_path, 'rb').read()
    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
    response = requests.post(upload_url, data=img, headers=headers)
    # print('\nUpload token: {0}'.format(response.content.decode('utf-8')))
    return response


CLIENT_SECRETS_JSON = "client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']


def main():
    args = parse_args()
    print('args', args)

    service, credentials = auth_util.get_authenticated(args.secrets, 'photoslibrary', 'v1', SCOPES)

    for photo_file in args.photos:
        upload_photo(service, credentials, args.album_id, photo_file, first_in_album=args.first_in_album)


def upload_photo(service, credentials, album_id, photo_file, first_in_album):
    upload_tokens = []
    response = upload_image(photo_file, photo_file, credentials)

    upload_tokens.append(response.content.decode())
    new_media_items = [{'simpleMediaItem': {'uploadToken': token}} for token in upload_tokens]
    request_body = {}
    if album_id:
        request_body['albumId'] = album_id
    request_body['newMediaItems'] = new_media_items
    if album_id and first_in_album:
        request_body['albumPosition'] = {'position': 'FIRST_IN_ALBUM'}

    response = service.mediaItems().batchCreate(body=request_body).execute()

    print('response', response)
    # response_str = str(response)
    # print('response', response_str)
    # success = response_str.find("'Success'") != 1
    # return success


if __name__ == '__main__':
    main()
