from storages.backends.s3boto3 import S3Boto3Storage

# This is where all the storages belong in for Media Serving as Production
class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = 'media'
