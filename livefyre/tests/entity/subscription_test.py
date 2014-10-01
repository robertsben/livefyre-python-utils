import unittest, pytest

from livefyre.tests import LfTest
from livefyre.src.entity.subscription import Subscription, SubscriptionType

try:
    import simplejson as json
except ImportError:
    import json


@pytest.mark.unit
class SubscriptionTestCase(LfTest, unittest.TestCase):
    TO = 'to'
    BY = 'by'
    TYPE = SubscriptionType.personalStream
    CREATED_AT = 10
    DICT = {'to': TO, 'by': BY, 'type': TYPE.name, 'createdAt': CREATED_AT}
    
    def test_init(self):
        sub = Subscription(self.TO, self.BY, self.TYPE, self.CREATED_AT)
        self.assertEquals(self.TO, sub.to)
        self.assertEquals(self.BY, sub.by)
        self.assertEquals(self.TYPE, sub.sub_type)
        self.assertEquals(self.CREATED_AT, sub.created_at)
        
    def test_func(self):
        sub = Subscription(self.TO, self.BY, self.TYPE, self.CREATED_AT)
        self.assertEquals(self.DICT, sub.to_dict())
        
        sub2 = Subscription.serialize_from_json(self.DICT)
        self.assertEquals(self.TO, sub2.to)
        self.assertEquals(self.BY, sub2.by)
        self.assertEquals(self.TYPE, sub2.sub_type)
        self.assertEquals(self.CREATED_AT, sub2.created_at)
        
        sub3 = json.dumps(sub2)
        self.assertEquals(json.dumps(self.DICT), sub3)
        
        
if __name__ == '__main__':
    unittest.main()
