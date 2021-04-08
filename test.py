import minimalmodbus, struct, configparser, os
from os.path import join
from time import sleep

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(join(dirname, 'config.ini'))

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

def main(): 

    while True:
        try:
            ph = readModbusRegisters(2049)
            temperature = readModbusRegisters(2051)
            cod = readModbusRegisters(2053)
            tss = readModbusRegisters(2055)
            nh4 = readModbusRegisters(2057)
            k = readModbusRegisters(2059)
            level1 = readModbusRegisters(2073)
            radar_level1 = readModbusRegisters(2075)
            level2 = readModbusRegisters(2077)
            radar_level2 = readModbusRegisters(2079)

            print('-'*40)
            print("PH: {}".format(ph))
            print("Temperature: {}°".format(temperature))
            print("COD: {}mg/L".format(cod))
            print("TSS: {}mg/L".format(tss))
            print("NH4-N: {}mg/L".format(nh4))
            print("K+: {}mg/L".format(k))
            print("Level 1: {}m/s".format(level1))
            print("Radar Level 1: {}m/s".format(radar_level1))
            print("Level 2: {}m/s".format(level2))
            print("Radar Level 2: {}m/s".format(radar_level2))
            print('-'*40)
        except:
            print('Retrying...')

        sleep(1)

if __name__ == "__main__":
    main()