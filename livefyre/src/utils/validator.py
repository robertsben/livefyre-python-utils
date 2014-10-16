class Validator(object):
    def verify_attr(self, data, name):
        return '\n {} is missing.'.format(name) if not hasattr(data, name) else ''