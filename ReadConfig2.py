import configparser
import os

def getSQLCONFIG (filename):
     cf = configparser.ConfigParser ()
     cf.read (filename) #Read configuration file
     # Read corresponding file parameters
     _database = cf.get ("Database1", "database")
     _server = cf.get ("Database1", "server")
     _trusted = cf.get ("Database1", "trustedconnection")


     return _database, _server, _trusted #return required parameters







