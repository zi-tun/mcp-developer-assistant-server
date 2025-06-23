import configparser
import properties as properties
import importlib.resources as pkg_resources
import logging
logger = logging.getLogger(__name__)


class MyParser(configparser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop("__name__", None)
        return d

def collect_property_file_contents(section_name, file_name="config.ini"):
    """
     This method will attempt to open and load the config file
    :param file_name:
    :param section_name: The name of the section needed from the config file
    :return:
    """
    config_path = ""
    try:
        parser = MyParser()
        parser.read_file(pkg_resources.open_text(properties, file_name))
        content = MyParser.as_dict(parser)
        return content[section_name.upper()]

    except Exception as e:
        logger.error(
            f"ERROR: Unable to open and collect property file contents for"
            f"(property file: {config_path} account: {section_name})"
        )
        logger.error(f"ERROR: {repr(e)}")
