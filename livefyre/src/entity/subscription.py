from enum import Enum

try:
    import simplejson as json
except ImportError:
    import json


class Subscription(object):
    def __init__(self, to, by, sub_type, created_at=None):
        self.to = to
        self.by = by
        self.sub_type = sub_type
        if created_at:
            self.created_at = created_at
        
    @staticmethod
    def serialize_from_json(json_obj):
        return Subscription(json_obj['to'], json_obj['by'], json_obj['type'], json_obj['createdAt'])
    
    def to_dict(self):
        sub_dict = {
            'to': self.to,
            'by': self.by,
            'type': self.sub_type.name,
        }
        
        if hasattr(self, 'created_at'):
            sub_dict['createdAt'] = self.created_at
        return sub_dict
        
    #json hack to get around jwt json dumps
    def _json_support(*args):
        def default(self, o):
            return o.to_dict()
        json.JSONEncoder.default = default
    _json_support()

        
class SubscriptionType(Enum):
    personalStream = 1