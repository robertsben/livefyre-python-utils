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
        return core.get_urn() + Topic.TOPIC_IDENTIFIER + str(topic_id)
    
    
    def get_truncated_id(self):
        return self.topic_id[self.topic_id.find(self.TOPIC_IDENTIFIER) + len(self.TOPIC_IDENTIFIER):]
    
    
    def to_dict(self):
        topic_dict = {
            'id': self.topic_id,
            'label': self.label,
        }
        
        if self.created_at is not None:
            topic_dict['createdAt'] = self.created_at
        if self.modified_at is not None:
            topic_dict['modifiedAt'] = self.modified_at
        return topic_dict