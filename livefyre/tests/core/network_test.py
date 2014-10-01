import unittest, pytest

from livefyre import Livefyre
from livefyre.tests import LfTest


class NetworkTestCase(LfTest, unittest.TestCase):
    @pytest.mark.integration
    def test_set_user_sync_url(self):
        network = Livefyre.get_network(self.NETWORK_NAME, self.NETWORK_KEY)
        with self.assertRaisesRegexp(AssertionError, 'url_template should have {id}.'):
            network.set_user_sync_url('http://thisisa.test.url/')
            
        self.assertTrue(network.set_user_sync_url('http://answers.livefyre.com/{id}'))
        self.assertTrue(network.sync_user('user'))
        
    @pytest.mark.unit
    def test_build_validate_user_token(self):
        network = Livefyre.get_network(self.NETWORK_NAME, self.NETWORK_KEY)
        
        with self.assertRaisesRegexp(AssertionError, 'user_id should only contain alphanumeric characters'):
            network.build_user_auth_token('system@blah', 'testName', 86400.0)
        
        token = network.build_livefyre_token()
        
        self.assertIsNotNone(token)
        self.assertTrue(network.validate_livefyre_token(token))
        
        
if __name__ == '__main__':
    unittest.main()