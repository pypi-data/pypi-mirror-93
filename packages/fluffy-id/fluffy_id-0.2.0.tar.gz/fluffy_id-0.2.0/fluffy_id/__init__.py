"""Top-level package for GUID Generator."""

__author__ = """Pyunghyuk Yoo"""
__email__ = 'yoophi@gmail.com'
__version__ = '0.2.0'

from fluffy_id.fluffy_id import gen_guid, parse_guid, get_datetime

__all__ = ["gen_guid", "parse_guid", "get_datetime", ]
