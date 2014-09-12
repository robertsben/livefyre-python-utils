import base64, sys, hashlib, collections
import jwt, requests

from livefyre.src.utils import is_valid_full_url
from livefyre.src.api.domain import Domain
from livefyre.src.exceptions import LivefyreException

try:
    import simplejson as json
except ImportError:
    import json


def check_topics(network_urn, topics):
    if topics:
        for topic in topics:
            try:
                topic_id = topic.get_id()
                if topic_id.startswith(network_urn) and not topic_id.replace(network_urn, '?', 1).startswith(':site='):
                    return True
            except AttributeError:
                continue # not a topic!
    return False


class Collection(object):
    TYPE = ['reviews', 'sidenotes', 'ratings', 'counting', 'liveblog', 'livechat', 'livecomments']
    
    def __init__(self, site, article_id, title, url, options={}):
        assert is_valid_full_url(url), 'url must be a full domain. ie. http://livefyre.com'
        assert len(title) <= 255, "title's length should be under 255 char"
        
        if self.options:
            if 'type' in self.options and self.options['type'] not in self.TYPE:
                raise AssertionError('type is not a recognized type. must be in {0}'.format(self.TYPE))
            if 'topics' in self.options:
                self.network_issued = check_topics(site.network.get_urn(), self.options['topics'])

        self.site = site
        self.article_id = article_id
        self.title = title
        self.url = url
        self.options = options
    
    
    def create_or_update(self):
        response = self.__invoke_collection_api('create')
        if response.status_code == 200:
            self.collection_id = response.json()['data']['collectionId']
            return self
        if response.status_code == 409:
            response = self.__invoke_collection_api('update')
            if response.status_code == 200:
                return self
            raise LivefyreException('Error updating Livefyre collection. Status code: ' + response.status_code)
        raise LivefyreException('Error creating Livefyre collection. Status code: ' + response.status_code)

    
    def build_collection_meta_token(self):
        j = self.__get_json()
        if self.network_issued:
            j['iss'] = self.site.network.getUrn()
        
        return jwt.encode(j, self.site.network.key if self.network_issued else self.key)
    
    
    def build_checksum(self):
        j = self.__get_json()

        return hashlib.md5(str(json.dumps(info))).hexdigest()
    
    
    def get_collection_content(self, article_id):
        if sys.version_info >= (3, 0):
            article_bytes = bytes(str(article_id), 'utf-8')
        else:
            article_bytes = bytes(str(article_id))
        encoded_article_id = base64.b64encode(article_bytes).decode('utf-8')
        url = '{0}/bs3/{1}/{2}/{3}/init'.format(Domain.bootstrap(self), self.network.name, self.s_id, encoded_article_id)
        
        response = requests.get(url=url)
        if response.status_code == 200:
            return response.json()
        return None


    def build_livefyre_token(self):
        return self.site.build_livefyre_token()


    def get_urn(self):
        return self.site.get_urn() + ":collection=" + self.s_id
    

    def __invoke_collection_api(self, method):
        uri = '{0}/api/v3.0/site/{1}/collection/{2}/'.format(Domain.quill(self), self.s_id, method)
        data = self.__get_payload()
        headers = {'Content-Type': 'application/json', 'Accepts': 'applicatio/json'}
            
        response = requests.post(uri, params={'sync':1}, data=json.dumps(data), headers=headers)
        return response
    
    
    def __get_json(self):
        d = {
            'articleId': self.article_id,
            'url': self.url,
            'title': self.title,
        }
        d.update(self.options)
        
        return collections.OrderedDict(sorted(d.items()))
    
    
    def __get_payload(self):
        return {
            'articleId': self.article_id,
            'collectionMeta': self.build_collection_meta_token(),
            'checksum': self.build_checksum(),
        }
