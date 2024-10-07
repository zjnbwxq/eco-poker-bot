import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from localization import Localization
import traceback
import sys

# 新添加的导入
from game_board import GameBoard

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Game state (simplified for now)
game_in_progress = False
players = []
current_player = 0

# 新添加的全局变量
game_board = None

# Initialize localization
localization = Localization()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='language')
async def set_language(ctx, lang=None):
    if lang is None:
        current_lang = localization.current_language
        await ctx.send(f"Current language is: {current_lang}. Use '!language en' or '!language zh' to change.")
    else:
        response = localization.set_language(lang)
        await ctx.send(response)

# 更新后的 start_game 函数
@bot.command(name='start')
async def start_game(ctx):
    global game_in_progress, players, game_board
    if game_in_progress:
        await ctx.send(localization.get_text('game_in_progress'))
        return
    game_in_progress = True
    players = [ctx.author]
    game_board = GameBoard()
    board_image = game_board.create_board_image()
    await ctx.send(localization.get_text('start_game', ctx.author.name),
                   file=discord.File(board_image, filename="game_board.png"))

@bot.command(name='join')
async def join_game(ctx):
    global players
    if not game_in_progress:
        await ctx.send(localization.get_text('no_game_in_progress'))
        return
    if ctx.author in players:
        await ctx.send(localization.get_text('already_in_game'))
        return
    players.append(ctx.author)
    await ctx.send(localization.get_text('player_joined', ctx.author.name, len(players)))

# 新添加的 show_board 函数
@bot.command(name='board')
async def show_board(ctx):
    global game_board
    if not game_in_progress or game_board is None:
        await ctx.send(localization.get_text('no_game_in_progress'))
        return
    board_image = game_board.create_board_image()
    await ctx.send(file=discord.File(board_image, filename="game_board.png"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Error: Missing required argument. Usage: {ctx.prefix}{ctx.command.name} <argument>")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Error: Unknown command. Use !help to see available commands.")
    else:
        print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# Add more game commands here (draw, play, attack, etc.)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))