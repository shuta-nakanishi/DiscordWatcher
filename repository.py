import json
import os
import boto3

# ステータスの保存・読み込みを抽象化するリポジトリクラスとその実装を定義します。 --- IGNORE ---
class StatusRepository:

    def load_status(self):
        raise NotImplementedError()

    def save_status(self, status):
        raise NotImplementedError()

# ローカルファイルにステータスを保存・読み込みするリポジトリ
class LocalFileRepository(StatusRepository):

    def __init__(self, file_name):
        self.file_name = file_name

    # 前回のステータスを読み込む
    def load_status(self):

        if os.path.exists(self.file_name):

            try:

                with open(
                    self.file_name,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data = json.load(f)

                    return data.get(
                        "desktop_status",
                        "offline"
                    )

            except Exception:

                return "offline"

        return "offline"

    # 現在のステータスを保存する
    def save_status(self, status):

        with open(
            self.file_name,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "desktop_status": status
                },
                f,
                ensure_ascii=False,
                indent=4
            )
            
# S3にステータスを保存・読み込みするリポジトリ
class S3Repository(StatusRepository):

    def __init__(self, bucket_name, key):

        self.bucket_name = bucket_name
        self.key = key
        self.s3 = boto3.client("s3")

    # 前回のステータスを読み込む
    def load_status(self):

        try:

            response = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=self.key
            )

            body = response["Body"].read()

            data = json.loads(
                body.decode("utf-8")
            )

            return data.get(
                "desktop_status",
                "offline"
            )

        except Exception:

            return "offline"

    # 現在のステータスを保存する
    def save_status(self, status):

        body = json.dumps(
            {
                "desktop_status": status
            },
            ensure_ascii=False,
            indent=4
        )

        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=self.key,
            Body=body,
            ContentType="application/json"
        )