"""
Copyright Justin Klein 2024 All Rights Reserved.
This code will parse through a Discord channel and retrieve all of the messages in a specific time frame.
It will then upload all of the messages to a text file to allow for easy attendance tracking.
"""
import json
import os
import pytz
import requests
from datetime import datetime, date, timedelta
# Used to load the environment variables in .env
from dotenv import load_dotenv
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

def getMessages() :
	try:
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
				# Get the time the message was sent and convert it to EST
				currentTimeStamp = datetime.fromisoformat(message.get('timestamp', '')[:-6]).replace(tzinfo=pytz.timezone('GMT')).astimezone(pytz.timezone('US/Eastern'))
				# This checks only for messages within the last 24 hours of running the script.
				# If you try to run the script more than 24 hours after the meeting,
				# it might skip messages sent near the beginning of the meeting.
				if datetime.now(tz=pytz.timezone('US/Eastern')) - currentTimeStamp < timedelta(hours=24) and " " not in message['content']:
					file.write(message['content'] + "@miamioh.edu\n")
	except Exception as e:
		print(e)
		input()
getMessages()