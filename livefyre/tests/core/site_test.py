import unittest

from livefyre import Livefyre
from livefyre.tests import LfTest
from livefyre.src.utils import pyver


class SiteTestCase(LfTest, unittest.TestCase):
    def test_build_collection(self):
        site = Livefyre.get_network(self.NETWORK_NAME, self.NETWORK_KEY).get_site(self.SITE_ID, self.SITE_KEY)
        
        if pyver < 2.7:
            pass
        elif pyver < 3.0:
            with self.assertRaisesRegexp(AssertionError, 'url must be a full domain. ie. http://livefyre.com'):
                site.build_livecomments_collection('title', 'articleId', 'url.com')
            with self.assertRaisesRegexp(AssertionError, 'title\'s length should be under 255 char'):
                site.build_livecomments_collection('1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456', 'article_id', 'http://url.com')
        else:
            with self.assertRaisesRegex(AssertionError, 'url must be a full domain. ie. http://livefyre.com'):
                site.build_livecomments_collection('title', 'articleId', 'url.com')
            with self.assertRaisesRegex(AssertionError, 'title\'s length should be under 255 char'):
                site.build_livecomments_collection('1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456', 'article_id', 'http://url.com')
        
        if pyver >= 2.7:
            with self.assertRaises(AssertionError):
                site.build_collection('bad type', self.TITLE, self.ARTICLE_ID, self.URL)
                

        collection = site.build_livecomments_collection(self.TITLE, self.ARTICLE_ID, self.URL)
        self.assertTrue(collection)


    #test other collection creation types

if __name__ == '__main__':
    unittest.main()