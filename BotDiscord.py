import discord
import random
import os
from dotenv import load_dotenv
from discord.ext import commands
from Lists import *
from time import *

load_dotenv("info.env")

TOKEN = os.environ.get("TOKEN_ID")

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

ban = {}

@client.event
async def on_ready():
    print("Le VivouBot est prêt")
    await client.change_presence(activity=discord.Game(name='type .help'))

@client.event
async def on_message(message):
    channel = message.channel
    if str(message.author.id) in ban: #Si user est banni alors chaque message qu'il envoie est supprimé et il reçoit un dm pour lui rappeler

        messages = []
        async for message in channel.history(limit = 1):
            messages.append(message)
            await channel.delete_messages(messages)
        await message.author.send("Chut tu es ban :shushing_face:")

    if message.author.bot == False and (message.content.startswith("Slt") 
                                        or message.content.startswith("slt") 
                                        or message.content.startswith("Hey") 
                                        or message.content.startswith("hey") 
                                        or message.content.startswith("Yo") 
                                        or message.content.startswith("yo") 
                                        or message.content.startswith("Hello") 
                                        or message.content.startswith("hello") 
                                        or message.content.startswith("Bonjour") 
                                        or message.content.startswith("bonjour") 
                                        or message.content.startswith("Salut") 
                                        or message.content.startswith("salut")
                                        ):
        bonjour_list = bonjour_init()
        bonjour = random.choice(bonjour_list)
        await channel.send(bonjour.format(message.author.mention))
    content = message.content
    await client.process_commands(message)

@client.event
async def on_message_delete(message):
    author = message.author
    content= message.content
    channel = message.channel
    guild = message.guild
    if message.author.bot == False and message.content.startswith(".") == False: # Affiche seulement les messages supprimés par un utilisateur qui ne sont pas des commandes
        print ("Message supprimé par",author)
        print (f"Sur le serveur {guild} dans le channel {channel} : {content}")

@client.event
async def on_command_error(ctx,error):
    if ctx.name == "..":
        return
    else:
        messages = []
        channel = str(ctx.channel)
        if channel[0]!="D" and channel[1]!="i":
            async for message in ctx.channel.history(limit = 1):
                messages.append(message)
            await ctx.channel.delete_messages(messages)
        await ctx.author.send(error)
        await ctx.author.send("Essayez .help pour obtenir la liste des fonctionnalités")
        print("Command not invoked correctly by " + str(ctx.author))
        print(error)

########################
# Commandes Classiques #
########################

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong!')

@client.command(name="test")
async def test(ctx):
    print(ctx.author)

@client.command(pass_context=True)
async def help(ctx, commande='help'):
    author = ctx.message.author
    channel = ctx.message.channel
    if commande=='meme':
        embed = discord.Embed(
        colour = discord.Color.orange()
        )

        embed.set_author(name = 'Help meme')
        embed.add_field(name = "Différentes catégories (en minuscule)", value = 'Alcool\nKaamelott\nStarwars\nSpicy\nGames\nHistory\nInfo\nMetal\nMisc\nScience\nSkyrim', inline=False)
        
        await author.send(embed=embed) 
                    
    
    else:
        embed = discord.Embed(
            colour = discord.Color.purple()
        )

        embed.set_author(name = 'Help')
        embed.add_field(name = ".ping", value = 'Renvoie Pong!', inline=False)
        embed.add_field(name = ".trash", value = 'Envoie une insulte random', inline=False)
        embed.add_field(name = ".compliment", value = 'Envoie un compliment random', inline=False)
        if ctx.guild.id == CONFIFI:
            embed.add_field(name = ".louis [Louis/louis_simulator]", value = 'Invoque Sir Louis', inline=False)
        embed.add_field(name = ".m[eme] <catégorie>", value = 'Poste un meme random de la catégorie choisie (.help meme for categories/leave blank for random meme)', inline=False)
        embed.add_field(name = ".roll[dice] <Number of dices> <Number of faces>", value = "Throws a define amount of dices", inline=False)
        embed.add_field(name = "ADMIN ONLY", value = "No perm no power", inline=True)
        embed.add_field(name = ".clear <nombre>", value = 'Supprime <nombre> messages du salon', inline=False)
        embed.add_field(name = ".s[oft]b[an] <@user> <raison> ", value = 'Empeche l\'utilisateur mentionné d\'écrire dans le chat' , inline=False)
        embed.add_field(name = ".u[n]b[an] <@user>", value = 'Unban l\'utilisateur mentionné', inline=False)
        await author.send(embed=embed)

@client.command()
async def trash(ctx):
    trash_list = trash_init()
    await ctx.send(random.choice(trash_list))

@client.command()
async def compliment(ctx):
    compl_list = compl_init()
    await ctx.send(random.choice(compl_list))

@client.command(pass_context=True)
async def louis(ctx):
    sleep(2)
    louis_list=louis_init()
    channel = ctx.message.channel
    await channel.send(random.choice(louis_list))

@client.command(aliases = ['m'])
async def meme(ctx, category = 'all'):
    categories =['alcool','kaamelott','starwars','games','history','science','info','metal','misc','spicy','skyrim']
    if category == 'all':
        category = random.choice(categories)
    nbr_memes = {'alcool':13,'kaamelott':27,'starwars':2,'games':8,'history':19,'info':11,'metal':22,'science':6,'misc':38,'spicy':46,'skyrim':7}
    channel = ctx.message.channel
    number = random.randint(1,(nbr_memes[category]))
    await channel.send(file=discord.File(f"memes/{category}/{category} ({number}).jpg"))

