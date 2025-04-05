# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random
import time
import os
import requests

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
async def suma(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def memescontaminacion(ctx):
    meme = random.choice(os.listdir("Memes")) #Choose a random meme from Memes Animales
    with open(f"Memes/{meme}", "rb") as f: #It opens Memes Animales and shows the meme that the function meme has chose
        picture = discord.File(f) #picture is equal to the discord file of meme
    await ctx.send(file=picture) #sends the variable picture


@bot.command()
async def datos(ctx):
    lista = ["La contaminación mata nueve millones de personas al año, el doble que el COVID-19", 
             "La extracción y el procesamiento de los materiales, los combustibles y la comida son responsables de la mitad de las emisiones de gases de efecto invernadero mundiales totales y de más del 90 % de la pérdida de biodiversidad y el estrés hídrico.", 
             "Cada año, 8 millones de toneladas de plástico al año acaba en los océanos",
             "Si bien algunos de los residuos que acaban en el mar provienen de buques y demás transportes de navegación, el 80% de toda la contaminación proviene de actividades realizadas en tierra",
             "Cada 8 segundos muere 1 niño por causas relacionadas con el consumo de agua contaminada y, según las estadísticas, 3400 millones de personas en el mundo entero mueren cada año por afecciones relacionadas con el agua contaminada",
             "Unos 1,5 millones de aves, peces, ballenas y tortugas mueren al año por desechos plásticos en el mar",
             "La contaminación del aire puede provocar enfermedades respiratorias como asma, bronquitis crónica y enfermedad pulmonar obstructiva crónica",
             "La contaminación del aire causa aproximadamente 7 millones de muertes prematuras al año, según la Organización Mundial de la Salud",
             "La contaminación del suelo es un problema que afecta a la calidad de los alimentos que comemos. Los productos químicos tóxicos que se encuentran en el suelo pueden ser absorbidos por las plantas y, posteriormente, por los seres humanos que las consumen",
             "La contaminación del aire también tiene un impacto en el medio ambiente. Puede dañar la capa de ozono, causar lluvia ácida y contribuir al cambio climático",
            ]
    await ctx.send("Sabias que:")
    await ctx.send(random.choice(lista))

def get_duck_image_url():   
    url = 'https://random-d.uk/api/random' #Lleva a un lugar con imagenes de pato aleatorias
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck') #Manda imagenes aleatorias de patos
async def pato(ctx):
    '''Una vez que llamamos al comando duck, 
    el programa llama a la función get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)


def get_random_pokemon_image():
    random_id = random.randint(1, 1025)  # There are 1025 Pokémon in the API
    url = f"https://pokeapi.co/api/v2/pokemon/{random_id}" #Adds to the link the pokemon number we would get
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json() #Gives the image of the pokemon
        name = data["name"] #Gives the name of the pokemon
        image_url = data["sprites"]["front_default"] #Pokemon sprite URL
        return name, image_url
    else:
        return None, None

@bot.command()
async def pokemon(ctx):
    """Sends a random Pokémon image when the user types ?pokemon"""
    name, image_url = get_random_pokemon_image()
    if name and image_url:
        await ctx.send(f"El nombre del pokemon es: **{name}**")
        await ctx.send(image_url)
    else:
        await ctx.send("Oops! Algo salio mal, intenta de nuevo")


@bot.command()
async def help(ctx):
    await ctx.send("Agrega un signo de '?' antes de cualquier comando:")
    time.sleep(1)
    await ctx.send("suma --> Suma dos numeros juntos, agrega los dos numeros luego de escribir el comando")
    await ctx.send("tira --> Tira un dado, primero escribe el numero de dados, luego 'd' y el numero de caras que los dados tienen")
    await ctx.send("escoge --> Escoge algo entre varias opciones, agrega las opciones despues del comando")
    await ctx.send("repite --> Repite un mensage muchas veces, agrega las veces que quieres que el mensage sea repetido")
    await ctx.send("joined --> Dice si se une un usuario")
    await ctx.send("cool --> Dice si un usuario es cool")
    await ctx.send("_bot --> Pregunta y dice si el bot es cool, escribe ?cool bot para inicializar")
    await ctx.send("meme --> Muestra un meme")
    await ctx.send("MemeContaminacion --> Muestra memes sobre la contaminacion")
    await ctx.send("Datos --> Muestra un dato curioso sobre la contaminacion")
    await ctx.send("pato --> Envia una imagen random de un pato")
    await ctx.send("help --> Muestra una lista de todos los comandos y lo que hacen")


@bot.command()
async def tira(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def escoge(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repite(ctx, times: int, content='repeating...'):
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
