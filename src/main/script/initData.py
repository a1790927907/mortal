import os
import shutil

from src.main.globalSettings.config import Settings as globalSettings


def init_function_codes():
    function_codes_dir = os.path.dirname(globalSettings.function_codes_dir)
    if not os.path.exists(function_codes_dir):
        os.mkdir(function_codes_dir)
    for file_path, _, files in os.walk(os.path.join(os.path.dirname(__file__), "initialFunctionCodes")):
        for filename in files:
            function_code_filename = os.path.join(globalSettings.function_codes_dir, filename)
            if not os.path.exists(function_code_filename):
                shutil.copyfile(os.path.join(file_path, filename), function_code_filename)


def init_py_model():
    py_model_dir = os.path.dirname(globalSettings.model_cache_dir)
    if not os.path.exists(py_model_dir):
        os.mkdir(py_model_dir)


def init():
    init_function_codes()
    init_py_model()


if __name__ == '__main__':
    init()
