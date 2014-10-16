from livefyre.src.utils.validator import Validator


class NetworkValidator(Validator):
    def validate(self, data):
        reason = ''
        
        if not hasattr(data, 'name'):
            reason += '\n name is missing.'
        elif not data.name.endswith('fyre.co'):
            reason += '\n name does not end in fyre.co.'
        
        reason += self.verify_attr(data, 'key')
        
        if len(reason) > 0:
            expl = 'Problems with your network input:' + reason
            raise AssertionError(expl)
        
        return data