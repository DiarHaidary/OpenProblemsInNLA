import importlib.util,json,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location("ie05_harness",sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.validate_project(Path(sys.argv[2]));print(json.dumps(c,indent=2))
