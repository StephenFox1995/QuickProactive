from travel import Travel
from coord import coordinate
from key import KEY

if __name__ == "__main__":
  businessLocation = coordinate(53.3469158, -6.279328200000009)
  userLocation = coordinate(53.34750503535324, -6.274092528002939)

  travel = Travel(KEY)
  print(travel.find(businessLocation, userLocation, find="duration"))
  print(travel.find(businessLocation, userLocation, find="distance"))