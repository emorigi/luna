from pysnmp.hlapi import *
from pprint import pprint
from inspect import getmembers

g = getCmd(SnmpEngine(),
CommunityData('public'),
    UdpTransportTarget(('192.168.2.1', 161)),
    ContextData(),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.31.1.1.1.6.3')))

errorIndication, errorStatus, errorIndex, varBinds=next(g)
if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    bytein=varBinds[0][1].prettyPrint()

print("in=|"+bytein+"|")

# definisco un po' di costanti così come suggeriscono le best practice di home assistant
# configuro quali parametri sono opzionali e quali richiesti
#    name: Internet
#    oidin: 1.3.6.1.2.1.31.1.1.1.6.3
#    oidout: 1.3.6.1.2.1.31.1.1.1.10.3
#    community: 'public'
#    unit_of_measurement: "bps"
#    version: '2c'
#    scan_interval: 10
#    host: 192.168.2.1
#bytes-in=.1.3.6.1.2.1.31.1.1.1.6.3 
#bytes-out=.1.3.6.1.2.1.31.1.1.1.10.3
