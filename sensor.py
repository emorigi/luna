import logging
import voluptuous as vol
from pysnmp.hlapi import *

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_UNIT_OF_MEASUREMENT
import homeassistant.util.dt as dt_util
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

# icona che rappresenta il sensore
ICON = "mdi:brightness-3"

# definisco un po' di costanti così come suggeriscono le best practice di home assistant
CONF_OID = "oid"
CONF_HOST = "host"
CONF_COMMUNITY = "community"
CONF_VERSIONE = "version"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_UNIT_OF_MEASUREMENT = "unit_of_measurement"
CONF_ICON = "icon"
DEFAULT_NAME = "Moon_IN"
DEFAULT_OID = "1.3.6.1.2.1.31.1.1.1.6.2"
DEFAULT_HOST = ""
DEFAULT_COMMUNITY = "public"
DEFAULT_VERSIONE = "2c"
DEFAULT_SCAN_INTERVAL = "10"
DEFAULT_UNIT_OF_MEASUREMENT="Bps"
DEFAULT_ICON = "mdi:upload"

def interroga_snmp (parametri):
    oggetto=getCmd(SnmpEngine(),
        CommunityData(parametri[CONF_COMMUNITY]),
        UdpTransportTarget((parametri[CONF_HOST], 161)),
        ContextData(),
        ObjectType(ObjectIdentity(parametri[CONF_OID])))
    # eseguo snmp
    errorIndication, errorStatus, errorIndex, varBinds=next(oggetto)
    errore=0
    byteps=0
    if errorIndication:
        errore=1
    elif errorStatus:
        errore=1
    else:
        byteps=varBinds[0][1].prettyPrint()
    result={ "byteps": byteps, "errore": errore }
    _LOGGER.info("luna: interroga_snmp byteps=|"+byteps+"|")
    return(result)

# configuro quali parametri sono opzionali e quali richiesti
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_OID, default=DEFAULT_OID): cv.string,
        vol.Required(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Optional(CONF_COMMUNITY, default=DEFAULT_COMMUNITY): cv.string,
        vol.Optional(CONF_VERSIONE, default=DEFAULT_VERSIONE): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
        vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=DEFAULT_UNIT_OF_MEASUREMENT): cv.string,
        vol.Optional(CONF_ICON, default=DEFAULT_ICON): cv.string
    }
)

#    name: Internet
#    oidin: 1.3.6.1.2.1.31.1.1.1.6.21
#    oidout: 1.3.6.1.2.1.31.1.1.1.10.2
#    community: 'public'
#    unit_of_measurement: "bps"
#    version: 2c
#    scan_interval: 10
#    host: 192.168.2.1

# funzione che viene chiamata per il primo setup della platform
async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Moon sensor."""
    name = config.get(CONF_NAME)
    altro = {
        "oid": config.get(CONF_OID),
        "community": config.get(CONF_COMMUNITY),
        "unit_of_measurement": config.get(CONF_UNIT_OF_MEASUREMENT),
        "version": config.get(CONF_VERSIONE),
        "scan_interval": config.get(CONF_SCAN_INTERVAL),
        "host": config.get(CONF_HOST),
        "icon": config.get(CONF_ICON)
    }
    # qui istanzio la classe..
    oggetto = MoonSensor(name,altro)
    async_add_entities([oggetto], True)

class MoonSensor(Entity):
    """Representation of a Moon sensor."""

    def __init__(self, name, altri_parametri):
        """Initialize the sensor."""
        self._name = name
        self._state = None
        self._parametri = altri_parametri
        self._ultimo_valore_assoluto= 0

#    @property
#    def state_attributes(self):
#        _LOGGER.info("luna: "+self._name+" PROCIONS ")
#        return {
#            "state": self._state,
#            "device_class": "none",
#            "unit_of_measurement": self._parametri[CONF_UNIT_OF_MEASUREMENT],
#            CONF_SCAN_INTERVAL: self._parametri[CONF_SCAN_INTERVAL]
#        }

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self._parametri[CONF_ICON]

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._parametri[CONF_UNIT_OF_MEASUREMENT]

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def state_attributes(self):
        i=str(self._parametri['scan_interval'])
        return { 'intervallo': i }

    async def async_update(self):
        x=interroga_snmp(self._parametri)
        penultimo=self._ultimo_valore_assoluto
        nuovo=x["byteps"]
        _LOGGER.info("luna: "+self._name+" penultimo valore=|"+str(penultimo)+"| nuovo=|"+str(nuovo)+"|")
        if (x["errore"] == 1):
            """il nuovo valore ha un problema"""
            delta=0
        elif (nuovo==0):
            """il nuovo valore è 0, c'è stato un problema"""
            delta=0
        else:
            if (penultimo==0):
                """bene, abbimo la prima rilevazione quindi delta lo forzo ancora a zero"""
                delta=0
                self._ultimo_valore_assoluto=nuovo
            else:
                """dalla seconda rilveazione buona in poi siamo qui"""
                self._ultimo_valore_assoluto=nuovo
                delta=int(nuovo) - int(penultimo)
        dt=self._parametri[CONF_SCAN_INTERVAL]
        dts=float(dt.seconds)
        _bps = float( ( ( (float(delta)/ dts) *8) / 1024) )
        bps = round(_bps,3)
        self._state = bps
        _LOGGER.info("luna: "+self._name+" delta=|"+str(bps)+"|")
