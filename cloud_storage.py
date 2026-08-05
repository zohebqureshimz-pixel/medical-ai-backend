import os
import boto3
from botocore.exceptions import ClientError

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")

s3_client = None

if S3_BUCKET_NAME and AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
            endpoint_url=S3_ENDPOINT_URL
        )
        print(f"[CloudStorage] S3 Client initialized for bucket: {S3_BUCKET_NAME}")
    except Exception as e:
        print(f"[CloudStorage Error] Failed to initialize S3 client: {e}")
else:
    print("[CloudStorage] S3 environment variables not set. Operating in local storage mode.")


def upload_file_to_cloud(local_file_path: str, cloud_key: str) -> bool:
    """Uploads a local file to S3 Cloud Storage if configured."""
    if not s3_client or not S3_BUCKET_NAME:
        return False
    try:
        s3_client.upload_file(local_file_path, S3_BUCKET_NAME, cloud_key)
        print(f"[CloudStorage Upload] Successfully uploaded {cloud_key} to cloud.")
        return True
    except Exception as e:
        print(f"[CloudStorage Upload Error] Failed uploading {cloud_key}: {e}")
        return False


def download_file_from_cloud(cloud_key: str, local_file_path: str) -> bool:
    """Downloads a file from S3 Cloud Storage to local path if configured."""
    if not s3_client or not S3_BUCKET_NAME:
        return False
    try:
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        s3_client.download_file(S3_BUCKET_NAME, cloud_key, local_file_path)
        print(f"[CloudStorage Download] Successfully fetched {cloud_key} from cloud.")
        return True
    except Exception as e:
        print(f"[CloudStorage Download Error] Failed fetching {cloud_key}: {e}")
        return False


def cloud_file_exists(cloud_key: str) -> bool:
    """Checks if a key exists in S3 Cloud Storage."""
    if not s3_client or not S3_BUCKET_NAME:
        return False
    try:
        s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=cloud_key)
        return True
    except ClientError:
        return False
