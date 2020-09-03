import re


def checkip(hostip):
    pat = re.compile(r'([0-9]{1,3})\.')
    r = re.findall(pat, hostip + ".")
    if len(r) == 4 and len([x for x in r if int(x) >= 0 and int(x) <= 255]) == 4:
        return True
    else:
        return False


def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False


print(isIP('0.0.0.0'))
