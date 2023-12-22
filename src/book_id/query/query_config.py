from configparser import ConfigParser

config_object = ConfigParser()

config_object.read("config.ini")

# QUERY

config_delimiter = config_object["QUERY"].get("DELIMITER")
