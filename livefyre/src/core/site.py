import base64, sys, hashlib
import jwt, requests

from datetime import datetime
from livefyre.src.utils import is_valid_full_url
from livefyre.src.api.personalizedstreams import PersonalizedStreamsClient
from livefyre.src.entity import Topic
from livefyre.src.factory import CursorFactory

try:
    import simplejson as json
except ImportError:
    import json


class Site(object):
    TYPE = ['reviews', 'sidenotes', 'ratings', 'counting', 'liveblog', 'livechat', 'livecomments']
    
    def __init__(self, network, site_id, site_key):
        self.network = network
        self.site_id = site_id
        self.site_key = site_key
    
    
    def build_collection_meta_token(self, title, article_id, url, options={}):
        assert is_valid_full_url(url), 'url must be a full domain. ie. http://livefyre.com'
        assert len(title) <= 255, "title's length should be under 255 char"
        
        collection_meta = {
            'title': title,
            'url': url,
            'articleId': article_id
        }
        
        if 'type' in options and options['type'] not in self.TYPE:
            raise AssertionError('type is not a recognized type. must be in {0}'.format(self.TYPE))
        
        collection_meta.update(options)
        return jwt.encode(collection_meta, self.site_key)
    
    
    def build_checksum(self, title, url, tags=''):
        assert is_valid_full_url(url), 'url must be a full domain. ie. http://livefyre.com'
        assert len(title) <= 255, "title's length should be under 255 char"
        
        meta_string = '{{"tags":"{0}","title":"{1}","url":"{2}"}}'.format(tags, title, url)

        return hashlib.md5(meta_string).hexdigest()
    
    
    def create_collection(self, title, article_id, url, tags='', s_type=None):
        url = 'http://quill.{0!s}/api/v3.0/site/{1!s}/collection/create/'.format(self.network.name, self.site_id)
        data = {
            'articleId': article_id,
            'collectionMeta': self.build_collection_meta_token(title, article_id, url, tags, s_type),
            'checksum': self.build_checksum(title, url, tags),
        }
        headers = {'content-type': 'application/json'}
            
        response = requests.post(url, params={'sync':1}, data=json.dumps(data), headers=headers)
        
        if response.status_code == 200:
            return response.json()['data']['collectionId']
        return None
    
    
    def get_collection_content(self, article_id):
        if sys.version_info >= (3, 0):
            article_bytes = bytes(str(article_id), 'utf-8')
        else:
            article_bytes = bytes(str(article_id))
        encoded_article_id = base64.b64encode(article_bytes).decode('utf-8')
        url = 'http://bootstrap.{0!s}/bs3/{0!s}/{1!s}/{2!s}/init'.format(self.network.name, self.site_id, encoded_article_id)
        
        response = requests.get(url=url)
        if response.status_code == 200:
            return response.json()
        return None


    def get_collection_id(self, article_id):
        json = self.get_collection_content(article_id)
        if json:
            return json['collectionSettings']['collectionId']
        return None


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
    
    
    # Collection Topic API
    def get_collection_topics(self, collection_id):
        return PersonalizedStreamsClient.get_collection_topics(self, collection_id)
    
    
    def add_collection_topics(self, collection_id, topics):
        return PersonalizedStreamsClient.post_collection_topics(self, collection_id, topics)
    
    
    def update_collection_topics(self, collection_id, topics):
        return PersonalizedStreamsClient.put_collection_topics(self, collection_id, topics)
    
    
    def remove_collection_topics(self, collection_id, topics):
        return PersonalizedStreamsClient.patch_collection_topics(self, collection_id, topics)
    
    
    # Timeline cursor
    
    def get_topic_stream_cursor(self, topic, limit = 50, date = datetime.now()):
        return CursorFactory.get_topic_stream_cursor(self, topic, limit, date)


    def get_urn(self):
        return self.network.get_urn() + ":site=" + self.site_id
