import argparse
import auth_util


def parse_args(arg_input=None):
    parser = argparse.ArgumentParser(description='Create album, list albums using Google Photos API.')
    parser.add_argument('--secrets', dest='secrets_file', default=CLIENT_SECRETS_JSON, required=False,
                        help='Google API OAuth client secrets file path.')
    parser.add_argument('--create-album', '-c', dest='album_name', required=False,
                        help='Creates album with specified album name.')
    parser.add_argument('--share-album', '-s', dest='share_album_id', required=False,
                        help='Enables sharing for album with specified album id.')
    parser.add_argument('--list-albums', '-l', required=False, action='store_true',
                        help='Retrieves and prints list of albums visible for credentials.')
    parser.add_argument('--create-shareable', '-cs', required=False, action='store_true',
                        help='Enable sharing after album is created.')

    return parser.parse_args(arg_input)


CLIENT_SECRETS_JSON = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']


def main():
    args = parse_args()

    service = auth_util.get_authenticated_service(args.secrets_file, 'photoslibrary', 'v1', SCOPES)
    if args.album_name:
        # album_title = 'title ' + str(datetime.datetime.now())
        album = create_album(service, args.album_name, args.create_shareable)
        print('created album', album)
    elif args.list_albums:
        albums = list_albums(service)
        print_albums(albums)
    elif args.share_album_id:
        share_response = share_album(service, args.share_album_id)
        print('share_response', share_response)
    else:
        print('no action')


def create_album(service, title, create_shareable):
    request_body = {
        'album': {'title': title}
    }
    album = service.albums().create(body=request_body).execute()

    if create_shareable:
        album_id = album.get('id')
        share_response = share_album(service, album_id)
        print('share_response', share_response)

    return album


def share_album(service, album_id):
    request_body = {
        'sharedAlbumOptions': {
            'isCollaborative': False,
            'isCommentable': False
        }
    }
    share_response = service.albums().share(albumId=album_id, body=request_body).execute()
    return share_response
    # album_response = service.albums().get(albumId=album_id).execute()
    # print(album_response)


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
    printable_keys = {'id', 'title', 'isWriteable', 'mediaItemsCount'}
    for album in albums:
        for key in list(album.keys()):
            if key not in printable_keys:
                del album[key]
        print(album)


if __name__ == '__main__':
    main()
