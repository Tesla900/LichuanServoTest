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
        # 1. Read value from register PA_064 (System reset)
        address = 0x64
        response = read_register(client, address)
        if response.isError():
            print("Failed to read register PA_064 (System reset).")
        else:
            print(f"Value read from PA_64 (System reset): {response.registers[0]}")

        # 2. Reset system, PA_064=1
        address = 0x64
        value = 0x01
        response = write_single_register(client, address, value)
        if response.isError():
            print("Failed to reset to factory settings.")
        else:
            print("Successfully set to defaults.")

    finally:
        client.close()

if __name__ == "__main__":
    main()