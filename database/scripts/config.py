from configparser import ConfigParser
import os
# https://www.postgresqltutorial.com/postgresql-python/connect/#:~:text=To%20connect%20to%20the%20suppliers,instance%20of%20the%20connection%20class.&text=The%20following%20is%20the%20list,that%20you%20want%20to%20connect.
"""
config.py is used to connect to a postgreSQL database.The database.ini file
contains your database connection parameters. The database.ini in the project
directory is only an example.  Like the yaml file, please reference the actual
file in the super directory

"""

'''
def load_config(section='postgresql'):
    wd = os.getcwd()
    # Get path of super directory
    parent_path = os.path.abspath(os.path.join(wd, os.pardir))
    filename = parent_path + "/" + "database.ini"
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config
'''

# hardcoded version of above code, in order to specify path if used anywhere else
def load_config(filename="database.ini", section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # Get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file.")

    return config
