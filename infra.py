import pulumi
from pulumi_aws import s3

class Bucket(pulumi.ComponentResource):

    def __init__(self, bucket_name: str, props=None, opts=None):
        super().__init__("InfraBucket", bucket_name, props, opts)
        # Create an AWS resource (S3 Bucket)
        self.tags = {"foo": "bar"}
        self.bucket = self.create_bucket(bucket_name="foo", tags=self.tags)

        # Export the name of the bucket
        # pulumi.export('bucket_name', self.bucket.id)
        self.register_outputs(
            {"bucket_name": self.bucket.id}
        )

    def create_bucket(self, bucket_name: str, tags: dict) -> s3.Bucket:
        bucket = s3.Bucket(bucket_name, tags=tags, opts=pulumi.ResourceOptions(parent=self))
        return bucket
            
class Infra(object):
    def __init__(self):
        pass

    def run(self):
        self.bucket = Bucket(bucket_name="foo")