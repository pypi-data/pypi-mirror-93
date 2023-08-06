"""Base library test module"""

from matatika.library import MatatikaClient
from tests.unittest_base import UnittestBase


class TestLibrary(UnittestBase):
    """Test class for library"""

    def setUp(self):

        super().setUp()

        auth_token = 'auth-token'
        endpoint_url = 'endpoint-url'
        workspace_id = 'workspace-id'
        self.client = MatatikaClient(auth_token, endpoint_url, workspace_id)
