import discord
from discord.ext import commands , tasks
import asyncio
import datetime
import random
from itertools import cycle


#Prefiksi i Bot-it, case insensitive
bot = commands.Bot(command_prefix="+" , case_insensitive = True , intents = discord.Intents.all())
bot.remove_command("help") #Fshin komanden default 'help'

#Aktiviteti i Bot-it
@bot.event
async def on_ready():
    print("I'm online and ready to go") #Bot is ready and running
    change_act.start()
    #type 1 = twitch  2 = listening   3 = watching      
    #discord.Activity( type = ,name = "")
    return await bot.change_presence(activity = discord.Game(next(games))) #Bot is playing a game
#Lista e lojrave qe po luan Bot-i
games = cycle(["Mining and Crafting", "Simulator Games"])
@tasks.loop(seconds = 1000) #Ndryshon lojen cdo 1000 sec
async def change_act():
    await bot.change_presence(activity = discord.Game(next(games)))


#-------------------------------------------------Komandat----------------------------------------------------
#Tregon te gjitha komandat e tjera
@bot.command()
async def help(ctx):
    help_embed = discord.Embed(title= "Command List", description = "All the available commnands", colour=0x8cd9e3)
    help_embed.set_author(name= "ByteBot")
    help_embed.add_field(name = "Hey", value="DMs you", inline = False)
    help_embed.add_field(name = "Talk", value="Says random stuff", inline = False)
    help_embed.add_field(name = "Dice", value="Throws a die", inline = False)
    help_embed.add_field(name = "RNG", value="Random number between 1 and the given number", inline = False)
    help_embed.add_field(name = "Google", value="Searches in Google the given words", inline = False)
    help_embed.add_field(name = "Clear", value="Deletes latest messages", inline = False)
    help_embed.add_field(name = "Ban", value="Bans a member", inline = False)
    help_embed.add_field(name = "Unban", value="Unbans a member", inline = False)
    help_embed.add_field(name = "Kick", value="Kicks a member", inline = False)
    help_embed.add_field(name = "Help", value="Displays this ", inline = False)
    help_embed.set_footer(text = "Requested")
    await ctx.send(embed = help_embed)

#DM-s perdoruesin e komandes
@bot.command()
async def hey(ctx):
    await ctx.author.send("Hello!")

#Unban-s a member if you give their ID
@bot.command()
async def unban(ctx, userid):
    user = discord.Object(id = userid)
    await ctx.guild.unban(user)
    unban_embed = discord.Embed(title="Member unbanned", colour=0x8cd9e3)
    unban_embed.add_field(name="Jail time is over", value="Now you can come back", inline= False)
    await ctx.send(embed= unban_embed)
    
#Throws a dice
@bot.command()
async def dice(ctx):
    dn = random.randint(1 , 6)
    await ctx.send(f"The die landed on `{dn}`")

#Random Number Generator between 1 and the number you give
@bot.command()
async def rng(ctx, num):
    try :
        rn = random.randint(1 , int(num))
        await ctx.send(f"Your random number is `{rn}`")
    except:
        await ctx.send("You must enter a number after the command")

#Message fshin equal too the number you give
@bot.command()
async def clear(ctx,*,number:int = None):
    if ctx.message.author.guild_permissions.manage_messages: #Checks for permissions
        try:
            if number is None:
                await ctx.send("You must add the number of messages that you want to delete")
            else:
                deleted = await ctx.message.channel.purge(limit = number) 
                await ctx.send(f"`{len(deleted)}` messages deleted by {ctx.message.author.mention} ")
        except :
            await ctx.send("You can't delete messages")
    else:
        await ctx.send("You don't have permissions for this command")

#Kick someone from the server me nje arsye te dhene
@bot.command()
async def kick(ctx,user: discord.Member, * ,reason = None):
    if user.guild_permissions.manage_messages: #Mods cant be kicked
        await ctx.send("You can't kick a mod")
    elif ctx.message.author.guild_permissions.kick_members: #Only the mods can use this command
        if reason is None:
            await ctx.guild.kick(user = user, reason = "none")
            await ctx.send(f"{user} has been kicked by {ctx.message.author.mention}")
        else:
            await ctx.guild.kick(user = user, reason = reason)
            await ctx.send(f"{user} has been kicked because by {ctx.message.author.mention} because {reason}")
    else:
        await ctx.send("You don't have permissions for this command")
    kick_embed = discord.Embed(title="Kicked successfully", colour=0x8cd9e3)
    kick_embed.add_field(name="Kicked ", value=f"{user} has been kicked", inline= False)
    kick_embed.add_field(name="Reason",value=reason,inline=False)
    await ctx.send(embed= kick_embed)

#Ban Someone
@bot.command()
async def ban(ctx,user: discord.Member, * ,reason = None):
    if user.guild_permissions.manage_messages: #Mods cant be banned
        await ctx.send("You can't ban a mod")
    elif ctx.message.author.guild_permissions.ban_members: #Only the mods can use this command
        if reason is None:
            await ctx.guild.ban(user = user, reason = "none")
            await ctx.send(f"{user} has been banned by {ctx.message.author.mention}")
        else:
            await ctx.guild.ban(user = user, reason = reason)
            await ctx.send(f"{user} has been banned by {ctx.message.author.mention} because {reason}")
    else:
        await ctx.send("You don't have permissions for this command")
    ban_embed = discord.Embed(title="Banned successfully", colour=0x8cd9e3)
    ban_embed.add_field(name="Banned ", value=f"{user} has been banned", inline= False)
    ban_embed.add_field(name="Reason",value=reason, inline=False)
    await ctx.send(embed= ban_embed)

#Google search link for the given prompt
@bot.command()
async def google(ctx ,*, aprompt):
    word = aprompt.replace(" ","+")
    await ctx.send(f"https://www.google.com/search?q={word}")



#Bot token from the Auth2
bot.run('') #vendoset token personal i bot-it 
