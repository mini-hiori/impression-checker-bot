import os
import re

import discord

from impression_fetcher import get_bms_list, get_event_list, get_stats

TOKEN = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理


@client.event
async def on_ready():
    print('ログインしました')

# メッセージ受信時に動作する処理


@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    print(message.content)
    if message.author.bot:
        return
    if re.match(r"/stats event=[0-9]+ id=[0-9]+", message.content):
        event_id, bms_id = re.search(
            r"/インプレ旋回 event=([0-9]+) id=([0-9]+)", message.content).groups()
        ret = get_stats(event_id, bms_id)
        if ret:
            await message.channel.send(ret)
        else:
            await message.channel.send("つながらへんのん")
    elif re.match(r"/recent_short_impression event=[0-9]+ id=[0-9]+", message.content):
        event_id, bms_id = re.search(
            r"/インプレ旋回 event=([0-9]+) id=([0-9]+)", message.content).groups()
        ret = get_stats(event_id, bms_id)
        if ret:
            await message.channel.send(ret)
        else:
            await message.channel.send("つながらへんのん")
    elif message.content == "/event_list":
        ret = get_event_list()
        if ret:
            ret = ret.split("\n")
            # 2000文字までしか送れないらしいので、途中で切る
            await message.channel.send("\n".join(ret[:75]))
            if ret[75:]:
                await message.channel.send("\n".join(ret[75:]))
        else:
            await message.channel.send("つながらへんのん")
    elif re.match(r"/bms_list event=[0-9]+", message.content):
        bms_id = re.search(
            r"/bms_list event=([0-9]+)",
            message.content).groups()[0]
        print(bms_id)
        ret = get_bms_list(bms_id)
        if ret:
            ret = ret.split("\n")
            # 2000文字までしか送れないらしいので、途中で切る
            await message.channel.send("\n".join(ret[:75]))
            if ret[75:]:
                await message.channel.send("\n".join(ret[75:]))
        else:
            await message.channel.send("つながらへんのん")
    else:
        ret = "正しいメッセージを送卵塊！"
        await message.channel.send(ret)


if __name__ == '__main__':
    client.run(TOKEN)
