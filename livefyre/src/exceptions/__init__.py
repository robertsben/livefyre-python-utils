class LivefyreException(Exception):
    pass
    

class ApiException(LivefyreException):
    def __init__(self, message):
        super(ApiException, self).__init__(message)


# 'Livefyre appears to be down. Please see status.livefyre.com or contact us for more information')
#         raise LivefyreException('Please check the contents of your request. Here is the response from our servers: ' + str(response.content))