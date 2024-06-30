from pymodbus.client import ModbusSerialClient as ModbusClient

def write_single_register(client, address, value):
    response = client.write_register(address, value, slave=1)
    return response

def read_register(client, address):
    response = client.read_holding_registers(address, count=1, slave=1)
    return response

def main():
    # Configure the serial client
    client = ModbusClient(method='rtu', port='COM10', baudrate=115200, stopbits=1, bytesize=8, parity='N')

    if not client.connect():
        print("Failed to connect to the device.")
        return

    try:
        # 1. Read value from register PA_083
        address = 0x83
        response = read_register(client, address)
        if response.isError():
            print("Failed.")
        else:
            print(f"Value read from PA_083: {response.registers[0]}")

    finally:
        client.close()

if __name__ == "__main__":
    main()