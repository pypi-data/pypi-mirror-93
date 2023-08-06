#Builder

#Builder Error happens when builder is having a wrong mode
class BuilderError(Exception):
    def __init__(self,msg):
        self.msg=msg

def Builder(**kwargs):
    args=dict(**kwargs)
    if args['mode'] == "Kivy":
        if args['ext'] == '.kv':
            file=args['file']
        else:
            raise BuilderError('Invalid Mode or Extension found!')
    else:
        raise BuilderError('Invalid Mode or Extension found!')
    return file