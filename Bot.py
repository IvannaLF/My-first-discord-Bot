import discord
from Generador import gen_pass #Dice que del nombre del archivo importa la funcion
from Lanzarmoneda import throw_coin #Importa la funcion coin del archivo Lanzar_moneda

# La variable intents almacena los privilegios del bot
intents = discord.Intents.default()
# Activar el privilegio de lectura de mensajes
intents.message_content = True
# Crear un bot en la variable cliente y transferirle los privilegios
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Hemos iniciado sesión como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send("Hi!") #Lanza Hi si el usuario escribe $hello
    elif message.content.startswith('$bye'):
        await message.channel.send("\U0001f642") #Lanza un emoji si el usuario escribe $bye
    elif message.content.startswith('$password'):
        await message.channel.send('Your password is...')
        await message.channel.send(gen_pass(10))
    elif message.content.startswith('$throw a coin'):
        await message.channel.send(throw_coin())
    else:
        await message.channel.send(message.content) #Esto hace que repita lo que mando el usuario

client.run("TOKEN") #Aqui se puso el TOKEN del bot
