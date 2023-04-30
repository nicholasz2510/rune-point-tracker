import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='rp ')

with open("points_data.json") as data_file:
    points_data = json.load(data_file)


@bot.event
async def on_ready():
    print('Logged on as ' + str(bot.user))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That wasn't a valid command!\nType `rp help` to see a list of commands.")
    else:
        raise error


@bot.command()
async def give(ctx, recipient: discord.Member, amount: int = 1):
    register(ctx.message.author.id)
    if not points_data[str(ctx.message.author.id)]["is_rune"]:
        await ctx.send("Hey, you're not Rune! You can't do that!")
        return
    register(recipient.id)
    if ctx.message.author.id == recipient.id:
        await ctx.send("Hmm... giving yourself some points?")
    points_data[str(recipient.id)]["rune_points"] += amount
    _save()
    await ctx.send("Wow! Rune just gave <@" + str(
        recipient.id) + "> " + str(amount) + " Rune Point" + ("" if amount == 1 else "s") + "!")


@give.error
async def give_error(ctx):
    await ctx.send(
        'Make sure you have the recipient and the amount of Rune Points you are giving in the command: `rp give '
        '<recipient> <rune points>`')


@bot.command()
async def remove(ctx, recipient: discord.Member, amount: int = 1):
    register(ctx.message.author.id)
    if not points_data[str(ctx.message.author.id)]["is_rune"]:
        await ctx.send("Hey, you're not Rune! You can't do that!")
        return
    register(recipient.id)
    if ctx.message.author.id == recipient.id:
        await ctx.send("Hmm... removing your own points?")
    points_data[str(recipient.id)]["rune_points"] -= amount
    _save()
    await ctx.send(
        ":( Rune just took away " + str(amount) + " Rune Point" + ("" if amount == 1 else "s") + " from <@" + str(
            recipient.id) + ">!")


@remove.error
async def remove_error(ctx):
    await ctx.send(
        'Make sure you have the recipient and the amount of Rune Points you are removing in the command: `rp remove '
        '<recipient> <rune points>`')


@bot.command()
async def bal(ctx, recipient: discord.Member = None):
    if recipient is None:
        discord_id = ctx.message.author.id
    else:
        discord_id = recipient.id
    register(discord_id)
    who = "They" if recipient else "You"
    await ctx.send(who + " have " + str(
        points_data[str(discord_id)]["rune_points"]) + " Rune Point" + ("" if points_data[str(discord_id)][
                                                                                 "rune_points"] == 1 else "s") + "!")


@bot.command()
async def leaderboard(ctx):
    lb = []
    for user_id in points_data.keys():
        user = await bot.fetch_user(int(user_id))
        if points_data[user_id]["rune_points"] != 0:
            lb.append((user.name + "#" + user.discriminator, points_data[user_id]["rune_points"]))
    lb.sort(key=lambda tup: tup[1], reverse=True)
    lb = lb[:10]
    lb_entries = []
    for i in range(len(lb)):
        lb_entries.append(
            str(i + 1) + ". " + lb[i][0] + " (" + str(lb[i][1]) + " Rune Point" + ("" if lb[i][1] == 1 else "s") + ")")
    await ctx.send("\n".join(lb_entries))


@bot.command()
async def loserboard(ctx):
    lb = []
    for user_id in points_data.keys():
        user = await bot.fetch_user(int(user_id))
        if points_data[user_id]["rune_points"] != 0:
            lb.append((user.name + "#" + user.discriminator, points_data[user_id]["rune_points"]))
    lb.sort(key=lambda tup: tup[1])
    lb = lb[:10]
    lb_entries = []
    for i in range(len(lb)):
        lb_entries.append(
            str(i + 1) + ". " + lb[i][0] + " (" + str(lb[i][1]) + " Rune Point" + ("" if lb[i][1] == 1 else "s") + ")")
    await ctx.send("\n".join(lb_entries))


def register(user_id):
    discord_id = str(user_id)
    if discord_id not in points_data:
        points_data[discord_id] = {}
        points_data[discord_id]["rune_points"] = 0
        points_data[discord_id]["is_rune"] = False
        _save()


def _save():
    with open('points_data.json', 'w+') as file_save:
        json.dump(points_data, file_save)


with open('api_key.txt', 'r') as f:
    bot.run(f.readline())
