"""

"""
import warnings

class BoundCheckError(BaseException):
    pass


class NewParamWarning(Warning):
    pass

class NoneWarning(Warning):
    pass

class AttrTypeNotFoundWarning(Warning):
    pass

warnings.simplefilter('always',NoneWarning)
warnings.simplefilter('always',AttrTypeNotFoundWarning)