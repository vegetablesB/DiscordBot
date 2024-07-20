from openai import OpenAI
import discord
import os
from pydub import AudioSegment

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.voice_states = True

bot = discord.Client(intents=intents)

TOKEN = 'BOT_TOKEN'

client = OpenAI()

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB


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

                # Check the file size
                file_size = os.path.getsize(file_path)
                if file_size > MAX_FILE_SIZE:
                    # Split the file if it exceeds the size limit
                    segments = split_audio_file(file_path)
                else:
                    segments = [file_path]

                # Send each segment to OpenAI and get the transcription
                try:
                    transcriptions = []
                    for segment in segments:
                        transcription = transcribe_voice_file(segment)
                        transcriptions.append(transcription)
                    full_transcription = " ".join(transcriptions)
                    await message.channel.send(
                        f'Transcription: {full_transcription}')
                except Exception as e:
                    await message.channel.send(
                        f'Error during transcription: {e}')

                # Clean up the files
                for segment in segments:
                    os.remove(segment)


def split_audio_file(file_path):
    audio = AudioSegment.from_file(file_path)
    file_size = os.path.getsize(file_path)

    # Calculate the duration for each segment in milliseconds
    segment_duration_ms = (MAX_FILE_SIZE / file_size) * len(audio)

    segments = []

    for i in range(0, len(audio), int(segment_duration_ms)):
        segment = audio[i:i + int(segment_duration_ms)]
        segment_file_path = f"{file_path.rsplit('.', 1)[0]}_segment_{i}.wav"
        segment.export(segment_file_path, format="wav")
        segments.append(segment_file_path)

    return segments


def transcribe_voice_file(file_path):
    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    return transcription


bot.run(TOKEN)
