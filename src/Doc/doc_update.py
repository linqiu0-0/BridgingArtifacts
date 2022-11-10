from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']
TEST_DOC_ID = '161eG6oAB1G_YMum66AeZzbiRpCwaq5Ic8pF7kSyK-Z8'
def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text





# return a message when successfully update doc content, return error otherwise
# The ID of a sample document: '161eG6oAB1G_YMum66AeZzbiRpCwaq5Ic8pF7kSyK-Z8'
def doc_update(intro: str, link: str = " ", doc_id: str = TEST_DOC_ID) -> str:
    try:
        # Create service endpoint
        service = build('docs', 'v1', credentials=get_credentials())

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=doc_id).execute()
        print('The title of the document is: {}'.format(document.get('title')))
        doc_content = document.get('body').get('content')
        # print(read_structural_elements(doc_content))

        # Start to build batch requests
        # Format text
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': intro + link + "\n",
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': len(intro) + 1,
                        'endIndex': len(intro) + len(link) + 1
                    },
                    'textStyle': {
                        'link': {
                            'url': link
                        }
                    },
                    'fields': 'link'
                }
            },
            {
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': 1
                    },
                    'paragraphStyle': {
                        'namedStyleType': 'NORMAL_TEXT',
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
            {
                "createNamedRange": {
                    'name': 'name_range1',
                    'range': {
                        'segmentId': '',
                        'startIndex': len(intro + link) +1,
                        'endIndex': len(intro + link) +2
                    }
                }
            }
        ]

        result = service.documents().batchUpdate(
            documentId=doc_id, body={'requests': requests}).execute()

        print(result)
        return "successfully updated the doc"
    except HttpError as err:
        print(err)
        return err




def get_credentials():
    """Shows basic usage of the Docs API.
       Prints the title of a sample document.
       """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../resources/token.json'):
        creds = Credentials.from_authorized_user_file('../resources/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../resources/DocsCredentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../resources/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


if __name__ == '__main__':
    service = build('docs', 'v1', credentials=get_credentials())

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=TEST_DOC_ID).execute()
    print('The title of the document is: {}'.format(document.get('title')))
    doc_update("Here are the updates from Slack ", "[link]", TEST_DOC_ID)
    doc_content = document.get('body').get('content')
    print(doc_content)
    print(read_structural_elements(doc_content))
