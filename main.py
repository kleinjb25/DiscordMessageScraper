"""
Copyright Justin Klein 2024 All Rights Reserved.
This code will parse through a Discord channel and retrieve all of the messages in a specific time frame.
It will then upload all of the messages to a text file to allow for easy attendance tracking.
"""
import json
import os
import requests
from datetime import datetime
from datetime import date
# Used to load the environment variables in .env
from dotenv import load_dotenv
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

def getMessages() :
	file = f"{date.today()}.txt"
	headers = {'authorization': discord_token}
	# If someone deletes the attendance channel accidentally,
	# just make sure you have developer tools enabled in the Discord Settings,
	# then right click the new attendance channel -> copy id and paste it in between "channels/channelID/messages".
	# In this case, 1203908563374706780 is the current channelID.
	req = requests.get(f'https://discord.com/api/v9/channels/1203908563374706780/messages', headers=headers)
	jsonData = json.loads(req.text)
	with open(file, 'a') as file:
		for message in jsonData:
			file.write(message['content'] + "@miamioh.edu\n")
getMessages()