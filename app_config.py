import configparser

config = configparser.ConfigParser()
config['VIN'] = {
    'official': 'YV4952NA4F120DEMO',  
    'unofficial': 'YV4952NA4F120DEMO'  
}

config['URL'] = {
    'official': 'https://api.volvocars.com/connected-vehicle/v2',
    'unofficial': 'https://playground.kls.hackclub.app/connected-vehicle/v2'
}

config.read('config.ini')

VINofficial = config['VIN']['official']
VINunofficial = config['VIN']['unofficial']

officialURL = config['URL']['official']
unofficialURL = config['URL']['unofficial']