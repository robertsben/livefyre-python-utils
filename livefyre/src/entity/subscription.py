from enum import Enum


class Subscription(object):
    def __init__(self, to, by, sub_type, created_at = None):
        self.to = to
        self.by = by
        self.sub_type = sub_type
        self.created_at = created_at
        
    @staticmethod
    def serialize_from_json(json):
        return Subscription(json['to'], json['by'], json['type'], json['createdAt'])
    
    def to_dict(self):
        sub_dict = {
                'to': self.to,
                'by': self.by,
                'type': self.sub_type.name,
        }
        
        if self.created_at is not None:
            sub_dict['createdAt'] = self.created_at
        return sub_dict 
        
        
class SubscriptionType(Enum):
    personalStream = 1