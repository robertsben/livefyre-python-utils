from livefyre.src.core.collection import Collection

class Site(object):
    def __init__(self, network, site_id, key):
        self.network = network
        self.site_id = site_id
        self.key = key
    
    
    def build_collection(self, title, article_id, url, options={}):
        return Collection(self, title, article_id, url, options)
    

    def build_livefyre_token(self):
        return self.network.build_livefyre_token()


    def get_urn(self):
        return self.network.get_urn() + ':site=' + self.site_id
