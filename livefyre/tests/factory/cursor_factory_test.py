import datetime, unittest

from livefyre import Livefyre
from livefyre.tests import LfTest
from livefyre.src.factory.cursorfactory import CursorFactory
from livefyre.src.entity.topic import Topic


class CursorFactoryTestCase(LfTest, unittest.TestCase):
    LIMIT = 10
    
    def test_personal_stream_cursor(self):
        network = Livefyre.get_network(self.NETWORK_NAME, self.NETWORK_KEY)
        date = datetime.datetime.now()
        ps_resource = 'urn:livefyre:{}:user={}:personalStream'.format(network.name, self.USER_ID)
        
        cursor = CursorFactory.get_personal_stream_cursor(network, self.USER_ID)
        self.assertEquals(ps_resource, cursor.resource)
        
        cursor = CursorFactory.get_personal_stream_cursor(network, self.USER_ID, self.LIMIT, date)
        self.assertEquals(ps_resource, cursor.resource)
        self.assertEquals(self.LIMIT, cursor.limit)
        
    
    def test_topic_stream_cursor(self):
        network = Livefyre.get_network(self.NETWORK_NAME, self.NETWORK_KEY)
        date = datetime.datetime.now()
        topic_id = 'topic'
        label = 'label'
        ts_resource = 'urn:livefyre:{}:topic={}:topicStream'.format(network.name, topic_id)
        
        topic = Topic.create(network, topic_id, label)
        cursor = CursorFactory.get_topic_stream_cursor(network, topic)
        self.assertEquals(ts_resource, cursor.resource)
        
        cursor = CursorFactory.get_topic_stream_cursor(network, topic, self.LIMIT, date)
        self.assertEquals(ts_resource, cursor.resource)
        self.assertEquals(self.LIMIT, cursor.limit)
        
        
if __name__ == '__main__':
    unittest.main()