@client.command(aliases = ['roll'])
async def rolldice(ctx ,nbr, faces):
    nbr= int(nbr)
    faces= int(faces)
    if nbr > 100:
        await ctx.channel.send("Nombre de dés demandé abusé c'est pas la NASA ici")
    else:
        if faces != 2:
            if nbr <= 25:

                embed = discord.Embed(
                    colour = discord.Color.red()
                )
                embed.set_author(name='{} rolled :'.format(ctx.author))
                for i in range (1,nbr+1):
                    result=random.randint(1,faces)
                    embed.add_field(name='Number {}°'.format(i),value = '{}'.format(result))
                await ctx.channel.send(embed=embed)
            else:
                nbr_needed = nbr//25
                nbr_reste = nbr%25
                j = 0
                for i in range (1,nbr_needed+1):
                    embed = discord.Embed(
                        colour = discord.Color.red()
                    )
                    embed.set_author(name='{} rolled :'.format(ctx.author))
                    for i in range (1,25+1):
                        j+=1
                        result=random.randint(1,faces)
                        embed.add_field(name='Number {}°'.format(j),value = '{}'.format(result))
                    await ctx.channel.send(embed=embed)
                if nbr_reste != 0:
                        embed = discord.Embed(
                            colour = discord.Color.red()
                        )
                        embed.set_author(name='{} rolled :'.format(ctx.author))
                        for i in range (1,nbr_reste+1):
                            j+=1
                            result=random.randint(1,faces)
                            embed.add_field(name='Number {}°'.format(j),value = '{}'.format(result))
                        await ctx.channel.send(embed=embed)
        else:
            choice = ["PILE","FACE"]
            if nbr <= 25:

                embed = discord.Embed(
                    colour = discord.Color.red()
                )
                embed.set_author(name='{} flipped a coin :'.format(ctx.author))
                for i in range (1,nbr+1):
                    result=random.randint(0,1)
                    embed.add_field(name='Number {}°'.format(i),value = '{}'.format(choice[result]))
                await ctx.channel.send(embed=embed)
            else:
                nbr_needed = nbr//25
                nbr_reste = nbr%25
                j = 0
                for i in range (1,nbr_needed+1):
                    embed = discord.Embed(
                        colour = discord.Color.red()
                    )
                    embed.set_author(name='{} flipped a coin :'.format(ctx.author))
                    for i in range (1,25+1):
                        j+=1
                        result=random.randint(0,1)
                        embed.add_field(name='Number {}°'.format(j),value = '{}'.format(choice[result]))
                    await ctx.channel.send(embed=embed)
                if nbr_reste != 0:
                        embed = discord.Embed(
                            colour = discord.Color.red()
                        )
                        embed.set_author(name='{} flipped a coin :'.format(ctx.author))
                        for i in range (1,nbr_reste+1):
                            j+=1
                            result=random.randint(0,1)
                            embed.add_field(name='Number {}°'.format(j),value = '{}'.format(choice[result]))
                        await ctx.channel.send(embed=embed)


###################
# Commandes Admin #
###################

@client.command(pass_context=True,  aliases=['delete', 'clean'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit = int(amount)):
        messages.append(message)
    await channel.delete_messages(messages)
    await channel.send("{} messages supprimés".format(amount))

@client.command(pass_context=True, aliases=["sb"])
@commands.has_permissions(administrator=True)
async def softban(ctx,user:str,raison):
    b=user
    user = user.replace("<","") 
    user = user.replace(">","") 
    user = user.replace("@","")
    user = user.replace("!","") 

    messages=[]
    async for message in ctx.channel.history(limit = 1):
        messages.append(message)
    await ctx.channel.delete_messages(messages)

    if user in ban:
        await ctx.send("Utilisateur déjà banni")
    else:
        ban[user]=raison
        await ctx.send("{} banni pour : {}".format(b ,raison))

@client.command(pass_context=True,aliases= ["ub"])
@commands.has_permissions(administrator=True)
async def unban(ctx,user:str):
    b=user
    user = user.replace("<","") 
    user = user.replace(">","") 
    user = user.replace("@","")
    user = user.replace("!","")

    messages=[]
    async for message in ctx.channel.history(limit = 1):
        messages.append(message)
    await ctx.channel.delete_messages(messages)
    
    if user in ban:
        ban.pop(user,"Cet utilisateur n'était pas bani")
        await ctx.send("Re-bienvenu parmi nous")
    else:
        await ctx.send ("Cet utilisateur n'est pas bani")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def banlist(ctx):
    await ctx.author.send(ban)
    messages=[]
    async for message in ctx.channel.history(limit = 1):
        messages.append(message)
    await ctx.channel.delete_messages(messages)


""" @client.command()
async def maj(ctx,nbrmaj,*args):
    user =ctx.message.author
    role = "Admin"
    if role in user.roles:
        channel = ctx.author.channel
        embed = discord.Embed(
            colour = discord.Color.purple()
            )
        embed.set_title(name = 'MAJ')
        embed.add_field(name = "Nouvelle(s) commandes:",value = "Faites .help pour savoir ce qu'elles font", inline=False)
        for nvllecommande in args:
            embed.add_field(name = nvllcommande, inline=False)

        await channel.send(embed = embed) """


client.run(TOKEN)