import configparser
import json
import asyncio
from datetime import date, datetime
import time

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)


# some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
_offset_id=0

async def main():
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, '+905346403281')
        except SessionPasswordNeededError:
            await client.sign_in(password='a09367854752A')

    me = await client.get_me()

    user_input_channel = 'https://t.me/rosecryptochannelpremium'
    # input('enter entity(telegram URL or entity id):')

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset_id = _offset_id
    limit = 10
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    while True:
        # print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        # if not history.messages:
        #     break
        messages = history.messages
        print(messages[0].message)
        for msg in messages:
            if "buy setup" in msg.message.lower():
                print(msg.message)
        # _offset_id =
        time.sleep(10)

        # for message in messages:
        #     all_messages.append(message.to_dict())
        # offset_id = messages[len(messages) - 1].id
        # total_messages = len(all_messages)
        # if total_count_limit != 0 and total_messages >= total_count_limit:
        #     break
    # print(messages[len(messages) - 1])

    # with open('channel_messages.json', 'w') as outfile:
    #     json.dump(all_messages, outfile, cls=DateTimeEncoder)
# def parsMessage(message):
#     if("entry" in message):
with client:
    client.loop.run_until_complete(main())


