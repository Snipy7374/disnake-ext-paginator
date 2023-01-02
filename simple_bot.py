import disnake
from disnake.ext import commands
from disnake_ext_paginator import Paginator

bot = commands.Bot(
    intents=disnake.Intents.all(),
    command_prefix=commands.when_mentioned
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command()
async def test(inter):
    embeds= [
        disnake.Embed(
            title='h'
        ),
        disnake.Embed(
            title='o'
        )
    ]
    paginator = Paginator(timeout=10, page_counter_separator="🍎",on_timeout_message="Lmao", interaction_check_message="Sus")
    await paginator.start(interaction=inter, pages=embeds)

@bot.slash_command()
async def test_kok(inter):
    embeds = [
        disnake.Embed(
            title="h"
        ),
        disnake.Embed(
            title="lmao"
        ),
    ]
    await Paginator(timeout=None).start(interaction=inter, pages=embeds)

@bot.slash_command()
async def lmao(inter):
    await inter.response.send_message(bot.persistent_views)

bot.run('OTc1MzM4NTUwMjg1NDM5MDE2.GQRd6J.0HevEEa8uQTCtj_-y_UNLoYfj9_RNWsi9hrfeM')