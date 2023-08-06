import inspect, json, logging, re, sys


def pobj(obj):
    r = t_obj = size_obj = p_obj = None
    try:
        # print('---type---', type(obj).__name__ )
        t_obj = str(type(obj).__name__)
        size_obj = sys.getsizeof(obj)
        size_obj = size_obj / 1000
        frame = inspect.currentframe().f_back
        s = inspect.getframeinfo(frame).code_context[0]
        r = re.search(r"\((.*)\)", s).group(1)
        if t_obj in ['dict', 'ReturnDict']:
            p_obj = json.dumps(obj, indent=2, sort_keys=True)
        elif t_obj in ['Request', 'WSGIRequest', 'SessionStore']:
            p_obj = vars(obj)
        else:
            p_obj = obj
    except:
        pass
    finally:
        print('\n\n---{}---type:{}---size:{}-KB---\n{}'.format(r, t_obj, size_obj, p_obj))


def pobjl(logger_name: str, logger_level: str):
    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }

    logger = logging.getLogger(logger_name)
    console_handler = logging.StreamHandler()
    logger_formatter = logging.Formatter('\n[%(asctime)s] %(levelname)s - %(name)s - file: %(module)s - fun: %(funcName)s() - LN: %(lineno)d \n%(message)s')
    console_handler.setFormatter(logger_formatter)
    logger.addHandler(console_handler)
    LOGGER_LEVEL = levels.get(logger_level.lower(), 'warning')
    logger.setLevel(LOGGER_LEVEL)

    return logger