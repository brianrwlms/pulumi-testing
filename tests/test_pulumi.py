from mock import Mock
import pulumi
import pytest


class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + '_id', args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}

pulumi.runtime.set_mocks(
    MyMocks(),
    preview=False,  # Sets the flag `dry_run`, which is true at runtime during a preview.
)

# import infra
from infra import Infra

@pytest.mark.unit
# @pytest.mark.xfail  # remove this or comment if you remove the "bar" assertion to have it pass
@pulumi.runtime.test
def test_bucket_tags():
    infra = Infra()
    infra.run()
    def check_tags(args):
        urn, tags = args
        assert tags, f'server {urn} must have tags'
        assert "foo" in tags, f"foo t be in tags"
        # comment below out to pass
        # assert "bar" in tags, f"bIar must be in tags"
    return pulumi.Output.all(infra.bucket.bucket.urn, infra.bucket.bucket.tags).apply(check_tags)

@pytest.fixture
def infra():
    infra = Infra()
    return infra

@pytest.mark.unit
def test_bucket_creation_with_pytest(mocker, infra):
    # create a mock to patch the Bucket.create_bucket() method
    m_create_bucket = Mock()
    # patch the actual method with the Mock
    mocker.patch("infra.Bucket.create_bucket", m_create_bucket)
    # run the program
    # us infra fixture
    infra.run()
    m_create_bucket.assert_called_once_with(bucket_name="foo", tags={"foo": "bar"})
