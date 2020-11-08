import argparse
import auth_util


def parse_args(arg_input=None):
    parser = argparse.ArgumentParser(description='Upload photos to Google Photos.')
    parser.add_argument("--secrets", default=CLIENT_SECRETS_JSON, required=False,
                        help="Google API OAuth secrets file for working with Google docs")
    parser.add_argument('--create-album', required=False,
                        help='title of album to create')
    parser.add_argument("--list-albums", required=False, action="store_true",
                        help="Prints list of albums visible for credentials.")
    return parser.parse_args(arg_input)


CLIENT_SECRETS_JSON = "client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']


def main():
    args = parse_args()
    service = auth_util.get_authenticated_service(CLIENT_SECRETS_JSON, 'photoslibrary', 'v1', SCOPES)
    if args.create_album:
        # album_title = 'title ' + str(datetime.datetime.now())
        album = create_album(service, args.create_album)
        print('created album', album)
    elif args.list_albums:
        albums = list_albums(service)
        print_albums(albums)
    else:
        print('no action')


def create_album(service, title):
    request_body = {
        'album': {'title': title}
    }
    album = service.albums().create(body=request_body).execute()
    return album


def list_albums(service):
    albums = []
    page_token = None
    while True:
        response = service.albums().list(pageToken=page_token).execute()
        albums.extend(response['albums'])
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return albums


def print_albums(albums):
    interesting_keys = {'id', 'title', 'isWriteable', 'mediaItemsCount'}
    for album in albums:
        for key in list(album.keys()):
            if key not in interesting_keys:
                del album[key]
        print(album)


if __name__ == '__main__':
    main()
