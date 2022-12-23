from webserver import keep_alive
import os
import discord
import disnake
import datetime
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="/",
                   help_command=None,
                   intents=discord.Intents.all())


@bot.event
async def on_ready():
  print(f"Bot {bot.user} is ready to work!")


@bot.event
async def on_member_join(member):
  channel = member.guild.system_channel
  role = discord.utils.get(member.guild.roles, name='Locura')
  embed = disnake.Embed(
    colour=0xffffff,
    title="**Новый участник!**",
    description=f"{member.mention}\n Welcome to our server!",
    timestamp=datetime.datetime.utcnow())

  embed.set_thumbnail(url=f"{member.avatar.url}")
  await channel.send(embed=embed)
  await member.add_roles(role)


@bot.event
async def on_command_error(ctx, error):
  print(error)

  if isinstance(error, commands.MissingPermissions):
    await ctx.send(
      f"{ctx.author}, у вас недостаточно прав для выполнения данной команды! ")
  elif isinstance(error, commands.UserInputError):
    await ctx.send(embed=disnake.Embed(
      description=
      f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
    ))


@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason="Нарушение правил."):
  await ctx.send(
    f"Администратор {ctx.author.mention} исключил пользователя {member.mention}",
    delete_after=2)
  await member.kick(reason=reason)
  await ctx.message.delete()


@bot.command()
async def ls_say(ctx, member: discord.Member, *, message):
  embed = discord.Embed(title=message,
                        description=f"From: {ctx.author}",
                        colour=discord.Color.green())

  await member.send(embed=embed)


@bot.command()
async def news(ctx, *, message):
  embed = discord.Embed(title='**News!**',
                        description=message,
                        colour=discord.Colour.random(),
                        timestamp=datetime.datetime.utcnow())

  await ctx.send(embed=embed)



@bot.command()
async def say(ctx, *, message):
  embed = discord.Embed(title=message,
                        description='\u200b',
                        colour=discord.Colour.random(),
                        timestamp=datetime.datetime.utcnow())

  await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: disnake.Member, *, reason="Нарушение правил."):
  await ctx.send(
    f"Администратор {ctx.author.mention} исключил пользователя {member.mention}",
    delete_after=2)
  await member.ban(reason=reason)


@bot.command(pass_context=True)
async def hello(ctx):
  await ctx.send('Hi')


@bot.command()
async def join(ctx):
  global voice
  channel = ctx.message.author.voice.channel
  voice = get(bot.voice_clients, guild=ctx.guild)

  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect()
    await ctx.send(f"Бот присоединился к каналу: {channel}")


@bot.command()
async def leave(ctx):
  channel = ctx.message.author.voice.channel
  voice = get(bot.voice_clients, guild=ctx.guild)

  if voice and voice.is_connected():
    await voice.disconnect()
  else:
    voice = await channel.connect
    await ctx.send(f"Бот отключился от канала: {channel}")


@bot.command()
async def clear(ctx, amount=100):
  await ctx.channel.purge(limit=amount)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def help(ctx):
  emb = disnake.Embed(
    title="Навигация по командам, Используется с префиксом < ? >")

  emb.add_field(name="clear", value='Очистка чата')
  emb.add_field(name="kick",
                value='Удаление участника с сервера',
                inline=False)
  emb.add_field(name="ban",
                value='Ограничение доступа к серверу',
                inline=False)
  emb.add_field(name="time", value='Текущее время')

  await ctx.send(embed=emb)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def time(ctx):
  emb = disnake.Embed(title="Текущее время",
                      description='Вы сможете узнать текущее время',
                      colour=0x2ecc71,
                      url='https://www.timeserver.ru/')

  emb.set_author(name=bot.user.name, )
  emb.set_footer(text='Спасибо за использование нашего бота!')
  emb.set_thumbnail(
    url='https://cdn-icons-png.flaticon.com/512/2838/2838590.png')

  now_date = datetime.datetime.now()

  emb.add_field(name='Time', value='Time : {}'.format(now_date))
  await ctx.send(embed=emb)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def rules_ru(ctx):
  emb = disnake.Embed(title='Правила Сервера', colour=0xFFFFFF)

  emb.add_field(
    name=':loudspeaker:',
    value=
    '**Угрозы расправы в реальной жизни, а также угрозы причинения какого-либо ущерба.**'
  )
  emb.add_field(
    name=":loudspeaker:",
    value=
    "**Оскорбление других Пользователей, в том числе и без использования ненормативной лексики, а также провокации на оскорбление.**",
    inline=False)
  emb.add_field(name=":loudspeaker:",
                value="**Запрещен  нацизм и тому подобные вещи.**",
                inline=False)
  emb.add_field(
    name=":loudspeaker:",
    value=
    "**Вымогательство или попрошайничество во всех возможных проявлениях.**",
    inline=False)
  emb.add_field(
    name=":loudspeaker:",
    value=
    "**Flood, offtop, CAPS, Zalgo, троллинг, препятствие общению, в том числе посредством <реакций> к сообщениям.**",
    inline=False)
  emb.add_field(name=':loudspeaker:',
                value='**За перезаход на сервер бан.**',
                inline=False)
  emb.add_field(
    name=':loudspeaker: ',
    value='**Запрещен Пиар своих Discord Каналов и Youtube Каналов.**',
    inline=False)

  await ctx.send(embed=emb)


keep_alive()

my_secret = os.environ['DISCORD_TOKEN']
bot.run(os.getenv('DISCORD_TOKEN'))

