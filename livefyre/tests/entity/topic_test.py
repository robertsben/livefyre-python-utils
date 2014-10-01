import unittest

from livefyre.tests import LfTest
from livefyre.src.entity.topic import Topic

try:
    import simplejson as json
except ImportError:
    import json


class TopicTestCase(LfTest, unittest.TestCase):
    ID = 'id'
    LABEL = 'label'
    CREATED_AT = 10
    MODIFIED_AT = 100
    DICT = {'id': ID, 'label': LABEL, 'createdAt': CREATED_AT, 'modifiedAt': MODIFIED_AT}
    
    def test_init(self):
        topic = Topic(self.ID, self.LABEL, self.CREATED_AT, self.MODIFIED_AT)
        self.assertEquals(self.ID, topic.topic_id)
        self.assertEquals(self.LABEL, topic.label)
        self.assertEquals(self.CREATED_AT, topic.created_at)
        self.assertEquals(self.MODIFIED_AT, topic.modified_at)
        
    def test_func(self):
        topic = Topic(self.ID, self.LABEL, self.CREATED_AT, self.MODIFIED_AT)
        self.assertEquals(self.DICT, topic.to_dict())
        
        topic2 = Topic.serialize_from_json(self.DICT)
        self.assertEquals(self.ID, topic2.topic_id)
        self.assertEquals(self.LABEL, topic2.label)
        self.assertEquals(self.CREATED_AT, topic2.created_at)
        self.assertEquals(self.MODIFIED_AT, topic2.modified_at)
        
        topic3 = json.dumps(topic2)
        self.assertEquals(json.dumps(self.DICT), topic3)
        
        
if __name__ == '__main__':
    unittest.main()
