import time
import discord
from discord.ext import tasks, commands
from module import mongo_module


class Task(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # 開始執行函式
        self.notify_new_product.start()
        self.start_time = time.time()

    def cog_unload(self):
        # 取消執行函式
        self.notify_new_product.cancel()

    # 定義要執行的循環函式
    @tasks.loop(minutes=1)
    async def notify_new_product(self):
        db = mongo_module.connect_to_mongodb()
        collection = db['notify_log']
        data_list = mongo_module.find_documents(collection, {"status": "PENDING"})
        if data_list:
            channel_id = 533147349590081538
            channel = self.bot.get_channel(channel_id)
            embeds = [
                discord.Embed(
                    title=data['item']['product_name'],
                    description=data['item']['product_link']
                ).add_field(
                    name='賣家',
                    value=data['item']['seller_id'],
                    inline=True
                ).add_field(
                    name='價格',
                    value=data['item']['price'],
                    inline=True
                ) for data in data_list
            ]
            if embeds:
                await channel.send(embeds=embeds)
                ids_to_update = [data['_id'] for data in data_list]
                collection.update_many(
                    {"_id": {"$in": ids_to_update}},
                    {"$set": {"status": "REQUESTED"}}
                )


async def setup(bot: commands.Bot):
    await bot.add_cog(Task(bot))