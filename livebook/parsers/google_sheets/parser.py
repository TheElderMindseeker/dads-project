import gspread
import os
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from json import loads
from livebook.parsers import *
from os.path import dirname

# If modifying these scopes, delete the file token.pickle.
scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# The ID and range of the needed spreadsheet.
spreadsheet_id = '1PNWun9wY9cFdBs4FbDcnWPh6FGWnvJ6pNluKc1n0cpo'
# Get credentials from service account file
creds = None
try:
    creds = service_account.Credentials.from_service_account_file(dirname(__file__) + '/livebook_client_credentials.json',
                                                                scopes=scopes)
except FileNotFoundError:
    cred_var = os.environ['GOOGLE_CREDS']
    cred_info = loads(cred_var)
    creds = service_account.Credentials.from_service_account_info(cred_info)

# Create a client for gspread
client = gspread.Client(auth=creds)
# Create a session for it
client.session = AuthorizedSession(creds)
# Get the sheet
sheet = client.open_by_key(spreadsheet_id)
# We'll nearly always need the meta sheet
meta_sheet = sheet.worksheet("livebook_meta")

# TODO: Good idea?
'''
Module variables
'''
stats_end = 1


# TODO: Error-checking. Right now we assume the document is perfectly-done
def read_stats():
    """
    Reads all the stats from the sheet's livebook_meta sheet
    :return: an array of Stats
    """
    stats = []
    column = [""]
    column_val = 1

    while len(column) != 0:
        column = meta_sheet.col_values(column_val)

        if column:
            new_stat = Stat(column[0].strip(), column[1], int(column[2]), column[3:])

            stats.append(new_stat)

        column_val += 1

    global stats_end
    if stats_end == 1:
        stats_end = column_val

    return stats


def read_initial_scenes():
    """
    Reads the names of the initial and all final scenes
    Requires read_stats to happen first
    :return: name of the initial scene, array of final scene names
    """
    info = meta_sheet.col_values(stats_end)

    start = info[0].strip()
    ends = list(map(lambda x: x.strip(), info[1:]))

    return start, ends


def read_scene(scene_name):
    """
    Reads the information on the required scene
    :param scene_name: name of the scene
    :return: Scene object
    """
    worksheet = sheet.worksheet(scene_name)
    row = 2
    options = []
    option = [""]

    text = worksheet.cell(1, 1).value

    while len(option) > 0:
        option = worksheet.row_values(row)

        if len(option) > 0:
            flavor = option[2] if len(option) > 2 else ""
            options.append(Option(option[0], option[1].strip(), flavor))

        row += 1

    scene = Scene(text, options)
    return scene


def get_scene_names():
    return [i.title for i in sheet.worksheets()]


def test_read():
    values = meta_sheet.col_values(1)

    if not values:
        print('No data found.')
    else:
        print(values)
        print('Row:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)


if __name__ == '__main__':
    # test_read()
    print(get_scene_names())
    stats = read_stats()
    for stat in stats:
        print(stat)
    start, ends = read_initial_scenes()
    print(start, ends)
    scene = read_scene("cthulu")
    scene.parse_text(stats)
    print(scene.text)
    for opt in scene.options:
        print(opt)

# TODO: No idea if this is really needed
if client.session is not None:
    client.session.close()
