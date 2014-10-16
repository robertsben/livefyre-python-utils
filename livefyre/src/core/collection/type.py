from enum import Enum


class CollectionType(Enum):
    COUNTING = 'counting'
    LIVEBLOG = 'liveblog'
    LIVECHAT = 'livechat'
    LIVECOMMENTS = 'livecomments'
    RATINGS = 'ratings'
    REVIEWS = 'reviews'
    SIDENOTES = 'sidenotes'

    def __init__(self, ctype):
        self.ctype = ctype
        
    def __str__(self):
        return self.ctype