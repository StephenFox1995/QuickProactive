import os
import json
import argparse
import subprocess


class Config(object):
  """
    Class to edit configuration file.
  """

  _CONFIG_FILENAME = "config.json"
  _CONFIG_FILE_PATH = "/etc/quick/%s" % _CONFIG_FILENAME
  _CONFIG_DIR = "/etc/quick/"
  _MONGO_OBJECT_NAME = "mongodb"
  _MONGO_DATABASES = "databases"
  _GMAPS = "gmaps"
  _TOKEN = "token"
  _FILE_TEMPLATE = {"databases": [] }
  
  @staticmethod
  def checkRoot():
    """
      Ensures that the user currently executing is the root user.
      @throws If not the root an exception is thrown
    """
    if os.getuid() != 0:
      raise Exception("Must be executed with root privileges.")

  def makeConfigFile(self):
    """
     Creates the configuration file where settings and configurations
     are stored.
    """
    Config.checkRoot()
    if not os.path.exists(self._CONFIG_DIR):
      os.mkdir(self._CONFIG_DIR)

    # Let user know that this configration file already exists
    # and that proceeding will overwrite the current configuration
    if os.path.exists(self._CONFIG_FILE_PATH):
      print("%s already exists. Overwrite? y/n" % self._CONFIG_FILE_PATH)
      response = raw_input()
      if response != "y":
        return
      print("Overwriting... %s" % self._CONFIG_FILE_PATH)
    with open(self._CONFIG_FILE_PATH, "w+") as fp:
      json.dump(self._FILE_TEMPLATE, fp, indent=2)
      print("Configuration file successfully created.")


  def addMongoDatabase(self, uri, port, database):
    """
      Adds basic details for a Mongo database to the configuration file.

      @param uri:(str) The URI to find the database.

      @param port:(int) The port the MongoDB instance is running on.

      @param database:(str) The name of the database to connect to.
    """
    fileContents = self.__readConfigFile()
    newDatabase = { "uri": uri, "port": port, "database": database }
    fileContents[self._MONGO_DATABASES].append(newDatabase)
    self.__writeConfigFile(fileContents)
  
  def removeMongoDatabase(self, uri, port, database):
    """
      Removes details for a database, from the databases list in the
      configuration file.

      @param uri:(str) The database uri.
      @param port:(int) The port.
      @param database:(str) The name of the database.
    """
    fileContents = self.__readConfigFile()
    databases = fileContents[self._MONGO_DATABASES]
    dbToCheck = { "uri": uri, "port": port, "database": database }
    for (i, value) in enumerate(databases):
      if (self.__dbCompare(databases[i], dbToCheck)):
        del databases[i]
    print(databases)

    fileContents[self._MONGO_DATABASES] = databases
    self.__writeConfigFile(fileContents)

  def __dbCompare(self, db1, db2):
    """
      Compares the details of two databases, to check if they are the same.
    """
    if db1["uri"] == db2["uri"] and \
        db1["port"] == db2["port"] and \
        db1["database"] == db2["database"]:
      return True
    else:
      return False


  def addGoogleMapsKey(self, key):
    """
      Adds a Google Maps API key to the configuration file.

      @param key:(str) The Google Maps API key to add to the configuration file.
    """
    fileContents = self.__readConfigFile()
    newKey = { "key": key }
    fileContents[self._GMAPS] = newKey
    self.__writeConfigFile(fileContents)

  
  def addTokenSecretKey(self, secret):
    """
      Adds the token secret to the configuration file.

      @param secret:(str) The token secret key.
    """
    fileContents = self.__readConfigFile()
    newTokeSecret = {"secret": secret}
    fileContents[self._TOKEN] = newTokeSecret
    self.__writeConfigFile(fileContents)


    
  def __readConfigFile(self):
    """
      Read from the configuration file defined by __CONFIG_FILE_PATH.
    """
    with open(self._CONFIG_FILE_PATH) as file:
      return json.load(file)
      

  def __writeConfigFile(self, contents):
    """
      Write to the configuration file defined by __CONFIG_FILE_PATH.
      Note: must have root priveleges.
    """
    Config.checkRoot()
    with open(self._CONFIG_FILE_PATH, "w+") as fp:
      contents = json.dumps(contents, indent=2, sort_keys=True)
      fp.write(contents)

      
    

def args():
  parser = argparse.ArgumentParser("Confiration file util")
  parser.add_argument(
    "-mk", "--make",
      help="Make the configuration file at /etc/quick/config.",
      dest="makeconfig",
      type=bool,
      default=False
  )
  parser.add_argument(
    "-m", "--mongo",
      help="Add or delete a MongoDB from config file, format: [-uri] [-p] [-db]",
      dest="mongo",
      choices=["add", "delete"]
  )
  parser.add_argument(
    "-u", "--uri",
      help="URI for new Mongo database",
      dest="uri",
      type=str
  )
  parser.add_argument(
    "-p", "--port",
      help="Port for new Mongo database",
      dest="port",
      type=int
      
  )  
  parser.add_argument(
    "-d", "--db",
      help="The Mongo database name",
      dest="db",
      type=str
  )
  parser.add_argument(
    "-g", "--gmapskey",
      help="Adds a Google Maps API Key",
      dest="gmapskey",
      type=str
  )
  parser.add_argument(
    "-t", "--token",
      help="Add token secrey to configuration file",
      dest="tokenSecret",
      type=str
  )
  return parser

def handleArgs(parsedArgs):
  args = parsedArgs
  config = Config()

  if args.makeconfig == True:
    config.makeConfigFile()

  if args.mongo != None:
    if args.port != None and \
        args.uri != None and \
        args.db  != None:
      if args.mongo == "add":
        config.addMongoDatabase(args.uri, args.port, args.db)
        print("Successfully Added!")
      elif args.mongo == "delete":
        config.removeMongoDatabase(args.uri, args.port, args.db)
        print("Successfully Removed!")
    else:
      parse.error("--mongo usage: [-uri] [-p] [-db]")
      exit(1)

  if args.gmapskey != None:
    config.addGoogleMapsKey(args.gmapskey)
        
  if args.tokenSecret != None:
    config.addTokenSecretKey(args.tokenSecret)


if __name__ == "__main__":
  handleArgs(args().parse_args())
