try:
    # Declare this a namespace package if pkg_resources is available.
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    pass
