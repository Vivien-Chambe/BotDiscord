import discord

from discord.ext import commands

TOKEN = ''

client = commands.Bot(command_prefix = '.')
client.remove_command('help')


@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(activity=discord.Game(name='Kill Every Human Being'))

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print(author,content)
    await client.process_commands(message)

@client.event
async def on_message_delete(message):
    author = message.author
    content= message.content
    channel = message.channel
    if content[0] != '.':
        await channel.send('C\'est pas bien de supprimer {} :rage:'.format(author))
    else:
        print(content)
    

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong!')

@client.command(pass_context=True)
async def clear(ctx, amount):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit = int(amount)):
        messages.append(message)
    await channel.delete_messages(messages)
    await channel.send("{} messages supprimés".format(amount))

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    channel = ctx.message.channel
    embed = discord.Embed(
        colour = discord.Color.purple()
    )

    embed.set_author(name = 'Help')
    embed.add_field(name = ".ping", value = 'Renvoie Pong!', inline=False)
    embed.add_field(name = ".clear <nombre>", value = 'Supprime <nombre> messages du salon', inline=False)
    embed.add_field(name = ".trash", value = 'Envoie une insulte random', inline=False)
    embed.add_field(name = ".compliment", value = 'Envoie une insulte random', inline=False)

    await author.send(embed=embed)

    messages = []
    async for message in channel.history(limit = 1):
        messages.append(message)
    await channel.delete_messages(messages)




client.run(TOKEN)
