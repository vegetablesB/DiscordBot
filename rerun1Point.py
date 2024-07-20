import interactions
import requests

bot = interactions.Client(
    token="BOT_TOKEN")

# This Bot is to call the webhook forward service
# to trigger the rerun of the 1point Jenkins job


@interactions.slash_command(
    name="rerun1point",
    description="Triggers the rerun webhook"
)
async def rerun(ctx):
    url = 'WEBRELAY_WEBHOOK_URL'

    try:
        response = requests.post(url)
        response.raise_for_status()
        result_message = f'Request was successful: {response.status_code}'
    except requests.exceptions.HTTPError as http_err:
        result_message = f'HTTP error occurred: {http_err}'
    except Exception as err:
        result_message = f'Other error occurred: {err}'

    # Respond in the channel where the command was called
    await ctx.send(result_message)

bot.start()
