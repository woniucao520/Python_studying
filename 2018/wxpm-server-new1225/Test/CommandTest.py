from Commands.Command import Command
import json


tmp = b'{"cmd": "CMD_USER_BUY", "args": {"USER_ID": "1","P_NO": "730002", "PRICE": "234", "MONEY": "2342", "MAX_VOLUME": "23423", "VOLUME": "10"}}'

cmd = Command.process(tmp)

print(type(cmd))
print(type(cmd['args']))