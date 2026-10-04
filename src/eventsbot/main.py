import threading
import asyncio
import pathlib

import discord
import dotenv

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.none()
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged in as {self.user.name}.")
        await self.tree.sync()

@discord.app_commands.command(description="指定された時間の後、指定されたユーザーにメンションを行う")
@discord.app_commands.guild_only
@discord.app_commands.describe(user="ターゲット", minutes="待機時間（分）")
async def scheduled_mention(interaction: discord.Interaction, user: discord.Member, minutes: int):
    async def after():
        await asyncio.sleep(60 * minutes)
        await interaction.followup.send(user.mention)
    asyncio.create_task(after())
    await interaction.response.send_message("予約完了")

if __name__ == "__main__":
    TOKEN = dotenv.get_key(pathlib.Path(__file__).parent.parent.parent.joinpath(".env"), "TOKEN")
    client = Client()
    client.tree.add_command(scheduled_mention)
    client.run(TOKEN)
