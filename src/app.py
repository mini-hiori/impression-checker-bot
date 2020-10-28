import math
import os
import re
import traceback

import discord

from impression_fetcher import (get_bms_list, get_event_list,
                                get_long_impression, get_short_impression,
                                get_stats)

TOKEN = os.environ['DISCORD_BOT_TOKEN']
TARGET_CHANNEL_LIST = ["インプレ旋回bot"]

# 接続に必要なオブジェクトを生成
client = discord.Client()


@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_message(message):
    if message.author.bot or str(message.channel) not in TARGET_CHANNEL_LIST:
        # 発言者がbotなら無視、また/インプレ旋回bot以外のチャンネルの発言は無視
        # message.channelはdiscord.channel.TextChannel型なのでstrと直接比較できない
        return
    if message.content.startswith("/"):
        # /から始まる発言にだけ反応
        try:
            if message.content == "/インプレ旋回":
                # hello
                await message.channel.send("インプレ旋回！")
            elif re.match(r"/stats event=[0-9]+ id=[0-9]+", message.content):
                event_id, bms_id = re.search(
                    r"/stats event=([0-9]+) id=([0-9]+)", message.content).groups()
                ret = get_stats(event_id, bms_id)
                if ret:
                    await message.channel.send(ret)
                else:
                    await message.channel.send("インプレ取得に失敗しました バグ鴨試練")
            elif re.match(r"/check_short_impression event=[0-9]+ id=[0-9]+", message.content):
                event_id, bms_id = re.search(
                    r"/check_short_impression event=([0-9]+) id=([0-9]+)", message.content).groups()
                ret = get_short_impression(event_id, bms_id)
                if ret:
                    # 2000文字までしか送れないので…
                    for i in range(math.ceil(len(ret) / 800)):
                        await message.channel.send(ret[i * 800:(i + 1) * 800])
                else:
                    await message.channel.send("インプレ取得に失敗しました バグ鴨試練")
            elif re.match(r"/check_long_impression event=[0-9]+ id=[0-9]+", message.content):
                event_id, bms_id = re.search(
                    r"/check_long_impression event=([0-9]+) id=([0-9]+)", message.content).groups()
                ret = get_long_impression(event_id, bms_id)
                if ret:
                    # 2000文字までしか送れないので…
                    for i in range(math.ceil(len(ret) / 800)):
                        await message.channel.send(ret[i * 800:(i + 1) * 800])
                else:
                    await message.channel.send("インプレ取得に失敗しました バグ鴨試練")
            elif message.content == "/event_list":
                ret = get_event_list()
                if ret:
                    ret = ret.split("\n")
                    # 2000文字までしか送れないらしいので、途中で切る
                    await message.channel.send("\n".join(ret[:50]))
                    if ret[50:]:
                        await message.channel.send("\n".join(ret[50:]))
                else:
                    await message.channel.send("インプレ取得に失敗しました バグ鴨試練")
            elif re.match(r"/bms_list event=[0-9]+", message.content):
                bms_id = re.search(
                    r"/bms_list event=([0-9]+)",
                    message.content).groups()[0]
                print(bms_id)
                ret = get_bms_list(bms_id)
                if ret:
                    ret = ret.split("\n")
                    # 2000文字までしか送れないらしいので、途中で切る
                    await message.channel.send("\n".join(ret[:50]))
                    if ret[50:]:
                        await message.channel.send("\n".join(ret[50:]))
                else:
                    await message.channel.send("インプレ取得に失敗しました バグ鴨試練")
            else:
                ret = "正しいメッセージを送卵塊！\nコマンド説明はピン留めしてあるよ"
                await message.channel.send(ret)
        except BaseException:
            traceback.print_exc()
            await message.channel.send("バグりました 修正旋回！！！！！！")


if __name__ == '__main__':
    client.run(TOKEN)
