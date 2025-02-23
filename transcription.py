import discord
import os
import replicate

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.voice_states = True

bot = discord.Client(intents=intents)

TOKEN = 'BOT_TOKEN'
MODEL = (
    "openai/whisper:"
    "8099696689d249cf8b122d833c36ac3f75505c666a395ca40ef26f68e7d3d16e"
)

# Whisper openai api is 0.006/min, but replicate is 0.0006/min


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type.startswith('audio'):
                # Download the voice file
                voice_file = await attachment.to_file()
                file_path = voice_file.filename
                with open(file_path, 'wb') as f:
                    await attachment.save(f)

                # Send file to Replicate Openai Whisper-V3 and get the transcription
                try:
                    transcription = transcribe_voice_file(file_path)

                    if len(transcription) >= 2000:
                        # Write the transcription to a text file
                        text_file_path = file_path.rsplit(
                            '.', 1)[0] + '_transcription.txt'
                        with open(text_file_path, 'w') as text_file:
                            text_file.write(transcription)

                        await message.channel.send(
                            file=discord.File(text_file_path))
                        os.remove(text_file_path)
                    else:
                        await message.channel.send(
                            f'Transcription: {transcription}')
                except Exception as e:
                    await message.channel.send(
                        f'Error during transcription: {e}')


def transcribe_voice_file(file_path):
    audio_file = open(file_path, "rb")
    input = {
        "audio": audio_file
    }
    output = replicate.run(
        MODEL,
        input=input
    )
    os.remove(file_path)
    return output['transcription']


bot.run(TOKEN)
