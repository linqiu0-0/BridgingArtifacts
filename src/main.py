from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '161eG6oAB1G_YMum66AeZzbiRpCwaq5Ic8pF7kSyK-Z8'


def main():
    try:
        # Create service endpoint
        service = build('docs', 'v1', credentials=getCredentials())

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        print('The title of the document is: {}'.format(document.get('title')))


        # Start to build batch requests
        # Format text
        res = service.new_batch_http_request()
        intro = "Here is the link to your video clip: "
        link = "https://www.youtube.com\n"
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': intro + link,
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': len(intro),
                        'endIndex': len(intro) + len(link)
                    },
                    'textStyle': {
                        'link': {
                            'url': 'https://www.youtube.com'
                        }
                    },
                    'fields': 'link'
                }
            },
            {
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': 10
                    },
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_1',
                        'spaceAbove': {
                            'magnitude': 10.0,
                            'unit': 'PT'
                        },
                        'spaceBelow': {
                            'magnitude': 10.0,
                            'unit': 'PT'
                        }
                    },
                    'fields': 'namedStyleType,spaceAbove,spaceBelow'
                }
            },
        ]

        result = service.documents().batchUpdate(
            documentId=DOCUMENT_ID, body={'requests': requests}).execute()
    except HttpError as err:
        print(err)
def getCredentials():
    """Shows basic usage of the Docs API.
       Prints the title of a sample document.
       """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

if __name__ == '__main__':
    main()
# [END docs_quickstart]