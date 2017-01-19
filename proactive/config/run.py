from config import Config
import argparse

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
      choices=["add", "del"]
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
      help="Add or delete a Google Maps API Key",
      dest="gmapskey",
      type=str,
      choices=["add", "del"]
  )
  parser.add_argument(
    "-k", "--key",
      help="A key",
      dest="key"
  )
  parser.add_argument(
    "-s", "--secret",
      help="Add or delete token secret to configuration file",
      dest="secret",
      type=str,
      choices=["add", "del"]
  )
  parser.add_argument(
    "-t", "--token",
      help="Token.",
      dest="token",
      type=str
  )
  parser.add_argument(
    "-r", "--read",
      help="Read from the configuration file, specifying the property or properties to read.",
      dest="read",
      nargs="*"
  )
  parser.add_argument(
    "-f", "--format",
      help="The out put format from read.",
      dest="format",
      default="raw",
      choices=["raw", "newline", "json"]
  )
  return parser


def printArgs(objectList, format="raw"):
  """
    Print a list of objects in the correct format.
    The formats are:
     - raw : Standard print.
     - newline: Each element on a newline.
     - json: Each element is readable json format.
  """
  if format == "newline":
    for el in objectList:
      print("%s\n" % el)
  elif format == "json":
    import json
    print("%s" % json.dumps(objectList, indent=2))
  else:
    print("%s" % objectList)

def handleArgs(parser):
  args = parser.parse_args()
  config = Config()
  ADD_ARG = "add"
  DELETE_ARG = "del"

  # Make config args
  if args.makeconfig == True:
    config.makeConfigFile()
  
  # Mongo Args
  if args.mongo == ADD_ARG:
    if args.port != None and \
        args.uri != None and \
        args.db != None:
      config.addMongoDatabase(args.uri, args.port, args.db)
      print("Successfully Added!")
    else:
      parser.error("--mongo usage: [-uri] [-p] [-db]")
      exit(1)
  elif args.mongo == DELETE_ARG:
    config.deleteMongoDatabase(args.uri, args.port, args.db)
    print("Successfully Removed!")
  
  
  # Google Maps Args
  if args.gmapskey == ADD_ARG and args.key != None:
    config.addGoogleMapsKey(args.key)
  elif args.gmapskey == DELETE_ARG:
    config.deleteGoogleMapsKey()

  # Token Secret Args      
  if args.secret == ADD_ARG and args.token != None:
    config.addTokenSecretKey(args.token)
  elif args.secret == DELETE_ARG:
    config.deleteTokenSecretKey()

  # Read arg.
  if args.read != None:
    props = config.read(args.read)
    if (props != None): printArgs(props, args.format)

if __name__ == "__main__":
  handleArgs(args())
