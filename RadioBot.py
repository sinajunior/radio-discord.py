import asyncio
import discord
from discord import FFmpegPCMAudio
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot
import nacl
from discord import Color, Embed, Interaction, app_commands, ButtonStyle

intents = discord.Intents.all()

token = ""
prefix = "!"

streams = [
    {"name": "RadioJavan", "link": "http://stream.radiojavan.com/radiojavan"},
    {"name": "Nightride.fm", "link": "https://stream.nightride.fm/nightride.m4a"},
    {"name": "Synthwave.hu", "link": "https://ecast.myautodj.com/public1channel"},
    {"name": "Laut.fm", "link": "https://nightdrive.stream.laut.fm/nightdrive"},
    {"name": "I love Radio", "link": "https://streams.ilovemusic.de/iloveradio10.mp3"},
    {"name": "MonsterCat Radio", "link": "https://streams.ilovemusic.de/iloveradio24.mp3"},
    {"name": "Chill and Lofi House", "link": "https://streams.ilovemusic.de/iloveradio17.mp3"},
    {"name": "MainStage Madness", "link": "https://streams.ilovemusic.de/iloveradio22.mp3"},
    {"name": "Mashup Radio", "link": "https://streams.ilovemusic.de/iloveradio5.mp3"},
    {"name": "The Hard Club", "link": "https://streams.ilovemusic.de/iloveradio20.mp3"},
    {"name": "The Floor Radio", "link": "https://streams.ilovemusic.de/iloveradio14.mp3"},
    {"name": "New Pop", "link": "https://streams.ilovemusic.de/iloveradio11.mp3"},
    {"name": "The Sun and Beach", "link": "https://streams.ilovemusic.de/iloveradio15.mp3"},
    {"name": "X-Mas", "link": "https://streams.ilovemusic.de/iloveradio8.mp3"}

]

bot = commands.Bot(command_prefix = prefix, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    activity = discord.Game(name=f"Nothing", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("bot ready")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command")
    except Exception as e:
        print(e)

@bot.tree.command(name="ping", description="bot ping")
async def ping(interaction : discord.Interaction):
    await interaction.response.send_message(f"Pong! `{round(bot.latency * 1000)} ms`")
async def play_stream(interaction: discord.Interaction, msg : discord.Message):
    guild = interaction.guild
    global player

    if interaction.user.voice is None or interaction.user.voice.channel is None:
        await interaction.response.send_message("Connect to a Voice Channel to start the radio")
        return

    channel = interaction.user.voice.channel
    player = await channel.connect()
    if player.is_playing():
        player.stop()
    player.play(
        FFmpegPCMAudio(
            streams[(int(msg.content) - 1) if type(msg) != int else (msg - 1)]["link"]
        )
    )
    await interaction.response.send_message(
        f"Playing the Radio - **`{streams[(int(msg.content) -1) if type(msg) != int else (msg - 1)]['name']}`**"
    )

@bot.tree.command(name="rplay")
async def rplay(interacton : discord.Interaction, channel: int = 0):
    Guild = interacton.guild
    if not Guild.voice_channels:
        await interacton.response.send_message("Connect to a Voice Channel to start the radio")
        return  
    if channel > 4: 
        return
    if channel != 0:
        await play_stream(interacton, channel)
        return
    radio_channel_prompt = f"""
    `📻 | Radio Discord`
   Select a radio channel -
> 1. **`Radiorecord.ru`**
> 2. **`Nightride.fm`**
> 3. **`Synthwave.hu`**
> 4. **`Laut.fm`**
> 5. **`IloveRadio`**
> 6. **`MonsterCat Radio`**
> 7. **`Chill and Lofi House`**
> 8. **`MainStage Madness`**
> 9. **`Mashup Radio`**
> 10. **`The Hard Club`**
> 11. **`The Floor Radio`**
> 12. **`New Pop`**
> 13. **`The Sun and Beach`**
> 14. **`X-Mas`**
    """
    await interacton.response.send_message(radio_channel_prompt)
    def check(msg : discord.Message):
        return (
            msg.author == interacton.user
            and msg.channel == interacton.channel
            and msg.content.isnumeric()
            and int(msg.content) in [i + 1 for i in range(len(streams))]
        )
    msg = 0
    try:
        msg = await bot.wait_for("message", check=check, timeout=20)
    except asyncio.TimeoutError:
        await interacton.response.send_message("Sorry you didn't answer in time :C")
        return
    try:
        await play_stream(interacton, msg)
    except Exception as e:
        print(f"[ERROR]: {e}")

@bot.tree.command(name="stop", description="Stop Radio")
async def rstop(interation : discord.Interaction):
    global player
    Guild = interation.guild
    if Guild.voice_channels is None:
        await interation.response.send_message("Connect to a Voice Channel to start the radio")
        return 
    else:
        player.stop()
        await interation.response.send_message("Radio disconnected and paused correctly")
        await interation.guild.voice_client.disconnect(force=True)

@bot.tree.command()
async def help_1(interaction : discord.Interaction):
    imageURL = "https://i.imgur.com/w5XnsL3.png"
    embed=Embed(title="Help Command", description="Hey im a Radio for Discord", color=0x3194bf)
    embed.set_image(url=imageURL)
    embed.add_field(name="rplay", value="Starts the Radio in a Voice Channel", inline=False)
    embed.add_field(name="rstop", value="Stop and Disconnect the Radio from Voice Channel", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(token)