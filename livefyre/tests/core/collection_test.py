import datetime, unittest, jwt

from jwt import DecodeError
from livefyre import Livefyre
from livefyre.tests import LfTest
from livefyre.src.dto.topic import Topic
from livefyre.src.utils import pyver


class CollectionTestCase(LfTest, unittest.TestCase):
    CHECKSUM = '8bcfca7fb2187b1dcb627506deceee32'
    
    def setUp(self):
        super(CollectionTestCase, self).setUp()
        self.network = Livefyre.get_network(self.NETWORK_NAME, self.NETWORK_KEY)
        self.site = self.network.get_site(self.SITE_ID, self.SITE_KEY)
        
    def test_create_update_collection(self):
        name = 'PythonCreateCollection' + str(datetime.datetime.now())
        
        collection = self.site.build_livecomments_collection(name, name, self.URL).create_or_update()
        other_id = collection.get_collection_content()['collectionSettings']['collectionId']
        self.assertEqual(collection.data.collection_id, other_id)
        
        collection.data.title = name+'super'
        collection.create_or_update()
        #works but takes some time on the server side to update...
#         content = collection.get_collection_content()
#         self.assertEqual(name+'super', content['collectionSettings']['title'])
    
    def test_build_collection_token(self):
        collection = self.site.build_reviews_collection('title', 'articleId', 'https://livefyre.com')
        token = collection.build_collection_meta_token()
         
        self.assertTrue(token)
        self.assertEqual(jwt.decode(token, self.SITE_KEY)['type'], 'reviews')
        
        collection = self.site.build_liveblog_collection('title', 'articleId', 'https://livefyre.com')
        token = collection.build_collection_meta_token()
        self.assertEqual(jwt.decode(token, self.SITE_KEY)['type'], 'liveblog')
        
        topics = [Topic.create(self.network, '1', '1')]
        collection = self.site.build_livecomments_collection(self.TITLE, self.ARTICLE_ID, self.URL)
        collection.data.topics = topics
        self.assertTrue(collection.is_network_issued())
        
        token = collection.build_collection_meta_token()
        
        if pyver < 2.7:
            pass
        elif pyver < 3.0:
            with self.assertRaisesRegexp(DecodeError, 'Signature verification failed'):
                jwt.decode(token, self.site.data.key)
        else:
            with self.assertRaisesRegex(DecodeError, 'Signature verification failed'):
                jwt.decode(token, self.site.data.key)
        
        decoded_token = jwt.decode(token, self.network.data.key)
        self.assertEqual(self.network.urn, decoded_token['iss'])
    
    def test_build_checksum(self):
        collection = self.site.build_livecomments_collection('title', 'articleId', 'http://livefyre.com')
        collection.data.tags = 'tags'

        checksum = collection.build_checksum()
        self.assertEqual(self.CHECKSUM, checksum, 'checksum is not correct.')
        

if __name__ == '__main__':
    unittest.main()