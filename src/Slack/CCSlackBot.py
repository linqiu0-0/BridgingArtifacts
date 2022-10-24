import os
import slack

bot_api_token=os.environ['SLACK_BOT_TOKEN']
client= slack.WebClient(token=bot_api_token)

