import configparser
import json
from datetime import datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest, GetUnreadMentionsRequest)
from telethon.tl.types import (
    PeerChannel
)

# some functions to parse json date
from trade import *


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

    user_input_channel = 'https://t.me/iraninanfreedom'#'https://t.me/rosecryptochannelpremium' #'https://t.me/rosecryptochannelpremium'   #'https://t.me/withIranfromIstanbul'#'https://t.me/IranintlTV' #https://t.me/ManotoTV'
    # input('enter entity(telegram URL or entity id):')

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset_id = 0
    limit = 10
    all_messages = []
    submit_orders_id = []
    total_messages = 0
    total_count_limit = 0
    try:
        while True:
            history = await client(GetHistoryRequest(
                peer=my_channel,
                offset_id=0,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=offset_id,
                hash=0
            ))
            messages = history.messages
            if len(messages) > 0:
                try:
                    for msg in messages:
                        if msg.message == "" or msg.message is None:
                            continue
                        if "buy setup" in str(msg.message).lower():
                            type = "long"
                            symbol = findSymbol(msg.message)
                            print(f'long symbol ={symbol}\n')
                            setMarginMode(symbol,"Isolated")
                            setLeverage(symbol,"Long",LONG_LEVERAGE)
                            setupOrder(type, symbol,LONG_LEVERAGE,ORDER_AMOUNT)
                        elif "short setup" in str(msg.message).lower():
                            type = "short"
                            symbol = findSymbol(msg.message)
                            print(f'short symbol= {symbol}\n')
                            setMarginMode(symbol, "Isolated")
                            setLeverage(symbol, "Short", SHORT_LEVERAGE)
                            setupOrder(type, symbol,SHORT_LEVERAGE,ORDER_AMOUNT)
                    offset_id = messages[0].id
                except Exception:
                    print("mored too loop!!")

                    # my_json = json.loads(result.decode('utf8').replace("'", '"'))
                    # orderid = my_json['data']['orderId']
                    # print(orderid)
                    # time.sleep(5)
                    # print(cancleOrder(symbol,str(orderid)))
            time.sleep(60)
    except Exception:
        print("AKH In Che Errori Bood !!!")


def findSymbol(message):
    start = message.find("#")
    stop = message.find(" ")
    return f'{str(message[start + 1:stop]).upper()}-USDT'


with client:
    client.loop.run_until_complete(main())
