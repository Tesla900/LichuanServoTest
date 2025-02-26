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

        # 2. Set parameters: Target position 80000 (PA_09A=0x0001, PA_09B=0x3880), target velocity 200 (PA_09C=0x0000, PA_09D=0x00C8), acceleration time 200 (PA_09E=0x0000, PA09F=0x00C8), deceleration time 200 (PA_0A0=0x0000, PA0A1=0x00C8)
        start_address = 0x9A
        values = [0x0001, 0x3880, 0x0000, 0x00C8, 0x0000, 0x00C8, 0x0000, 0x00C8]
        response = write_multiple_registers(client, start_address, values)
        if response.isError():
            print("Failed to set parameters.")
        else:
            print("Parameters set successfully.")

        # 3. Enable relative position mode operation, PA_091=1
        address = 0x91
        value = 0x01
        response = write_single_register(client, address, value)
        if response.isError():
            print("Failed to set control mode.")
        else:
            print("Control mode set successfully.")

    finally:
        client.close()

if __name__ == "__main__":
    main()