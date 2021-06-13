import argparse
import gspread


# Google API service account json file
# https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account
CLIENT_SECRETS_JSON = 'client_secrets_sheet.json'


def parse_args(arg_input=None):
    parser = argparse.ArgumentParser(description='Add row to Google Sheet using Google Sheets API.')
    parser.add_argument('--secrets', default=CLIENT_SECRETS_JSON, required=False,
                        help='Google Service Account json file.')
    parser.add_argument('--sheet-id', required=True,
                        help='Google Sheet doc Id. Google Sheet document is visible '
                             'if created by Google API service account '
                             'or owner of the document shares doc with service account email. ')
    parser.add_argument('--worksheet-ind', '-wi', default=0, type=int, required=False,
                        help='Work sheet index. Default value: %(default)s')
    parser.add_argument('--row-data', required=True,
                        help='Comma separated row data.')
    parser.add_argument('--separator', required=False, default=',',
                        help='Row data separator. Default value: %(default)s')

    return parser.parse_args(arg_input)


def main():
    args = parse_args()
    print('args', args)

    gc = gspread.service_account(filename=args.secrets)
    # print(gc)
    sh = gc.open_by_key(args.sheet_id)
    # print(sh)
    worksheet = sh.get_worksheet(args.worksheet_ind)
    values = args.row_data.split(args.separator)
    # worksheet.append_row(('2020.11.10 21:45:04', '24.0', '49.0'))
    worksheet.append_row(values)
    print(worksheet)


if __name__ == '__main__':
    main()
