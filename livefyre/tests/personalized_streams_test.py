import unittest

from livefyre import Livefyre
from livefyre.tests import Config
from livefyre.src.entity import Topic


class LivefyreTestCase():#unittest.TestCase):
    def setUp(self):
        self.network = Livefyre.get_network(Config.NETWORK_NAME, Config.NETWORK_KEY)
        self.site = self.network.get_site(Config.SITE_ID, Config.SITE_KEY)
        

    def test_network_topic(self):
        topic = self.network.create_or_update_topic('1', 'UN')
        topic = self.network.get_topic(1)
        deleted = self.network.delete_topic(topic)
        topics = self.network.get_topics()
     
     
    def test_site_topic(self):
        topic = self.site.create_or_update_topic('2', 'DEUX')
        topic = self.site.get_topic(2)
        deleted = self.site.delete_topic(topic)
        topics = self.site.get_topics()
     
     
    def test_network_topics(self):
        topics = {'1': 'UN', '2': 'DEUX'}
        returned_topics = self.network.create_or_update_topics(topics)
        returned_topics = self.network.get_topics()
        deleted = self.network.delete_topics(returned_topics)
        topics = self.network.get_topics()
     
     
    def test_site_topics(self):
        topics = {'1': 'UN', '2': 'DEUX'}
        returned_topics = self.site.create_or_update_topics(topics)
        returned_topics = self.site.get_topics()
        deleted = self.site.delete_topics(returned_topics)
        topics = self.site.get_topics()
     
     
    def test_collection_topics(self):
        topic_dict = {'1': 'UN', '2': 'DEUX'}
        topics = self.site.create_or_update_topics(topic_dict)
         
        added = self.site.add_collection_topics(Config.COLLECTION_ID, topics)
        added, removed = self.site.update_collection_topics(Config.COLLECTION_ID, [topics[0]])
        removed = self.site.remove_collection_topics(Config.COLLECTION_ID, [topics[0]])
        collection_topics = self.site.get_collection_topics(Config.COLLECTION_ID)
         
        self.site.delete_topics(topics)
     
     
    def test_subscription_api(self):
        topic_dict = {'1': 'UN', '2': 'DEUX'}
        topics = self.network.create_or_update_topics(topic_dict)
         
        added = self.network.add_subscriptions(Config.USER, topics)
        user_subs = self.network.get_subscriptions(Config.USER)
        added, removed = self.network.update_subscriptions(Config.USER, [topics[1]])
        user_subs = self.network.get_subscribers(topics[1])
        removed = self.network.remove_subscriptions(Config.USER, [topics[1]])
         
        self.network.delete_topics(topics)
    
    def test_timeline_cursor(self):
        topic = Topic.create(self.network, "1", "UN")
        
        cursor = self.network.get_topic_stream_cursor(topic)
        data1 = cursor.previous()
        data2 = cursor.next()

        self.assertEquals(data1['data'], data2['data'])
    
        
if __name__ == '__main__':
    unittest.main()