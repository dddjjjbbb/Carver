from configparser import ConfigParser

config_object = ConfigParser()


config_object.read("config.ini")

# LIST

config_number_of_list_results = config_object["BOOK"].getint("NUMBER_OF_LIST_RESULTS")
