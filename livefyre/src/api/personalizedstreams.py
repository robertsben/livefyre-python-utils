import requests

from livefyre.src.api import get_lf_token_header
from livefyre.src.entity import Topic, Subscription, SubscriptionType

try:
    import simplejson as json
except ImportError:
    import json


def get_url(core):
    return PersonalizedStreamsClient.BASE_URL.format(core.get_network_name())


class PersonalizedStreamsClient(object):
    BASE_URL = 'https://{}.quill.fyre.co/api/v4'
    STREAM_BASE_URL = 'https://bootstrap.livefyre.com/api/v4'
    
    TOPIC_PATH = '/{}/'
    MULTIPLE_TOPIC_PATH = '/{}:topics/';
    COLLECTION_TOPICS_PATH = '/{}:collection={}:topics/';
    USER_SUBSCRIPTION_PATH = '/{}:subscriptions/';
    TOPIC_SUBSCRIPTION_PATH = '/{}:subscribers/';
    TIMELINE_PATH = '/timeline/';
    
    
    @staticmethod
    def get_topic(core, topic_id):
        url = get_url(core) + PersonalizedStreamsClient.TOPIC_PATH.format(Topic.generate_urn(core, topic_id))
        headers = get_lf_token_header(core)

        response = requests.get(url, headers = headers)
        data = response.json()['data']
        
        return Topic.serialize_from_json(data['topic']) if 'topic' in data else None


    @staticmethod
    def get_topics(core, limit, offset):
        url = get_url(core) + PersonalizedStreamsClient.MULTIPLE_TOPIC_PATH.format(core.get_urn())
        headers = get_lf_token_header(core)

        response = requests.get(url, params = {'limit': limit, 'offset': offset}, headers = headers)
        data = response.json()['data']
        
        return [Topic.serialize_from_json(x) for x in data['topics']] if 'topics' in data else []


    @staticmethod
    def post_topics(core, topics):
        for topic in topics:
            assert topic.label and len(topic.label) <= 128, 'topic label should not be empty and have 128 or less characters'
        
        url = get_url(core) + PersonalizedStreamsClient.MULTIPLE_TOPIC_PATH.format(core.get_urn())
        form = json.dumps({'topics': [x.to_dict() for x in topics]})
        headers = get_lf_token_header(core)
        headers['Content-Type'] = 'application/json'
        
        response = requests.post(url, data = form, headers = headers)
        data = response.json()['data']
        
        created = data['created'] if 'created' in data else 0
        updated = data['updated'] if 'updated' in data else 0
            
        return created, updated
        
        
    @staticmethod
    def patch_topics(core, topics):
        url = get_url(core) + PersonalizedStreamsClient.MULTIPLE_TOPIC_PATH.format(core.get_urn())
        form = json.dumps({'delete': [x.topic_id for x in topics]})
        headers = get_lf_token_header(core)
        headers['Content-Type'] = 'application/json'
        
        response = requests.patch(url, data = form, headers = headers)
        data = response.json()['data']
        
        return data['deleted'] if 'deleted' in data else 0
    
    
    @staticmethod
    def get_collection_topics(site, collection_id):
        url = get_url(site) + PersonalizedStreamsClient.COLLECTION_TOPICS_PATH.format(site.get_urn(), collection_id)
        headers = get_lf_token_header(site)

        response = requests.get(url, headers = headers)
        data = response.json()['data']
        
        return data['topicIds'] if 'topicIds' in data else None


    @staticmethod
    def post_collection_topics(site, collection_id, topics):
        url = get_url(site) + PersonalizedStreamsClient.COLLECTION_TOPICS_PATH.format(site.get_urn(), collection_id)
        form = json.dumps({'topicIds': [x.topic_id for x in topics]})
        headers = get_lf_token_header(site)
        headers['Content-Type'] = 'application/json'
        
        response = requests.post(url, data = form, headers = headers)
        data = response.json()['data']

        return data['added'] if 'added' in data else 0
    
    
    @staticmethod
    def put_collection_topics(site, collection_id, topics):
        url = get_url(site) + PersonalizedStreamsClient.COLLECTION_TOPICS_PATH.format(site.get_urn(), collection_id)
        form = json.dumps({'topicIds': [x.topic_id for x in topics]})
        headers = get_lf_token_header(site)
        headers['Content-Type'] = 'application/json'
        
        response = requests.put(url, data = form, headers = headers)
        data = response.json()['data']
        
        added = data['added'] if 'added' in data else 0
        removed = data['removed'] if 'removed' in data else 0
            
        return added, removed
        
        
    @staticmethod
    def patch_collection_topics(site, collection_id, topics):
        url = get_url(site) + PersonalizedStreamsClient.COLLECTION_TOPICS_PATH.format(site.get_urn(), collection_id)
        form = json.dumps({'delete': [x.topic_id for x in topics]})
        headers = get_lf_token_header(site)
        headers['Content-Type'] = 'application/json'
        
        response = requests.patch(url, data = form, headers = headers)
        data = response.json()['data']
    
        return data['removed'] if 'removed' in data else 0
    
    
    @staticmethod
    def get_subscriptions(network, user):
        url = get_url(network) + PersonalizedStreamsClient.USER_SUBSCRIPTION_PATH.format(network.get_user_urn(user))
        headers = get_lf_token_header(network)

        response = requests.get(url, headers = headers)
        data = response.json()['data']
        
        return [Subscription.serialize_from_json(x) for x in data['subscriptions']] if 'subscriptions' in data else []


    @staticmethod
    def post_subscriptions(network, user, topics):
        url = get_url(network) + PersonalizedStreamsClient.USER_SUBSCRIPTION_PATH.format(network.get_user_urn(user))
        form = json.dumps({'subscriptions': [Subscription(x.topic_id, user, SubscriptionType.personalStream).to_dict() for x in topics]})
        headers = get_lf_token_header(network, user)
        headers['Content-Type'] = 'application/json'
        
        response = requests.post(url, data = form, headers = headers)
        data = response.json()['data']
        
        return data['added'] if 'added' in data else 0
    
    
    @staticmethod
    def put_subscriptions(network, user, topics):
        url = get_url(network) + PersonalizedStreamsClient.USER_SUBSCRIPTION_PATH.format(network.get_user_urn(user))
        form = json.dumps({'subscriptions': [Subscription(x.topic_id, user, SubscriptionType.personalStream).to_dict() for x in topics]})
        headers = get_lf_token_header(network, user)
        headers['Content-Type'] = 'application/json'
        
        response = requests.put(url, data = form, headers = headers)
        data = response.json()['data']
        
        added = data['added'] if 'added' in data else 0
        removed = data['removed'] if 'removed' in data else 0
            
        return added, removed
        
        
    @staticmethod
    def patch_subscriptions(network, user, topics):
        url = get_url(network) + PersonalizedStreamsClient.USER_SUBSCRIPTION_PATH.format(network.get_user_urn(user))
        form = json.dumps({'delete': [Subscription(x.topic_id, user, SubscriptionType.personalStream).to_dict() for x in topics]})
        headers = get_lf_token_header(network, user)
        headers['Content-Type'] = 'application/json'
        
        response = requests.patch(url, data = form, headers = headers)
        data = response.json()['data']
    
        return data['removed'] if 'removed' in data else 0
    
    
    @staticmethod
    def get_subscribers(network, topic, limit, offset):
        url = get_url(network) + PersonalizedStreamsClient.TOPIC_SUBSCRIPTION_PATH.format(topic.topic_id)
        headers = get_lf_token_header(network)

        response = requests.get(url, params = {'limit': limit, 'offset': offset}, headers = headers)
        data = response.json()['data']
        
        
        return [Subscription.serialize_from_json(x) for x in data['subscriptions']] if 'subscriptions' in data else []
    
    
    @staticmethod
    def get_timeline_stream(core, resource, limit, until, since):
        url = PersonalizedStreamsClient.STREAM_BASE_URL + PersonalizedStreamsClient.TIMELINE_PATH
        headers = get_lf_token_header(core)
        params = {'resource': resource, 'limit': limit}
        if until is not None:
            params['until'] = until
        elif since is not None:
            params['since'] = since

        return requests.get(url, params = params, headers = headers).json()
    