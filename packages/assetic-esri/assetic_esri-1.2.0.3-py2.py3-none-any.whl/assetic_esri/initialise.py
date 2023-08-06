from __future__ import absolute_import

from assetic.tools.shared import InitialiseBase
from . import Config
from .__version__ import __version__
from .tools.esri_messager import EsriMessager


class Initialise(InitialiseBase):
    def __init__(self, configfile=None, inifile=None, logfile=None, loglevelname=None):
        # initialise obejct here with all of the values we need
        conf = Config()
        conf.messager = EsriMessager()
        conf.xmlconfigfile = configfile
        conf.inifile = inifile
        conf.logfile = logfile
        conf.loglevelname = loglevelname

        super(Initialise, self).__init__(__version__, config=conf)
