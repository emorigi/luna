# luna

creato per interrogare via snmp una oid e specificatamente usato per prendere l'uso della banda verso internet 

Per installare il componente clonare il componente in locale nella /etc/CARTELLA_HA_CONFIG/custom_components/
in modo che dentro custom_components ci sia la sottocartella "luna" con dentro i files.

Configurare configuration.yaml aggiungendo un sensore:

sensor:
  - platform: luna
    name: WAN_in
    oid: 1.3.6.1.2.1.31.1.1.1.6.3
    community: 'public'
    unit_of_measurement: "MB/s"
    version: 2c
    scan_interval: 60
    icon: mdi:download
    host: 192.168.2.1
  - platform: luna
    name: WAN_out
    oid: 1.3.6.1.2.1.31.1.1.1.10.3
    community: 'public'
    unit_of_measurement: "MB/s"
    version: 2c
    scan_interval: 60
    icon: mdi:upload
    host: 192.168.2.1
    
ovviamente, lasciarlo configurato con i propri parametri.
La configurazione dell'esempio crea due entità che interrogano le oid specificate sul device 192.168.2.1 con la community public 2 versione 2c ogni 60 secondi. Le entità avranno l'icona indicata da icon. Le oid specificate indicano NEL MIO CASO l'interfaccia del mio router (.3 finale) su cui è attaccato "internet".

