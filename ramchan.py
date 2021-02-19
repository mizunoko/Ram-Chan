import discord
from eyes1 import newscmd
from discord.ext import commands
import json
import asyncio
#--------prefix--------|
prefix='ram '
#--------bot--------|
ram = commands.Bot(command_prefix=prefix)
ram.remove_command('help')
#--------contants & vars--------|
global channels
channels = []
#--------loop--------

async def NewsLoop():
	llist = newscmd.news_links()
	print(llist)
	if llist:
		for i in llist:
			title, content, img_link, news_link= newscmd.news_link_parser(i)
			c=title.count('-')
			if c == 2:
				title, g, l = title.split('-')
			elif c==3:
				title, g, l, k = title.split('-')
			elif c==4:
				title, g, k, l, i = title.split('-')
			emb = discord.Embed(title='Anime • Manga News',color=discord.Color.from_rgb(255,182,193))
			emb.add_field(name=f"-------------------------------------------------------------",value=f"**[{title}:]({news_link})**\n{content}\n**-------------------------------------------------------------**")
			emb.set_footer(text='Source Anime News Network')
			emb.set_thumbnail(url=ram.user.avatar_url)
			emb.set_image(url=img_link)
			with open('channel.json', 'r') as file:
				data=json.load(file)
			for i in data['server']:
				channel = ram.get_channel(int(data['server'][i]))
				await channel.send(embed=emb)
	print('going to sleep for 6 mins')
	await asyncio.sleep(360)
	await NewsLoop()

@ram.event
async def on_ready():
	print('Konnichiwa Nee sama!')
	await ram.change_presence(activity=discord.Game(game))
	await NewsLoop()


@ram.command()
async def help(ctx):
	emb = discord.Embed(
		title='Help Section',
		description=f'''
		This message shows usage of this bot's commands''',
		color=discord.Color.from_rgb(255,182,193))
	emb.set_thumbnail(url=ram.user.avatar_url)
	emb.set_footer(text='Rem ♡ Ram')
	emb.add_field(name='Bot prefix', value=f'`{prefix}`', inline=False)
	emb.add_field(name=f'{prefix}ping', inline=False,value=f'''
		_Shows bot's current ping_
		`Ex:{prefix}ping`''')
	emb.add_field(name=f'{prefix}status', inline=False,value=f'''
		_Changes bot's playing status_
		Type the status after the command
		`Ex:{prefix}status with Rem chan`''')
	emb.add_field(name=f'{prefix}set' ,inline=False ,value=f'''
		_Used to set a channel as posting channel_
		_Available channel type is only_ `newschannel` _for the time being_
		Type the channel type and channel you want the bot to set as posting channel
		`Ex:{prefix}set newschannel #channel`''')

	await ctx.send(embed=emb)

def RemCheck(ctx):
	if ctx.author.id == 689075959072424013 or ctx.author.id == 656543188969848863:
		return True

@ram.command()
async def status(ctx, *, game):
	check = RemCheck(ctx)
	if check:
		if game == 'clear':
			await ctx.message.delete(delay=None)
			await ram.change_presence(status=None)
			msg = await ctx.send(f'Activity removed by <@{ctx.author.id}>')
			await msg.delete(delay=2)
		elif game is None:
			await ctx.send('Mention the status')
		else:
			await ctx.message.delete(delay=None)
			await ram.change_presence(activity=discord.Game(game))
			msg = await ctx.send(f'Activity changed by <@{ctx.author.id}>')
			await msg.delete(delay=2)
	else:
		await ctx.send("You are not Rem chan nor Jenna-sama! ")
		await ctx.send('''https://tenor.com/blITm.gif''')

@ram.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(ram.latency*1000, 1)} ms')

@ram.command()
async def set(ctx, type, channel=None):
	if type == 'newschannel':
		if channel==None or channel[0]!='<':
			await ctx.send('Provide a valid channel for me to post news')
		else:
			grb, id = channel.split('#')
			print(id)
			id, grb = id.split('>')
			id = int(id)
			channel = ram.get_channel(id)
			#--------<json stuff>--------|
			with open('channel.json', 'r') as file:
				data = json.load(file)
			data["server"].update({f"{channel.guild.id}":channel.id})
			with open('channel.json', 'w') as file:
				json.dump(data, file)
			#----------</json stuff>-----|
			await ctx.send(f'News will now be posted in {channel.mention}')
	else:
		await ctx.send('Unknown channel type')


ram.run('token')
