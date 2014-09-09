import base64, sys, hashlib, collections
import jwt, requests

from livefyre.src.utils import is_valid_full_url
from livefyre.src.api.domain import Domain
from livefyre.src.exceptions import LivefyreException

try:
    import simplejson as json
except ImportError:
    import json


class Collection(object):
    TYPE = ['reviews', 'sidenotes', 'ratings', 'counting', 'liveblog', 'livechat', 'livecomments']
    
    def __init__(self, site, article_id, title, url, options={}):
        assert is_valid_full_url(url), 'url must be a full domain. ie. http://livefyre.com'
        assert len(title) <= 255, "title's length should be under 255 char"
        
        if 'type' in self.options and self.options['type'] not in self.TYPE:
            raise AssertionError('type is not a recognized type. must be in {0}'.format(self.TYPE))

        self.site = site
        self.article_id = article_id
        self.title = title
        self.url = url
        self.options = options
    
    
    def create_or_update(self):
        response = self.invoke_collection_api('create')
        
        if response.status_code == 200:
            self.collection_id = response.json()['data']['collectionId']
            return
        if response.status_code == 409:
            response = self.invoke_collection_api('update')
            if response.status_code == 200:
                return self
            raise LivefyreException('Error updating Livefyre collection. Status code: ' + response.status_code)
        raise LivefyreException('Error creating Livefyre collection. Status code: ' + response.status_code)


    def get_json(self):
        d = {
            'articleId': self.article_id,
            'url': self.url,
            'title': self.title,
        }
        d.update(self.options)
        
        return collections.OrderedDict(sorted(d.items()))
    
    
    def get_payload(self):
        return {
            'articleId': self.article_id,
            'collectionMeta': self.build_collection_meta_token(),
            'checksum': self.build_checksum(),
        }
        
    
    def invoke_collection_api(self, method):
        uri = '{0}/api/v3.0/site/{1}/collection/{2}/'.format(Domain.quill(self), self.s_id, method)
        data = self.get_payload()
        headers = {'Content-Type': 'application/json', 'Accepts': 'application/json'}
            
        response = requests.post(uri, params={'sync':1}, data=json.dumps(data), headers=headers)
        return response
    
    
    def build_collection_meta_token(self):
        j = self.get_json()
        if self.network_issued:
            j['iss'] = self.site.network.getUrn()
        
        return jwt.encode(j, self.key)
    
    
    def build_checksum(self):
        meta_string = '{{"tags":"{0}","title":"{1}","url":"{2}"}}'.format(self.tags, self.title, self.url)

        return hashlib.md5(meta_string).hexdigest()
    
    
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


    def get_collection_id(self, article_id):
        json = self.get_collection_content(article_id)
        if json:
            return json['collectionSettings']['collectionId']
        return None
    
    
    def build_livefyre_token(self):
        return self.site.build_livefyre_token()


    def get_urn(self):
        return self.site.get_urn() + ":collection=" + self.s_id
