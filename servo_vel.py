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
        # 1. Set velocity mode, PA_094=3
        address = 0x94
        value = 0x03
        response = write_single_register(client, address, value)
        if response.isError():
            print("Failed to set velocity mode.")
        else:
            print("Velocity mode set successfully.")

        # 2. Read value from register PA_094 (Mode)
        address = 0x94
        response = read_register(client, address)
        if response.isError():
            print("Failed to read register PA_094 (System mode).")
        else:
            print(f"Value read from PA_094 (System mode): {response.registers[0]}")

        # 3. Set parameters: Acceleration time 200 (PA_09E=0x0000, PA09F=0x00C8), deceleration time 200 (PA_0A0=0x0000, PA0A1=0x00C8), target velocity 200 (PA_0A2=0x0000, PA0A3=0x00C8),
        start_address = 0x9E
        values = [0x0000, 0x00C8, 0x0000, 0x00C8, 0x0000, 0x00C8]
        response = write_multiple_registers(client, start_address, values)
        if response.isError():
            print("Failed to set parameters.")
        else:
            print("Parameters set successfully.")

        # 4. Read multiple registers from PA_09E to PA_A3
        start_address = 0x9E
        count = 6
        response = read_multiple_registers(client, start_address, count)
        if response.isError():
            print("Failed to read multiple registers from PA_9E to PA_A3.")
        else:
            print(f"Values read from PA_9E to PA_A3: {response.registers}")

        # 5. Enable operation, PA_091=4
        address = 0x91
        value = 0x04
        response = write_single_register(client, address, value)
        if response.isError():
            print("Failed to set control mode.")
        else:
            print("Control mode set successfully.")

        # 6. Read value from register PA_091 (Control status)
        address = 0x91
        response = read_register(client, address)
        if response.isError():
            print("Failed to read register PA_091 (Control mode status).")
        else:
            print(f"Value read from PA_091 (Control mode status): {response.registers[0]}")

        # 7. Read value from register PA_03 (System status)
        address = 0x03
        response = read_register(client, address)
        if response.isError():
            print("Failed to read register PA_03 (System status).")
        else:
            print(f"Value read from PA_03 (System status): {response.registers[0]}")

        # 8. Read value from register PA_08 (Driver Error Code)
        address = 0x08
        response = read_register(client, address)
        if response.isError():
            print("Failed to read register PA_08.")
        else:
            print(f"Value read from PA_08 (Driver Error Code): {response.registers[0]}")

        # 9. Read value from register PA_11 (Given velocity)
        address = 0x11
        response = read_register(client, address)
        if response.isError():
            print("Failed to read register PA_11.")
        else:
            print(f"Value read from PA_11 (Given velocity): {response.registers[0]}")

    finally:
        client.close()

if __name__ == "__main__":
    main()