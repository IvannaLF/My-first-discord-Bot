# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random
import time
from Generador import * #El * significa Todo
from Lanzarmoneda import throw_coin

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents, help_command = None)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def password(ctx, lon:int = 8): #Si no se escribe nada sera 8
    await ctx.send("Your new password is...")
    await ctx.send(gen_pass(lon))


@bot.command()
async def coin(ctx, lon:int = 1):
    for i in range(lon):
        await ctx.send("The coin turned out to be:")
        await ctx.send(throw_coin())



@bot.command()
async def help(ctx):
    await ctx.send("Add a '?' sign before all the commands:")
    time.sleep(1)
    await ctx.send("add --> Adds two numbers together, add the two numbers after the command")
    await ctx.send("password --> Creates a password, add the number of characters after the command")
    await ctx.send("coin --> Flip a coin, you can add the number of times it would flip the coin")
    await ctx.send("roll --> Rolls a dice, add first the number of dices and then the faces the dice has")
    await ctx.send("choose --> Chooses between multiple choices, add the choices after the command")
    await ctx.send("repeat --> Repeats a message several times, add the times you want the message to be repeated")
    await ctx.send("joined --> Says when a member joins")
    await ctx.send("cool --> Says if a user is cool")
    await ctx.send("_bot --> Asks and says if the bot is cool, add ?cool bot, to initialize")
    await ctx.send("help --> Makes a list of all the commands")


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


bot.run('TOKEN')
