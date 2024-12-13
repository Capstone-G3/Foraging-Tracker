import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
print(AWS_ACCESS_KEY_ID)
AWS_STORAGE_BUCKET_NAME='forage-bucket'
AWS_S3_ENDPOINT_URL='https://nyc3.digitaloceanspaces.com'

AWS_S3_OBJECT_PARAMETERS={
    "CacheControl" : 'max-age=86400'
}
AWS_LOCATION = 'https://forage-bucket.nyc3.digitaloceanspaces.com'

DEFAULT_FILE_STORAGE = 'forage-bucket.cdn.backends.MediaRootS3Boto3Storage'