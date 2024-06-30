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

def main():
    # Configure the serial client
    client = ModbusClient(method='rtu', port='COM10', baudrate=115200, stopbits=1, bytesize=8, parity='N')

    if not client.connect():
        print("Failed to connect to the device.")
        return

    try:
        # 1. Set position mode, PA_094=1
        address = 0x94
        value = 0x01
        response = write_single_register(client, address, value)
        if response.isError():
            print("Failed to set position mode.")
        else:
            print("Position mode set successfully.")

        # 2. Set parameters: Target position 80000, target velocity 200, acceleration time 200, deceleration time 200
        start_address = 0x9A
        values = [0x0001, 0x3880, 0x0000, 0x00C8, 0x0000, 0x00C8, 0x0000, 0x00C8]
        response = write_multiple_registers(client, start_address, values)
        if response.isError():
            print("Failed to set parameters.")
        else:
            print("Parameters set successfully.")

        # 3. Enable operation, PA_091=3
        address = 0x91
        value = 0x03
        response = write_single_register(client, address, value)
        if response.isError():
            print("Failed to set control mode.")
        else:
            print("Control mode set successfully.")

        # 4. Read value from register PA_03 (System status)
        address = 0x03
        response = read_register(client, address)
        if response.isError():
            print("Failed to read register PA_03 (System status).")
        else:
            print(f"Value read from PA_03 (System status): {response.registers[0]}")

        # 5. Read value from register PA_08 (Driver Error Code)
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