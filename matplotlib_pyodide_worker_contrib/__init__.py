from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("matplotlib_pyodide_worker_contrib")
except PackageNotFoundError:
    # package is not installed
    pass
