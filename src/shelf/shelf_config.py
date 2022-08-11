from configparser import ConfigParser

config_object = ConfigParser()

<<<<<<< HEAD
config_object.read("/home/studs/PycharmProjects/goodreads-scraper/config.ini")
=======
config_object.read("/Users/daniel/PycharmProjects/carver/config.ini")
>>>>>>> b2ba7b2 (migrate to new machine)

# SHELF

config_number_of_shelf_results = config_object["BOOK"].getint("NUMBER_OF_SHELF_RESULTS")
