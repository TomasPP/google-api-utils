import os.path
import pickle
import json
import sys
import argparse

import util
import auth_util

from argparse import ArgumentParser
from google_auth_oauthlib.flow import InstalledAppFlow
# noinspection PyPackageRequirements
from googleapiclient.discovery import build
# noinspection PyPackageRequirements
from google.auth.transport.requests import Request


def parse_args(args):
    arg_parser = ArgumentParser(description='Append lines to Google Doc.')
    arg_parser.add_argument(
        '--secrets', dest='secrets_file', default=CLIENT_SECRETS_JSON, required=False,
        help='Google API OAuth client secrets file path'
    )

    arg_parser.add_argument(
        '--mode', default='append', required=False, choices=['append', 'insert', 'dump'],
        help="'append' - lines at the end of doc. "
             "'insert' - lines at the beginning of file. "
             "'dump' - do nothing just retrieve google doc content and print it to doc.json file."
    )

    arg_parser.add_argument('--infile',
                            default=sys.stdin,
                            required=False,
                            type=argparse.FileType('r'),
                            nargs='?')

    arg_parser.add_argument(
        '--max-lines', default='1000000', type=int, required=False,
        help='max line'
    )

    # arg_parser.add_argument(
    #     '--test-mode',
    #     action='store_true',
    #     help='testing mode'
    # )

    arg_parser.add_argument('document_id', help='Google Doc Id')

    parsed = arg_parser.parse_args(args)
    return parsed


CLIENT_SECRETS_JSON = 'client_secrets.json'
# If modifying these scopes, delete credentials pickle file.
SCOPES = ['https://www.googleapis.com/auth/documents']


def main():
    # https://developers.google.com/docs/api/samples/extract-text#python
    # append and every step repeatable
    # empty file: one-two lines, over max line?
    # append line to file
    # surplus lines to full file
    # clear all file

    args = parse_args(sys.argv[1:])
    document_id = args.document_id
    mode = args.mode
    # mode = 'dump'
    max_lines = args.max_lines
    # test_mode = args.test_mode

    # lines = sys.stdin.read()
    lines = '''Test string1
Test string2
'''
# Test string3
# '''
# Test string4
# Test string6'''
    lines = args.infile.read()
    # print(lines)

    lines = '\n'.join([line.rstrip() for line in lines.splitlines() if line.strip()])  # strip empty lines and last \n
    new_line_count = len(lines.splitlines())
    print('new_line_count', new_line_count)
    util.exit_if_true(len(lines) == 0, 'no input lines in --infile or stdin')

    service = auth_util.get_authenticated_service(args.secrets_file, 'docs', 'v1', SCOPES)

    # Retrieve google doc content
    document = service.documents().get(documentId=document_id).execute()
    util.write_str_to_file('doc.json', json.dumps(document, indent=4))
    # print('The title of the document is: {}'.format(document.get('title')))
    util.exit_if_true(mode == 'dump', 'dump mode tasks finished. quiting script.', prefix='')

    content = document['body']['content']
    current_lines = len(content) - 1  # first element is sectionBreak, discounting it.
    surplus_lines = (current_lines + new_line_count) - max_lines
    clear_all = surplus_lines > current_lines
    surplus_lines = current_lines if clear_all else surplus_lines

    requests = []
    last_index = content[-1]['endIndex'] - 1
    # print('last_index', last_index)
    if mode == 'append':
        index = last_index
        empty_file = index == 1
        lines = '\n' + lines if not clear_all and not empty_file else lines
        lines = lines[:-1] if lines.endswith('\n') else lines
        insert_text_request(requests, index, lines)
        if surplus_lines > 0 and not empty_file:
            delete_end_index = content[surplus_lines]['endIndex']  # - 1
            # print('delete_end_index', delete_end_index)
            delete_text_request(requests, 1, delete_end_index)
    else:  # mode == 'insert':
        if surplus_lines > 0:
            delete_text_request(requests, content[-surplus_lines]['startIndex'], last_index)
        index = 1
        lines = lines + '\n' if not clear_all else lines
        insert_text_request(requests, index, lines)

    print('index', index)

    if len(requests) > 0:
        result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        print('result', result)


def insert_text_request(requests, index, lines):
    requests.append(
        {
            'insertText': {
                'location': {
                    'index': index,
                },
                'text': lines
            }
        }
    )


def delete_text_request(requests, start, end):  # end - 1
    requests.append(
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': start,
                    'endIndex': end,
                }
            }
        }
    )


def get_authenticated_service(secrets_file):
    credentials = None

    # The pickle file stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_pickle_file = os.path.splitext(secrets_file)[0] + '.pickle'
    if os.path.exists(token_pickle_file):
        with open(token_pickle_file, 'rb') as token:
            credentials = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                secrets_file, SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_pickle_file, 'wb') as token:
            pickle.dump(credentials, token)
    service = build('docs', 'v1', credentials=credentials)
    return service


if __name__ == '__main__':
    main()
