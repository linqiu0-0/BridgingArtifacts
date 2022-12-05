# Connected Conversation Zoom App

Server.py builds a simple server which can responds to the get and post request.
To run the sever, first install all dependencies in requirements.txt by running `pip install -r requirements.txt`. It will be easier to maintain the dependencies in the virtual envrionment.[See Useful Commands 1]
You can launch server by running `flask --app server --debug run` in the src directory.

### Useful Commands
1.  `. env/bin/activate` to activate your virtual environment to manage the dependencies for your project
2. Run `ngrok http #number of your localhost port#` to launch the ngrok. For example, `ngrok http 5000`.
3. ngrok with hostname `ngrok http --region=us --hostname=bridgingartifacts.ngrok.io 5000`
### Google Doc APIs: Get title of a document and change document content
To test the Doc update feature, in the doc_update file:
1. Update doc_id to **Your_DOCUMENT_ID**.
2. Update **credentials.json** data in resources/credentials.json.
3. Regenerate token.json if necessary

<!-- ### Send Messages to Slack
### DON"T NEED TO DO IT NOW, EVERYTHING IS HARD CODED NOW
To test send messages to slack feature, you need
1.  In the root directory, run `. env/bin/activate` to activate your virtual environment to manage the dependencies for your project; or whatever commands to activate your virtual environment
2.  Then in the root directory, run `export SLACK_BOT_TOKEN=xoxb-14627938628-4255555908278-Bf6yXKpFnJYpPQqg6waoQ5cT`
 -->

### Docker
1. update requirements.txt when introducing new dependencies `pip freeze >`
2. `docker compose build `
3. `docker compose up`