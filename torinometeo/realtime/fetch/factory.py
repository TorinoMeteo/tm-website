import importlib


def parser_factory(type):
    """ Factory method to retrieve the parse class to be used with
        contents formatted as type

        WTF! Why the whitelist?
        To avoid auto import of modules, security is serius business.
    """
    path = '.parsers.%s'
    whitelist = ['txtwd', 'sintpi', 'clientraw', 'unito', 'weatherlink', 'aprs', 'realtime', 'txtmp', 'tm']
    if type in whitelist:
        mod = importlib.import_module(
            path % type, __name__.rsplit('.', 1)[0]
        )
        return getattr(mod, type[0].upper() + type[1:] + 'Parser')
