import unittest, pytest

from livefyre import Livefyre
from livefyre.tests import LfTest
from livefyre.src.utils import pyver


class NetworkTestCase(LfTest, unittest.TestCase):
    @pytest.mark.integration
    def test_set_user_sync_url(self):
        network = Livefyre.get_network(self.NETWORK_NAME, self.NETWORK_KEY)
        
        if pyver < 2.7:
            pass
        elif pyver < 3.0: 
            with self.assertRaisesRegexp(AssertionError, 'url_template should have {id}.'):
                network.set_user_sync_url('http://thisisa.test.url/')
        else:
            with self.assertRaisesRegex(AssertionError, 'url_template should have {id}.'):
                network.set_user_sync_url('http://thisisa.test.url/')
            
        network.set_user_sync_url('http://answers.livefyre.com/{id}')
        network.sync_user('user')
    
    @pytest.mark.unit
    def test_build_validate_user_token(self):
        network = Livefyre.get_network(self.NETWORK_NAME, self.NETWORK_KEY)
        
        if pyver < 2.7:
            pass
        elif pyver < 3.0:
            with self.assertRaisesRegexp(AssertionError, 'user_id should only contain alphanumeric characters'):
                network.build_user_auth_token('system@blah', 'testName', 86400.0)
        else:
            with self.assertRaisesRegex(AssertionError, 'user_id should only contain alphanumeric characters'):
                network.build_user_auth_token('system@blah', 'testName', 86400.0)
        
        token = network.build_livefyre_token()
        
        self.assertTrue(token)
        self.assertTrue(network.validate_livefyre_token(token))
        
        
if __name__ == '__main__':
    unittest.main()