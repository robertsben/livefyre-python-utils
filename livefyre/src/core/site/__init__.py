from livefyre.src.core.collection import Collection
from livefyre.src.core.collection.type import CollectionType
from .model import SiteData
from .validator import SiteValidator

class Site(object):
    def __init__(self, network, data):
        self.network = network
        self.data = data
        
    @staticmethod
    def init(network, site_id, key):
        data = SiteData(site_id, key)
        return Site(network, SiteValidator().validate(data))
    
    def build_livecomments_collection(self, title, article_id, url):
        return self.build_collection(CollectionType.LIVECOMMENTS, title, article_id, url)
    
    def build_liveblog_collection(self, title, article_id, url):
        return self.build_collection(CollectionType.LIVEBLOG, title, article_id, url)
        
    def build_livechat_collection(self, title, article_id, url):
        return self.build_collection(CollectionType.LIVECHAT, title, article_id, url)
    
    def build_counting_collection(self, title, article_id, url):
        return self.build_collection(CollectionType.COUNTING, title, article_id, url)
    
    def build_ratings_collection(self, title, article_id, url):
        return self.build_collection(CollectionType.RATINGS, title, article_id, url)
    
    def build_reviews_collection(self, title, article_id, url):
        return self.build_collection(CollectionType.REVIEWS, title, article_id, url)
    
    def build_sitenotes_collection(self, title, article_id, url):
        return self.build_collection(CollectionType.SIDENOTES, title, article_id, url)
    
    def build_collection(self, ctype, title, article_id, url):
        return Collection.init(self, ctype, title, article_id, url)
    
    @property
    def urn(self):
        return self.network.urn + ':site=' + self.data.site_id
