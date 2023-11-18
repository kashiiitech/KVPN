from config import *
from VPN.windscribe import Windscribe

windscribe = Windscribe(login,password)

# li= []

def Click(bol):
    if bol:
        windscribe.connect(rand=True)

    else:
        windscribe.disconnect()
    return

