from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient

# client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
client = WebClient(token='xoxb-14627938628-4255555908278-Bf6yXKpFnJYpPQqg6waoQ5cT')


# the default conversation is Ruotong, Shreya, and Lin's conversation
def sendMessages(channel_id: str = "C047U5E6Q2Y", text: str = "Hello world!"):
    try:
        # Call the conversations.list method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id,
            text=text
            # You could also use a blocks[] array to send richer content
        )
        # Print result, which includes information about the message (like TS)
        print(result)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")



if __name__ == '__main__':
    sendMessages()
