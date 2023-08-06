from pathlib import Path
import importlib
import glob
import pysquid.plugin


class PluginCollector():

    def __init__(self, paths: list = [Path('plugins')]):

        self.paths = set()
        self.pyfiles = set()
        self.pymodules = set()
        self.get_paths(paths)
        self.get_py_files()

    def get_paths(self, paths):
        
        for path in paths:

            if not isinstance(path, Path):
                continue

            if not path.exists():
                continue

            if not path.is_dir():
                continue

            self.paths.add(path)

    def get_py_files(self):

        all_files = set()

        for path in self.paths:
            files = set(glob.glob(str(path) + '/**/*.py', recursive=True))
            all_files = all_files.union(files)

        self.pyfiles = all_files

        pymodules = [f.replace('/', '.')[:-3] for f in self.pyfiles]
        self.pymodules = [f.strip('.__init__') for f in pymodules]

    def collect(self):

        plugins = {}

        for module in self.pymodules:

            imported_module = importlib.import_module(module)

            for export in imported_module.EXPORTS:

                ti = export()

                if isinstance(ti, pysquid.plugin.Plugin):
                    plugins[ti.plugin_id] = export

        return plugins
        
        
            
