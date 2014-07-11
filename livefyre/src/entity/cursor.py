import dateutil
from livefyre.src.api.personalizedstreams import PersonalizedStreamsClient


class TimelineCursor(object):
    def __init__(self, core, resource, limit, start_time):
        self.core = core
        self.resource = resource
        self.limit = limit
        self.cursor_time = start_time
        self.next = False
        self.previous = False
        
    def next(self, limit = None):
        if limit is None:
            limit = self.limit
            
        data = PersonalizedStreamsClient.get_timeline_stream(self.core, self.resource, limit, None, self.cursor_time.isoformat())
        cursor = data['meta']['cursor']
        
        self.next = cursor['hasNext']
        self.previous = cursor['next'] is not None
        
        self.cursor_time = dateutil.parser(cursor['next']) if self.previous else self.cursor_time

        return data
        
    def previous(self, limit = None):
        if limit is None:
            limit = self.limit
        
        import pdb;pdb.set_trace()
        
        data = PersonalizedStreamsClient.get_timeline_stream(self.core, self.resource, limit, self.cursor_time.isoformat(), None)
        cursor = data['meta']['cursor']
        
        self.previous = cursor['hasPrev']
        self.next = cursor['prev'] is not None
        
        self.cursor_time = dateutil.parser(cursor['prev']) if self.next else self.cursor_time

        return data