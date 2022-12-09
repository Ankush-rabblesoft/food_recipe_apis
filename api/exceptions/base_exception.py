class IException(Exception):
    def __init__(self, *args):
        super(Exception, self).__init__(*args)
        