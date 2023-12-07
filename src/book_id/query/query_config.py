from configparser import ConfigParser

config_object = ConfigParser()

config_object.read("/Users/daniel/PycharmProjects/carver/config.ini")

# QUERY

config_delimiter = config_object["QUERY"].get("DELIMITER")
