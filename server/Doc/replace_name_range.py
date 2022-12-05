
TEST_DOC_ID = '161eG6oAB1G_YMum66AeZzbiRpCwaq5Ic8pF7kSyK-Z8'

from googleapiclient.discovery import build
from Doc.doc_update import get_credentials


def replace_named_range(range_name, new_text, document_id = TEST_DOC_ID):
    service = build('docs', 'v1', credentials=get_credentials())
    # preprocess the new text
    if new_text[len(new_text ) -1] != "\n" :
        new_text += "\n"


    """Replaces the text in existing named ranges."""

    # Determine the length of the replacement text, as UTF-16 code units.
    # https://developers.google.com/docs/api/concepts/structure#start_and_end_index
    new_text_len = len(new_text.encode('utf-16-le')) / 2

    # Fetch the document to determine the current indexes of the named ranges.
    document = service.documents().get(documentId=document_id).execute()

    # Find the matching named ranges.
    named_range_list = document.get('namedRanges', {}).get(range_name)
    if not named_range_list:
        raise Exception('The named range is no longer present in the document.')

    # Determine all the ranges of text to be removed, and at which indices the
    # replacement text should be inserted.
    all_ranges = []
    insert_at = {}
    for named_range in named_range_list.get('namedRanges'):
        ranges = named_range.get('ranges')
        all_ranges.extend(ranges)
        # Most named ranges only contain one range of text, but it's possible
        # for it to be split into multiple ranges by user edits in the document.
        # The replacement text should only be inserted at the start of the first
        # range.
        insert_at[ranges[0].get('startIndex')] = True

    # Sort the list of ranges by startIndex, in descending order.
    all_ranges.sort(key=lambda r: r.get('startIndex'), reverse=True)

    # Create a sequence of requests for each range.
    requests = []

    # only update the most recent one
    r =  all_ranges[len(all_ranges) - 1]
    # Delete all the content in the existing range.
    requests.append({
        'deleteContentRange': {
            'range': r
        }
    })

    segment_id = r.get('segmentId')
    start = r.get('startIndex')
    if insert_at[start]:
        # Insert the replacement text.
        requests.append({
            'insertText': {
                'location': {
                    'segmentId': segment_id,
                    'index': start
                },
                'text': new_text
            }
        })

        placeholder = "[next update will be added here]"

        requests.append({'insertText': {
                'location': {
                    'segmentId': segment_id,
                    'index': start + new_text_len
                },
                'text': placeholder
            }})

        # Re-create the named range on the placeholder
        requests.append({
            'createNamedRange': {
                'name': range_name,
                'range': {
                    'segmentId': segment_id,
                    'startIndex': start + new_text_len,
                    'endIndex': start + new_text_len + len(placeholder)
                }
            }
        })

    # Make a batchUpdate request to apply the changes, ensuring the document
    # hasn't changed since we fetched it.
    body = {
        'requests': requests,
        'writeControl': {
            'requiredRevisionId': document.get('revisionId')
        }
    }
    service.documents().batchUpdate(documentId=document_id, body=body).execute()

def delete_name_range (range_name, document_id = TEST_DOC_ID):
    service = build('docs', 'v1', credentials=get_credentials())


    # Determine the length of the replacement text, as UTF-16 code units.
    # https://developers.google.com/docs/api/concepts/structure#start_and_end_index

    # Fetch the document to determine the current indexes of the named ranges.
    document = service.documents().get(documentId=document_id).execute()

    # Find the matching named ranges.
    named_range_list = document.get('namedRanges', {}).get(range_name)
    if not named_range_list:
        return
        # raise Exception('The named range is no longer present in the document.')

    # Determine all the ranges of text to be removed, and at which indices the
    # replacement text should be inserted.
    all_ranges = []
    insert_at = {}
    for named_range in named_range_list.get('namedRanges'):
        ranges = named_range.get('ranges')
        all_ranges.extend(ranges)
        # Most named ranges only contain one range of text, but it's possible
        # for it to be split into multiple ranges by user edits in the document.
        # The replacement text should only be inserted at the start of the first
        # range.
        insert_at[ranges[0].get('startIndex')] = True

    # Sort the list of ranges by startIndex, in descending order.
    all_ranges.sort(key=lambda r: r.get('startIndex'), reverse=True)

    # Create a sequence of requests for each range.
    requests = []

    # only update the most recent one
    r =  all_ranges[len(all_ranges) - 1]
    # Delete all the content in the existing range.
    requests.append({
        'deleteContentRange': {
            'range': r
        }
    })

    # Make a batchUpdate request to apply the changes, ensuring the document
    # hasn't changed since we fetched it.
    body = {
        'requests': requests,
        'writeControl': {
            'requiredRevisionId': document.get('revisionId')
        }
    }
    service.documents().batchUpdate(documentId=document_id, body=body).execute()




if __name__ == '__main__':
    replace_named_range( TEST_DOC_ID, "pre_name_range", "meeting update 1")

    # Retrieve the documents contents from the Docs service.
    # service = build('docs', 'v1', credentials=get_credentials())
    # document = service.documents().get(documentId=TEST_DOC_ID).execute()
    # print('The title of the document is: {}'.format(document.get('title')))
    # doc_content = document.get('body').get('content')
    # print(doc_content)