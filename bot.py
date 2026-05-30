import asyncio
import json
import os
import subprocess
import sys
import discord

# 【重要】トークンは環境変数などから読み込む形を強く推奨します
TOKEN = "MTUwODAzNTgxNTQ1NDkzMzE4NQ.GD0vQb.cTDY1T_CDJ1qTzHt0yP4hcCyWgSN_HIJHGpEoU"
TARGET_USER_ID = 843761269411938305
NOTIFY_CHANNEL_ID = 1508034338602877049

# 状態を保存する外部ファイル名
STATUS_FILE = "last_status.json"

intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)


# 前回保存したPC版ステータスを読み込む関数
# 存在しない場合は'offline'を返す
def load_previous_status():
    """前回実行時のステータスをファイルから読み込む"""
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("desktop_status", "offline")
        except Exception:
            return "offline"
    return "offline"


# 現在のPC版ステータスを保存する関数
# 次回実行時に前回値と比較できるようにする
def save_current_status(status_str):
    """今回のステータスをファイルに保存する"""
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump({"desktop_status": status_str}, f, ensure_ascii=False, indent=4)


@client.event
async def on_ready():

    print(f"Logged in as {client.user}")

    # Botのステータスを一時的に非表示にする（オプション）
    await client.change_presence(status=discord.Status.invisible)

    try:

        target_member = None

        # Botが参加しているサーバーから対象ユーザー検索
        for guild in client.guilds:

            member = guild.get_member(TARGET_USER_ID)

            if member:
                target_member = member
                break

        if not target_member:
            print(
                f"ユーザーID: {TARGET_USER_ID} が見つかりませんでした。"
            )

            await client.close()
            return

        # 現在のPC版Discord状態
        current_desktop_status = str(
            target_member.desktop_status
        )

        print(
            f"現在のPCステータス: "
            f"{current_desktop_status}"
        )

        # 前回状態
        previous_desktop_status = load_previous_status()

        print(
            f"前回のPCステータス: "
            f"{previous_desktop_status}"
        )

        # offline -> online
        if (
            previous_desktop_status == "offline"
            and current_desktop_status == "online"
        ):

            print(
                "状態遷移検知: "
                "offline -> online"
            )

            channel = client.get_channel(NOTIFY_CHANNEL_ID)
            if channel:
                await channel.send(
                    f"test"
                )

        # 今回状態保存
        save_current_status(
            current_desktop_status
        )

    except Exception as e:

        print(f"エラー: {e}")

    finally:

        # 単発実行なので終了
        await client.close()


client.run(TOKEN)