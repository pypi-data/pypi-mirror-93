import importlib

def __getattr__(name):
    try:
        lib = importlib.import_module(f"Crypto.Hash.{name.upper()}")
    except:
        raise AttributeError(f"Unknown attribute {name}")
    def func(data):
        return lib.new(data).digest()
    return func

def __hasattr__(name):
    try:
        importlib.import_module(f"Crypto.Hash.{name.upper()}")
        return True
    except:
        return False
