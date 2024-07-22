# Discord Bots

This repository contains the source code for two distinct Discord bots: the Rerun bot and the Transcription bot. Each bot serves a unique purpose, catering to different needs within a Discord server.

## Rerun Bot

The Rerun bot is designed to trigger a webhook, which in turn reruns a specific Jenkins job.

### Features

- **Webhook Trigger**: By using a slash command, users can trigger a webhook that reruns a Jenkins job.
- **Error Handling**: The bot provides feedback on the success or failure of the webhook call.

### Setup

1. Ensure you have Python installed.
2. Set the `WEBRELAY_WEBHOOK_URL` in `rerun1Point.py` to your webhook URL.
3. Set the `BOT_TOKEN` in `rerun1Point.py` to your Discord bot token.
4. Run the bot using `python rerun1Point.py`.

### Usage

- Use the `/rerun1point` slash command in Discord to trigger the Jenkins job rerun.

## Transcription Bot

The Transcription bot listens for voice file attachments in messages. When it detects an audio file or audio message, it downloads the file, optionally splits it if it exceeds a certain size, and then sends each segment to OpenAI whisper api for transcription. The transcribed text is then sent back to the channel.

### Setup for transcription bot

1. Set the `BOT_TOKEN` in `transcription.py` to your Discord bot token.
2. Set the `OPENAI_API_KEY` in the environment variables.
3. Run the bot using `python transcription.py`.

### Usage for transcribing bot

- Attach an audio file to a message in any channel where the bot is present. The bot will automatically process and transcribe the audio, sending the transcription back to the channel.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
