import asyncio
import os
import signal
import sys

import aiohttp


class Bot:
    def __init__(self, wikimedia_url, slack_url, loop):
        self.wikimedia_url = wikimedia_url
        self.slack_url = slack_url
        self.loop_time = loop
        self.latest = 0

    async def get_events(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.wikimedia_url) as r:
                response = await r.json()

        events = [
            event for event in response['query']['recentchanges']
            if event['rcid'] > self.latest
        ]
        if events:
            self.latest = events[0]['rcid']

        return events[::-1]

    async def send_slack_message(self, message):
        data = {'text': message}

        async with aiohttp.ClientSession() as session:
            async with session.post(self.slack_url, json=data) as r:
                await asyncio.sleep(2)
                await r.text()

    async def run_async(self):
        while True:
            print('Looping...')
            events = await self.get_events()
            for event in events:
                ts = event['timestamp'].replace('T', ' ').replace('Z', '')
                await self.send_slack_message(
                    "**{0}** was edited on **{1}** by {2}".format(
                        event['title'], ts, event['user'],
                    )
                )
                print('Sending message')
            await asyncio.sleep(self.loop_time)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_async())


def signal_handler(_, __):
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    B = Bot(
        os.environ['WMCS_WIKIMEDIA_URL'],
        os.environ['WMCS_SLACK_URL'],
        int(os.getenv('WMCS_LOOP_TIME', '30'))
    )
    B.run()
