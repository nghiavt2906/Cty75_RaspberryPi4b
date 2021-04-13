import minimalmodbus, struct, configparser, os, csv
from os.path import join
from datetime import datetime
from time import time, sleep

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(join(dirname, 'config.ini'))

maxRecordId = int(config['DEFAULT']['CURRENT_MAX_RECORD_ID'])

hmi = minimalmodbus.Instrument(config['HMI']['PORT'], int(config['HMI']['ID']))
hmi.serial.baudrate = int(config['HMI']['BAUDRATE'])

def readModbusRegisters(address):
    values = hmi.read_registers(address, 2)
    highByte, lowByte = list(map(lambda x: hex(x)[2:], values))
    while len(lowByte) < 4:
        lowByte += '0'
    while len(highByte) < 4:
        highByte += '0'

    hex_values = lowByte + highByte
    value = struct.unpack('!f', bytes.fromhex(hex_values))[0]

    return value

def readSensors():
    global maxRecordId

    record = {
        'Timestamp': datetime.now(),
        'PH': readModbusRegisters(2049),
        'Temperature': readModbusRegisters(2051),
        'COD': readModbusRegisters(2053),
        'TSS': readModbusRegisters(2055),
        'NH4-N': readModbusRegisters(2057),
        'K+': readModbusRegisters(2059),
        'Level-1': readModbusRegisters(2073),
        'Radar-level-1': readModbusRegisters(2075),
        'Level-2': readModbusRegisters(2077),
        'Radar-level-2': readModbusRegisters(2079)
    }        

    maxRecordId += 1
    record['Id'] = maxRecordId

    return record

def saveFile(data, filename, fieldnames):
    if not os.path.exists('pending'):
        os.mkdir('pending')

    with open(filename, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    config.set('DEFAULT', 'CURRENT_MAX_RECORD_ID', str(maxRecordId))
    with open(join(dirname, 'config.ini'), 'w') as configfile:
        config.write(configfile)

def main(): 
    data = []
    current_timestamp = datetime.now()
    filename = join(dirname, 'pending/{}.csv'.format(current_timestamp))
    fieldnames = [
        'Id', 
        'Timestamp', 
        'PH', 
        'Temperature', 
        'COD', 
        'TSS', 
        'NH4-N', 
        'K+', 
        'Level-1', 
        'Radar-level-1', 
        'Level-2', 
        'Radar-level-2'
    ]
    start = time()

    while True:
        try:
            if time() - start >= int(config['DEFAULT']['SAVE_INTERVAL']):
                saveFile(data, filename, fieldnames)
                data = []
                current_timestamp = datetime.now()
                filename = join(dirname, 'pending/GiaLai_CTY75_NUO_{}.csv'.format(current_timestamp))
                start = time()

            record = readSensors()
            data.append(record)
        except:
            print('Retrying...')

        sleep(int(config['DEFAULT']['READ_INTERVAL']))

if __name__ == "__main__":
    main()