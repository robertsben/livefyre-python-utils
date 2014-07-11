try:
    import simplejson as json
except ImportError:
    import json
    

class Topic(object):
    TOPIC_IDENTIFIER = ':topic='
    
    def __init__(self, topic_id, label, created_at = None, modified_at = None):
        self.topic_id = topic_id
        self.label = label
        self.created_at = created_at
        self.modified_at = modified_at
    
    @staticmethod
    def serialize_from_json(json):
        return Topic(json['id'], json['label'], json['createdAt'], json['modifiedAt'])
    
    @staticmethod
    def create(core, topic_id, label):
        return Topic(Topic.generate_urn(core, topic_id), label)
    
    @staticmethod
    def generate_urn(core, topic_id):
        return core.get_urn() + Topic.TOPIC_IDENTIFIER + topic_id
    
    def get_truncated_id(self):
        return self.topic_id[self.topic_id.find(self.TOPIC_IDENTIFIER) + len(self.TOPIC_IDENTIFIER):]
    
    def serialize_to_json(self):
        return {
                'id': self.topic_id,
                'label': self.label,
                'createdAt': self.created_at,
                'modifiedAt': self.modified_at
            }


class Subscription(object):
    def __init__(self, to, by, sub_type, created_at):
        self.to = to
        self.by = by
        self.sub_type = sub_type
        self.created_at = created_at
        
    @staticmethod
    def serialize_from_json(json):
        return Subscription(json['to'], json['by'], json['type'], json['createdAt'])
    
    def serialize_to_json(self):
        return {
                'to': self.to,
                'by': self.by,
                'type': self.sub_type,
                'createdAt': self.created_at,
            }
        
        
class SubscriptionType(object):
    personalStream = range(1)