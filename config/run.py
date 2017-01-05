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
  
  return parser

def handleArgs(parsedArgs):
  args = parsedArgs
  config = Config()
  ADD_ARG = "add"
  DELETE_ARG = "del"

  if args.makeconfig == True:
    config.makeConfigFile()

  if args.mongo != None:
    if args.port != None and \
        args.uri != None and \
        args.db  != None:
      if args.mongo == ADD_ARG:
        config.addMongoDatabase(args.uri, args.port, args.db)
        print("Successfully Added!")
      elif args.mongo == DELETE_ARG:
        config.deleteMongoDatabase(args.uri, args.port, args.db)
        print("Successfully Removed!")
    else:
      parse.error("--mongo usage: [-uri] [-p] [-db]")
      exit(1)
  
  if args.gmapskey == ADD_ARG and args.key != None:
    config.addGoogleMapsKey(args.key)
  elif args.gmapskey == DELETE_ARG:
    config.deleteGoogleMapsKey()
        
  if args.secret == ADD_ARG and args.token != None:
    config.addTokenSecretKey(args.token)
  elif args.secret == DELETE_ARG:
    config.deleteTokenSecretKey()


if __name__ == "__main__":
  handleArgs(args().parse_args())
