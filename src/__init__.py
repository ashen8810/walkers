# src/__init__.py

import glob
import os
import importlib

# Dynamically import all Python files in the src folder
module_files = glob.glob(os.path.join(os.path.dirname(__file__), '*.py'))

# Exclude the __init__.py file itself
module_files = [f for f in module_files if '__init__.py' not in f]

# Import all functions from each module
for module_file in module_files:
    module_name = os.path.splitext(os.path.basename(module_file))[0]
    module = importlib.import_module(f".{module_name}", package="src")
    
    # Optionally, import all functions from each module into the namespace
    globals().update({name: getattr(module, name) for name in dir(module) if not name.startswith('_')})
