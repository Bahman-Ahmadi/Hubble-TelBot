from json import loads, dumps
from random import choice


class JSON:

  def __init__(self, key: str, filename: str = "users.json"):
    self.key, self.filename = key, filename
    self.db_all = loads(open(filename).read())
    self.db = self.db_all[key]

  def makeUID(self, existsIds: list, start_char: str, length: int = 10) -> str:
    choices = [
      *"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    ]
    selected = start_char + \
        "".join([choice(choices) for i in range(length - len(start_char))])
    while selected in existsIds:
      # make a new UID while this UID is exist in table
      selected = start_char + \
          "".join([choice(choices)
                  for i in range(length - len(start_char))])
    return selected

  def GET(self, innerKey: str):
    return self.db.get(str(innerKey))

  def POST(self, innerKey: str, innerValue: any):
    self.db[innerKey] = innerValue
    self.UPDATE()
    return innerValue

  def PUT(self, ID: str, innerKey: str, innerValue: any):
    try:
      ID = str(ID)
      Type = type(self.db[ID][innerKey])
      if Type is list:
        self.db[ID][innerKey].append(innerValue)
      elif Type in [str, int, float]:
        self.db[ID][innerKey] += innerValue
      else:
        self.db[ID][innerKey] = innerValue
    except KeyError:
      self.db[ID][innerKey] = innerValue
    self.UPDATE()
    return self.db[ID][innerKey]

  def DELETE(self, innerKey: str):
    # delete a dict from a main dict
    self.db.pop(innerKey)
    self.UPDATE()

  def REMOVE(self, innerKey: str, innerValue: str):
    # remove an item from a list from a main dict
    self.db[innerKey].remove(innerValue)
    self.UPDATE()

  def UPDATE(self):
    self.db_all[self.key] = self.db
    open(self.filename,
         'w').write(dumps(self.db_all, indent=4, ensure_ascii=False))


def NewUser(uid) -> dict:
  user = JSON('users').GET(uid)
  if user is None:
    # not exists
    user = JSON("users").POST(str(uid), {"quota": 1, "referrals": []})
  return user
