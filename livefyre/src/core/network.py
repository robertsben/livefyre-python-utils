import time
import jwt, requests

from datetime import datetime
from livefyre.src.core.site import Site
from livefyre.src.api.personalizedstreams import PersonalizedStreamsClient
from livefyre.src.factory import CursorFactory
from livefyre.src.entity import Topic


class Network(object):
    DEFAULT_USER = 'system'
    DEFAULT_EXPIRES = 86400
    
    def __init__(self, name, key):
        self.name = name
        self.key = key
    
    
    def set_user_sync_url(self, url_template):
        assert '{id}' in url_template, 'url_template should have {id}.'
        
        url = 'http://{0!s}/'.format(self.name)
        data = {'actor_token' : self.build_livefyre_token(), 'pull_profile_url' : url_template}
        headers = {'Content-type': 'application/json'}
        
        request = requests.post(url=url, data=data, headers=headers)
        return request.status_code is 204
        
        
    def sync_user(self, user_id):
        url = 'http://{0!s}/api/v3_0/user/{1!s}/refresh'.format(self.name, user_id)
        data = {'lftoken' : self.build_livefyre_token()}
        headers = {'Content-type': 'application/json'}
        
        request = requests.post(url=url, data=data, headers=headers)
        return request.status_code is 200
    
    
    def build_livefyre_token(self):
        return self.build_user_auth_token(self.DEFAULT_USER, self.DEFAULT_USER, self.DEFAULT_EXPIRES)
    
    
    def build_user_auth_token(self, user_id, display_name, expires):
        assert user_id.isalnum(), 'user_id should only contain alphanumeric characters'

        return jwt.encode({
                'domain': self.name,
                'user_id': user_id,
                'display_name': display_name,
                'expires': int(time.time()) + expires},
            self.key)
    
    
    def validate_livefyre_token(self, lf_token):
        token_attr = jwt.decode(lf_token, self.key)
        return (token_attr['domain'] == self.name
            and token_attr['user_id'] == self.DEFAULT_USER
            and token_attr['expires'] >= int(time.time()))
        
    
    # Topic API
    def get_topic(self, topic_id):
        return PersonalizedStreamsClient.get_topic(self, topic_id)
    
    
    def create_or_update_topic(self, topic_id, label):
        topic = Topic.create(self, topic_id, label)
        PersonalizedStreamsClient.post_topic(self, topic)
        
        return topic


    def delete_topic(self, topic):
        return PersonalizedStreamsClient.patch_topic(self, topic)


    # Multiple Topic API
    def get_topics(self, limit = 100, offset = 0):
        return PersonalizedStreamsClient.get_topics(self, limit, offset)
    
    
    def create_or_update_topics(self, topic_value_map):
        topics = {}
        try:
            topics = [Topic.create(self, k, v) for k, v in topic_value_map.iteritems()]
        except:
            topics = [Topic.create(self, k, v) for k, v in topic_value_map.items()]
            
        return PersonalizedStreamsClient.post_topics(self, topics)


    def delete_topics(self, topics):
        return PersonalizedStreamsClient.patch_topics(self, topics)
    
    
    # Subscription API
    def get_subscriptions(self, user):
        return PersonalizedStreamsClient.get_subscriptions(self, user)

    
    def add_subscriptions(self, user, topics):
        return PersonalizedStreamsClient.post_subscriptions(self, user, topics)

    
    def update_subscriptions(self, user, topics):
        return PersonalizedStreamsClient.put_subscriptions(self, user, topics)

    
    def remove_subscriptions(self, user, topics):
        return PersonalizedStreamsClient.patch_subscriptions(self, user, topics)
    

    # Subscriber API
    def get_subscribers(self, topic, limit = 100, offset = 0):
        return PersonalizedStreamsClient.get_subscribers(self, topic, limit, offset)
    
    
    # Timeline cursor
    def get_topic_stream_cursor(self, topic, limit = 50, date = datetime.now()):
        return CursorFactory.get_topic_stream_cursor(self, topic, limit, date)
        
        
    def get_personal_stream_cursor(self, user, limit = 50, date = datetime.now()):
        return CursorFactory.get_personal_stream_cursor(self, user, limit, date)
        
        
    def get_urn(self):
        return 'urn:livefyre:' + self.name
    
    
    def get_user_urn(self, user):
        return self.get_urn() + ':user=' + user
        
    
    def get_site(self, site_id, site_key):
        return Site(self, site_id, site_key)