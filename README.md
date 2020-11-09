Contains command line utils for some Google API. 

```
usage: photo_upload.py [-h] [--secrets SECRETS] [--album_id ALBUM_ID]
                       [--first-in-album]
                       [photo [photo ...]]

Upload photos using Google Photos API.

positional arguments:
  photo                file names of photos to upload

optional arguments:
  -h, --help           show this help message and exit
  --secrets SECRETS    Google API OAuth client secrets file path.
  --album_id ALBUM_ID  Google Photos Album Id. If specified photos are added to this album.
  --first-in-album     Add each photo at index 0 in album. 
``` 
``` 
usage: photo_util.py [-h] [--secrets SECRETS_FILE] [--create-album ALBUM_NAME]
                     [--list-albums]

Create album, list albums using Google Photos API.

optional arguments:
  -h, --help            show this help message and exit
  --secrets SECRETS_FILE
                        Google API OAuth client secrets file path
  --create-album ALBUM_NAME, -c ALBUM_NAME
                        title of album to create
  --list-albums, -l     Retrieves and prints list of albums visible for
                        credentials.
```

```
usage: doc_util.py [-h] [--secrets SECRETS_FILE] [--mode {append,insert,dump}]
                   [--infile [INFILE]] [--max-lines MAX_LINES]
                   document_id

Append lines to Google Doc.

positional arguments:
  document_id           Google Doc Id

optional arguments:
  -h, --help            show this help message and exit
  --secrets SECRETS_FILE
                        Google API OAuth client secrets file path
  --mode {append,insert,dump}
                        'append' - lines at the end of doc. 'insert' - lines
                        at the beginning of file. 'dump' - do nothing just
                        retrieve google doc content and print it to doc.json
                        file.
  --infile [INFILE]
  --max-lines MAX_LINES
                        if doc has more values

```

`subscriptions_filter.py`.

# Installation

Requirements: Python 3.7 or later.

1. Install this application with pip:
    ```bash
    python3 -m pip install --src ~/soft -e git+https://github.com/TomasPP/google-api-utils
   #egg=subscriptions_filter
    ```
2. Create a project through the [Google Cloud Console](https://console.cloud.google.com/).
3. Enable your project to use the YouTube Data API via the [APIs &
   Services Dashboard](https://console.cloud.google.com/apis/dashboard).
4. Create an OAuth Client ID for a native application through the
   [Credentials](https://console.cloud.google.com/apis/credentials) page under APIs &
   Services.
5. Download the OAuth client secrets JSON file from the
   [Credentials](https://console.cloud.google.com/apis/credentials) page and
   rename it to `client_secrets.json`. 
5. Open [your youtube subscriptions page](https://www.youtube.com/feed/subscriptions) 
   and download cookies.txt file using extension 
   [like](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg?hl=en).  

