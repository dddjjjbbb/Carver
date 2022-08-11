from configparser import ConfigParser

config_object = ConfigParser()

<<<<<<< HEAD
config_object.read("/home/studs/PycharmProjects/goodreads-scraper/config.ini")
=======
config_object.read("/Users/daniel/PycharmProjects/carver/config.ini")
>>>>>>> b2ba7b2 (migrate to new machine)

# QUERY

config_delimiter = config_object["QUERY"].get("DELIMITER")
