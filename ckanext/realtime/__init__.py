# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)

SUCCESS_MESSAGE = 'SUCCESS'
FAIL_MESSAGE = 'FAIL'

YES_MESSAGE = 'YES'
NO_MESSAGE = 'NO'

NON_DATASTORE_MESSAGE = 'NOT-A-DATASTORE'
INVALID_RESOURCE_MESSAGE = 'INVALID-RESOURCE'