from livefyre.src.utils import pyver


if pyver < 2.7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict


class CollectionData(object):
    def __init__(self, ctype, title, article_id, url):
        self.ctype = ctype
        self.article_id = article_id
        self.title = title
        self.url = url
        self.collection_id = 'Call create_or_update() on the collection to set the collection id.'
        
    def as_map(self):
        attr = self.__dict__.copy()
        attr['type'] = self.ctype.value
        attr['articleId'] = self.article_id
        attr.pop('ctype', None)
        attr.pop('article_id', None)
        attr.pop('collection_id', None)
        
        return OrderedDict(sorted(attr.items()))
