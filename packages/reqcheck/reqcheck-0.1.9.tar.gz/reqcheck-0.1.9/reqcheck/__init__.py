import logging
import pkg_resources


__version__ = pkg_resources.get_distribution('reqcheck').version


logger = logging.getLogger('reqcheck')
