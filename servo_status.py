from pymodbus.client import ModbusSerialClient as ModbusClient

def write_single_register(client, address, value):
    response = client.write_register(address, value, slave=1)
    return response

def write_multiple_registers(client, start_address, values):
    response = client.write_registers(start_address, values, slave=1)
    return response

def read_register(client, address):
    response = client.read_holding_registers(address, count=1, slave=1)
    return response

def read_multiple_registers(client, start_address, count):
    response = client.read_holding_registers(start_address, count=count, slave=1)
    return response

def main():
    # Configure the serial client
    client = ModbusClient(method='rtu', port='COM10', baudrate=115200, stopbits=1, bytesize=8, parity='N')

    if not client.connect():
        print("Failed to connect to the device.")
        return
    try:
        # 1. Read value from register PA_03 (System status)
        address = 0x03
        response = read_register(client, address)
        if response.isError():
            print("Failed to read register PA_03 (System status).")
        else:
            print(f"Value read from PA_03 (System status): {response.registers[0]}")

        # 2. Read value from register PA_08 (Driver Error Code)
        address = 0x08
        response = read_register(client, address)
        if response.isError():
            print("Failed to read register PA_08.")
        else:
            print(f"Value read from PA_08 (Driver Error Code): {response.registers[0]}")
    finally:
        client.close()

if __name__ == "__main__":
    main()