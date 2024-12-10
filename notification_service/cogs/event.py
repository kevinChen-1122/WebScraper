import discord
from typing import List, Union
from discord.ext import commands


class Event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 機器人加入伺服器
    @commands.Cog.listener()
    async def on_guild_join(self: discord.Guild):
        print(f"Bot 加入「{self.name}」伺服器")

    # 機器人離開伺服器
    @commands.Cog.listener()
    async def on_guild_remove(self: discord.Guild):
        print(f"Bot 離開「{self.name}」伺服器")

    # 伺服器更新
    @commands.Cog.listener()
    async def on_guild_update(self: discord.Guild, after: discord.Guild):
        if self.name != after.name:
            print(f"伺服器更新名稱「{self.name} -> {after.name}」")

    # 成員加入
    @commands.Cog.listener()
    async def on_member_join(self: discord.Member):
        print(f"「{self.display_name}」加入「{self.guild.name}」伺服器")

    # 成員離開
    @commands.Cog.listener()
    async def on_member_remove(self: discord.Member):
        print(f"「{self.display_name}」離開「{self.guild.name}」伺服器")

    # 成員封禁
    @commands.Cog.listener()
    async def on_member_ban(self: discord.Guild, user: discord.User):
        print(f"「{self.name}」伺服器 Ban「{user.display_name}」")

    # 成員解禁
    @commands.Cog.listener()
    async def on_member_unban(self: discord.Guild, user: discord.User):
        print(f"「{self.name}」伺服器 UnBan「{user.display_name}」")

    # 發送訊息
    @commands.Cog.listener()
    async def on_message(self: discord.Message):
        print(f"「{self.author.display_name}」發送訊息「{self.content}」")

    # 更改訊息
    @commands.Cog.listener()
    async def on_message_edit(self: discord.Message, after: discord.Message):
        print(f"「{self.author.display_name}」更改訊息「{self.content} -> {after.content}」")

    # 刪除訊息
    @commands.Cog.listener()
    async def on_message_delete(self: discord.Message):
        print(f"「{self.author.display_name}」刪除訊息「{self.content}」")

    # 添加反應
    @commands.Cog.listener()
    async def on_reaction_add(self: discord.Reaction, user: Union[discord.Member, discord.User]):
        print(f"「{user.display_name}」添加反應「{self.emoji}」到「{self.message.content}」訊息")

    # 移除反應
    @commands.Cog.listener()
    async def on_reaction_remove(self: discord.Reaction, user: Union[discord.Member, discord.User]):
        print(f"「{user.display_name}」移除反應「{self.emoji}」到「{self.message.content}」訊息")

    # 清空反應
    @commands.Cog.listener()
    async def on_reaction_clear(self: discord.Message, reaction: List[discord.Reaction]):
        reaction = [str(i.emoji) for i in reaction]
        print(f"訊息「{self.content}」移除所有反應「{', '.join(reaction)}」")

    # 監聽交互作用
    @commands.Cog.listener()
    async def on_interaction(self: discord.Interaction):
        print(f"「{self.user.display_name}」使用「/{self.command.name}」指令")

    # 監聽語音動作
    @commands.Cog.listener()
    async def on_voice_state_update(self: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel is None and after.channel:
            print(f"「{self.display_name}」加入「{after.channel.name}」語音頻道")
        elif before.channel and after.channel is None:
            print(f"「{self.display_name}」離開「{before.channel.name}」語音頻道")
        elif before.channel != after.channel:
            print(f"「{self.display_name}」移動「{before.channel.name} -> {after.channel.name}」語音頻道")


async def setup(bot: commands.Bot):
    await bot.add_cog(Event(bot))
