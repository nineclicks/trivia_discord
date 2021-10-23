import json
import discord
from trivia_core import TriviaCore

with open('config.json', 'r') as pointer:
    config = json.load(pointer)

trivia = TriviaCore(**config['trivia_core'], platform='discord')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

def format_question(question):
    """
    Format a question dict as returned from TriviaCore
    """

    user = question.get('winning_user')
    if user:
        username = get_display_name(user.get('uid',''))
        line1 = f'Correct: **{question["winning_answer"]}** '
        line1 += f'-- {username} (today: {user["score"]:,} #{user["rank"]})'
    else:
        line1 = f'Answer: **{question["winning_answer"]}**'

    line2 = f'({question["year"]}) **{question["category"]}** '
    line2 += f'for **{question["value"]}**'
    if question['comment']:
        line2 += ' *question["comment"]*'

    line3 = f'> {question["question"]}'

    return f'{line1}\n{line2}\n{line3}'

@trivia.on_correct_answer
def correct_answer(message_payload, _):
    client.loop.create_task(message_payload.add_reaction('\N{THUMBS UP SIGN}'))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    if int(message.channel.id) != int(config['trivia_channel']):
        return

    uid = str(message.author.id)
    text = message.content

    trivia.handle_message(uid, text, message)

@trivia.on_get_display_name
def get_display_name(uid):
    guild = client.guilds[0]
    name = guild.get_member(int(uid)).display_name
    return name

@trivia.on_pre_format
def on_pre_format(message:str):
    return f'```{message}```'

@trivia.on_post_question
def post_question(question):
    print(question)
    channel = client.get_channel(int(config['trivia_channel']))
    if channel is None:
        return
    question_str = format_question(question)
    client.loop.create_task(channel.send(question_str))

@trivia.on_post_message
def post_message(message):
    channel = client.get_channel(int(config['trivia_channel']))
    client.loop.create_task(channel.send(message))

@trivia.on_post_reply
def post_reply(message, message_payload):
    channel = client.get_channel(message_payload.channel.id)
    client.loop.create_task(channel.send(message))

client.run(config['discord_bot_token'])