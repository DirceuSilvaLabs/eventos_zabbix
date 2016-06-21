# -*- coding: utf-8 -*- 
from pyzabbix import ZabbixAPI
from getpass import getpass



def get(endereco,usuario,senha):
    
    ZABBIX_SERVER = endereco
    zapi = ZabbixAPI(ZABBIX_SERVER)
    
    zapi.login(usuario, senha)
    
    triggers = zapi.trigger.get(only_true=1,
        skipDependent=1,
        monitored=1,
        active=1,
        output='extend',
        expandDescription=1,
        expandData='host',
    )
    
    unack_triggers = zapi.trigger.get(only_true=1,
        skipDependent=1,
        monitored=1,
        active=1,
        output='extend',
        expandDescription=1,
        expandData='host',
        withLastEventUnacknowledged=1,
    )
    unack_trigger_ids = [t['triggerid'] for t in unack_triggers]
    for t in triggers:
        t['unacknowledged'] = True if t['triggerid'] in unack_trigger_ids\
        else False
    print triggers 
    #return triggers 
