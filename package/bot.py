import discord

from config import Config
from repository import (
    LocalFileRepository,
    S3Repository
)

def create_repository():

    if Config.STATUS_STORAGE == "s3":

        return S3Repository(
            bucket_name=Config.S3_BUCKET_NAME,
            key=Config.S3_STATUS_KEY
        )

    return LocalFileRepository(
        "last_status.json"
    )


repository = create_repository()

TOKEN = Config.DISCORD_TOKEN
TARGET_USER_ID = Config.TARGET_USER_ID
NOTIFY_CHANNEL_ID = Config.NOTIFY_CHANNEL_ID

# discordサーバーの基本情報を取得するための標準設定を有効化
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# クライアントを作成し、初期状態を非表示に設定
client = discord.Client(intents=intents, status=discord.Status.invisible)

# クライアントが準備できたときに呼び出されるイベントハンドラー
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    try:

        target_member = None

        for guild in client.guilds:

            member = guild.get_member(
                TARGET_USER_ID
            )

            if member:
                target_member = member
                break

        if not target_member:

            print(
                f"ユーザーID: "
                f"{TARGET_USER_ID} "
                f"が見つかりませんでした。"
            )

            return

       # PC版のオンラインステータスを文字列として取得する
        current_desktop_status = str(
            target_member.desktop_status
        )

        print(
            f"現在のPCステータス: "
            f"{current_desktop_status}"
        )

        # 前回のPCステータスを読み込む
        previous_desktop_status = (
            repository.load_status()
        )

        print(
            f"前回のPCステータス: "
            f"{previous_desktop_status}"
        )

        # オフラインからオンラインへの状態遷移を検知する
        if (
            previous_desktop_status == "offline"
            and current_desktop_status == "online"
        ):

            print(
                "状態遷移検知: "
                "offline -> online"
            )

            # 通知チャンネルにメッセージを送信
            channel = await client.fetch_channel(
                NOTIFY_CHANNEL_ID
            )

            await channel.send(
                "オオクラ ガ "
                "オンライン ニナリマシタ"
            )

        # 現在のPCステータスを保存する
        repository.save_status(
            current_desktop_status
        )

    except Exception as e:

        print(
            f"エラーが発生しました: {e}"
        )

    finally:

        await client.close()

# クライアントを実行する
client.run(TOKEN)