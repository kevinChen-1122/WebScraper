import asyncio
from module import discord_module, get_config_module


async def main():
    bot = discord_module.Discord(token=get_config_module.discord_bot_token)
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
