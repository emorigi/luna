# luna

creato per interrogare via snmp una oid e specificatamente usato per prendere l'uso della banda verso internet 

Installazione componente su Home Assistant
1. cd CARTELLA_CONFIG_HOMEASSISTANT
2. mkdir custom_component
3. cd custom_component
4. mkdir luna ; cd luna ; git clonarci dentro il componente

configurazione di home assistant
1. modificare configuration.yaml con:
sensor:
  - platform: luna
    name: WAN_in
    oid: 1.3.6.1.2.1.31.1.1.1.6.3
    community: 'public'
    unit_of_measurement: "Bps"
    version: 2c
    scan_interval: 10
    host: 192.168.2.1
    
ovviamente con i propri parametri
