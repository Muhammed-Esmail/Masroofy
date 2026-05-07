import os
import sys
import django
from pathlib import Path
from pdoc import pdoc, doc

# 1. Setup Environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Ensure Python can find your apps inside src/backend
root_path = Path(__file__).parent
src_path = root_path / "src" / "backend"
sys.path.append(str(src_path))

# 2. Initialize Django
django.setup()

# 3. Define modules
modules = [
    "cycle", 
    "expenses", 
    "history", 
    "insights", 
    "login", 
    "transaction", 
    "userSettings"
]

def hide_clutter():
    """
    Tells pdoc to ignore migrations, tests, and admin files 
    to keep the sidebar clean.
    """
    for mod_name in modules:
        # doc.Module.from_name finds the module object
        m = doc.Module.from_name(mod_name)
        # We set __pdoc__ dynamically
        m.pdoc_attributes = {
            "migrations": False,
            "tests": False,
            "admin": False,
            "apps": False,
        }

if __name__ == "__main__":
    # Specify the output directory as a Path object
    output_path = root_path / "docs_pdoc"
    
    # Run pdoc
    pdoc(*modules, output_directory=output_path)
    
    print(f"✅ Documentation successfully generated at: {output_path.absolute()}")