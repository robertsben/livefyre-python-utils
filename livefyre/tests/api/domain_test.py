import unittest

from livefyre import Livefyre
from livefyre.tests import LfTest
from livefyre.src.api.domain import Domain


class DomainTestCase(LfTest, unittest.TestCase):
    def setUp(self):
        super(DomainTestCase, self).setUp()
        self.network = Livefyre.get_network(self.NETWORK_NAME, self.NETWORK_KEY)
        self.site = self.network.get_site(self.SITE_ID, self.SITE_KEY)
        self.collection = self.site.build_collection('TITLE', self.ARTICLE_ID, self.URL)
    
    def test_quill(self):
        quill_domain_ssl = 'https://{0}.quill.fyre.co'.format(self.network.get_network_name())
        domain = Domain.quill(self.network)
        self.assertEquals(quill_domain_ssl, domain)
        domain = Domain.quill(self.site)
        self.assertEquals(quill_domain_ssl, domain)
        domain = Domain.quill(self.collection)
        self.assertEquals(quill_domain_ssl, domain)
        
        quill_domain = 'http://quill.{0}'.format(self.network.name)
        self.network.ssl = False
        domain = Domain.quill(self.network)
        self.assertEquals(quill_domain, domain)
        domain = Domain.quill(self.site)
        self.assertEquals(quill_domain, domain)
        domain = Domain.quill(self.collection)
        self.assertEquals(quill_domain, domain)
    
    def test_bootstrap(self):
        bootstrap_domain_ssl = 'https://{0}.bootstrap.fyre.co'.format(self.network.get_network_name())
        domain = Domain.bootstrap(self.network)
        self.assertEquals(bootstrap_domain_ssl, domain)
        domain = Domain.bootstrap(self.site)
        self.assertEquals(bootstrap_domain_ssl, domain)
        domain = Domain.bootstrap(self.collection)
        self.assertEquals(bootstrap_domain_ssl, domain)
        
        bootstrap_domain = 'http://bootstrap.{0}'.format(self.network.name)
        self.network.ssl = False
        domain = Domain.bootstrap(self.network)
        self.assertEquals(bootstrap_domain, domain)
        domain = Domain.bootstrap(self.site)
        self.assertEquals(bootstrap_domain, domain)
        domain = Domain.bootstrap(self.collection)
        self.assertEquals(bootstrap_domain, domain)
     
        
if __name__ == '__main__':
    unittest.main()
