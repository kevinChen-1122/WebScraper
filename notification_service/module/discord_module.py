import os
import asyncio
import discord
from discord.ext import commands


class Discord:
    def __init__(self, command_prefix="!", intents=discord.Intents.all(), token=""):
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents)
        self.token = token
        self._setup_events()
        self._setup_commands()

    def _setup_events(self):
        """設置機器人的事件處理"""

        @self.bot.event
        async def on_ready():
            print(f"目前登入身份 --> {self.bot.user}")

    def _setup_commands(self):
        """設置機器人的指令處理"""

        @self.bot.command()
        async def load(ctx, extension):
            await self.bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"Loaded {extension} done.")

        @self.bot.command()
        async def unload(ctx, extension):
            await self.bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"UnLoaded {extension} done.")

        @self.bot.command()
        async def reload(ctx, extension):
            await self.bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"ReLoaded {extension} done.")

    async def _load_extensions(self):
        """載入所有指令檔案"""
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.bot.load_extension(f"cogs.{filename[:-3]}")

    async def start(self):
        """啟動機器人"""
        async with self.bot:
            await self._load_extensions()
            await self.bot.start(self.token)
