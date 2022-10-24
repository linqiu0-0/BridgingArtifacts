# Connected Conversation Zoom App

Server.py builds a simple server which can responds to the get and post request.
To run the sever, first install all dependencies in requirements.txt.
You can launch server by running `flask --app server --debug run`
### Google Doc APIs part: Get title of a document and change document content
To test the Doc update feature, in the doc_update file:
1. Update doc_id to **Your_DOCUMENT_ID**.
2. Update **credentials.json** data in resources/credentials.json.
3. Regenerate token.json if necessary