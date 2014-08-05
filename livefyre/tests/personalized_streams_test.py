import unittest

from livefyre import Livefyre
from livefyre.tests import Config
from livefyre.src.entity import Topic
from livefyre.src.api.personalizedstreams import PersonalizedStreamsClient
from livefyre.src.factory import CursorFactory


class LivefyreTestCase():#unittest.TestCase):
    def setUp(self):
        self.network = Livefyre.get_network(Config.NETWORK_NAME, Config.NETWORK_KEY)
        self.site = self.network.get_site(Config.SITE_ID, Config.SITE_KEY)
        

    def test_network_topic(self):
        topic = PersonalizedStreamsClient.create_or_update_topic(self.network, '1', 'UN')
        topic = PersonalizedStreamsClient.get_topic(self.network, 1)
        deleted = PersonalizedStreamsClient.delete_topic(self.network, topic)
        topics = PersonalizedStreamsClient.get_topics(self.network)
     
     
    def test_site_topic(self):
        topic = PersonalizedStreamsClient.create_or_update_topic(self.site, '2', 'DEUX')
        topic = PersonalizedStreamsClient.get_topic(self.site, 2)
        deleted = PersonalizedStreamsClient.delete_topic(self.site, topic)
        topics = PersonalizedStreamsClient.get_topics(self.site)
     
     
    def test_network_topics(self):
        topics = {'1': 'UN', '2': 'DEUX'}
        returned_topics = PersonalizedStreamsClient.create_or_update_topics(self.network, topics)
        returned_topics = PersonalizedStreamsClient.get_topics(self.network)
        deleted = PersonalizedStreamsClient.delete_topics(self.network, returned_topics)
        topics = PersonalizedStreamsClient.get_topics(self.network)
     
     
    def test_site_topics(self):
        topics = {'1': 'UN', '2': 'DEUX'}
        returned_topics = PersonalizedStreamsClient.create_or_update_topics(self.site, topics)
        returned_topics = PersonalizedStreamsClient.get_topics(self.site)
        deleted = PersonalizedStreamsClient.delete_topics(self.site, returned_topics)
        topics = PersonalizedStreamsClient.get_topics(self.site)
     
     
    def test_collection_topics(self):
        topic_dict = {'1': 'UN', '2': 'DEUX'}
        topics = PersonalizedStreamsClient.create_or_update_topics(self.site, topic_dict)
         
        added = PersonalizedStreamsClient.add_collection_topics(self.site, Config.COLLECTION_ID, topics)
        added, removed = PersonalizedStreamsClient.replace_collection_topics(self.site, Config.COLLECTION_ID, [topics[0]])
        removed = PersonalizedStreamsClient.remove_collection_topics(self.site, Config.COLLECTION_ID, [topics[0]])
        collection_topics = PersonalizedStreamsClient.get_collection_topics(self.site, Config.COLLECTION_ID)
         
        PersonalizedStreamsClient.delete_topics(self.site, topics)

     
    def test_subscription_api(self):
        user_token = self.network.build_user_auth_token(Config.USER_ID, Config.USER_ID + '@' + Config.NETWORK_NAME, self.network.DEFAULT_EXPIRES)
        topic_dict = {'1': 'UN', '2': 'DEUX'}
        topics = PersonalizedStreamsClient.create_or_update_topics(self.network, topic_dict)
         
        added = PersonalizedStreamsClient.add_subscriptions(self.network, user_token, topics)
        user_subs = PersonalizedStreamsClient.get_subscriptions(self.network, Config.USER_ID)
        added, removed = PersonalizedStreamsClient.replace_subscriptions(self.network, user_token, [topics[1]])
        user_subs = PersonalizedStreamsClient.get_subscribers(self.network, topics[1])
        removed = PersonalizedStreamsClient.remove_subscriptions(self.network, user_token, [topics[1]])
         
        PersonalizedStreamsClient.delete_topics(self.network, topics)
    
    def test_timeline_cursor(self):
        topic = Topic.create(self.network, "1", "UN")
        
        cursor = CursorFactory.get_topic_stream_cursor(self.network, topic)
        data1 = cursor.previous()
        data2 = cursor.next()

        self.assertEquals(data1['data'], data2['data'])
    
        
if __name__ == '__main__':
    unittest.main()