import os


class Settings:
    function_codes_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/functionCodes")
    model_cache_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/pyModel")
