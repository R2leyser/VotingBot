import discord
from datetime import timedelta
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv()


class Entry:
    author = ""
    url = ""

    def toString(self):
        return f'{self.author}: {self.url}'

    def __init__(self, author, url):
        self.author = author
        self.url = url


class MyClient(discord.Client):
    entries = set()
    delta = timedelta(weeks=1)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        buildMessage = ""
        poll = discord.Poll("vote on a best image", self.delta, multiple=True)
        if message.content == "print":
            for entry in self.entries:
                buildMessage += entry.toString() + "\n"
                poll.add_answer(text=entry.author)

            await message.channel.send(buildMessage)
            await message.channel.send(poll=poll)
            return

        print(f'Message from {message.author}: {message.content}')
        async for msg in message.channel.history(limit=500):
            if msg.author.name != self.user.name:
                if len(msg.attachments) != 0:
                    self.entries.add(
                            Entry(msg.author.name, msg.attachments[0].url))
        print("done")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(
    os.getenv("TOKEN")
)
