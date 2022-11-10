from Doc.doc_update import get_credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

TEST_DOC_ID = '161eG6oAB1G_YMum66AeZzbiRpCwaq5Ic8pF7kSyK-Z8'
NEXT_MEETING_DATE = 'Nov 17, 2022'
MEETING_NAME = 'Connected Conversation Weekly Meeting'


def insert_text_request(text):
    return {
        'insertText': {
            'location': {
                'index': 1,
            },
            'text': text,
        }
    }


def create_name_range(identifier, name):
    return {
        "createNamedRange": {
            'name': name,
            'range': {
                'segmentId': '',
                'startIndex': 1,
                'endIndex': len(identifier) + 1
            }
        }
    }


# return a message when successfully update doc content, return error otherwise
# The ID of a sample document: '161eG6oAB1G_YMum66AeZzbiRpCwaq5Ic8pF7kSyK-Z8'
def add_meeting_header(meeting_title, meeting_date: str = NEXT_MEETING_DATE, meeting_name: str = MEETING_NAME,
                       doc_id: str = TEST_DOC_ID) -> str:
    try:
        # Create service endpoint
        service = build('docs', 'v1', credentials=get_credentials())
        # Start to build batch requests
        # Format text

        add_bullet_point_request = {
            'createParagraphBullets': {
                'range': {
                    'startIndex': 1,
                    'endIndex': 1
                },
                'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE',
            }
        }



        delete_bullet_request = {
            'deleteParagraphBullets': {
                'range': {
                    'startIndex': 1,
                    'endIndex': 1
                },
            }
        }

        requests = [insert_text_request("\n\n"),{
            'updateParagraphStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': 1
                },
                'paragraphStyle': {
                    'namedStyleType': 'NORMAL_TEXT',
                    'spaceAbove': {
                        'magnitude': 0.0,
                        'unit': 'PT'
                    },
                    'spaceBelow': {
                        'magnitude': 0.0,
                        'unit': 'PT'
                    }
                },
                'fields': 'namedStyleType,spaceAbove,spaceBelow'
            }
        }];

        sections = ["Post Meeting Updates: ", "Action Items: ", "Meeting Notes: ", "Pre-meeting Notes: "]

        for section in sections:
            requests.append(add_bullet_point_request)
            placeholder = "[next update will be added here]"
            if section == "Pre-meeting Notes: ":
                requests.append(insert_text_request(placeholder))
                requests.append(create_name_range(placeholder, "pre_name_range"))

            if section == "Post Meeting Updates: ":
                requests.append(insert_text_request(placeholder))
                requests.append(create_name_range(placeholder, "post_name_range"))

            requests.append(insert_text_request("\n"))
            requests.append(delete_bullet_request)
            requests.append(insert_text_request(section))
            if section != "Pre-meeting Notes: ":
                requests.append(insert_text_request("\n"))
                requests.append(delete_bullet_request)
                requests.append(insert_text_request("\n"))

        requests.append({
            'insertText': {
                'location': {
                    'index': 1,
                },
                # 'text': meeting_date + " | " + meeting_name + "\n",
                'text': meeting_title + "\n",

            }
        })

        requests.append({
            'updateParagraphStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': 1
                },
                'paragraphStyle': {
                    'namedStyleType': 'HEADING_2',
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
        })

        result = service.documents().batchUpdate(
            documentId=doc_id, body={'requests': requests}).execute()

        # print(result)
        return "200"
    except HttpError as err:
        print(err)
        return err


if __name__ == '__main__':
    add_meeting_header(NEXT_MEETING_DATE, MEETING_NAME, TEST_DOC_ID)
