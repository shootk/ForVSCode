import serial
import serial.tools.list_ports


def uart_write_read(w_data, r_size):
    # Write
    ser.write(w_data)
    print('Send: ' + str(w_data))

    # Read
    r_data = ser.read_until(size=r_size)  # size分Read
    print('Recv: ' + str(r_data))

    return r_data


def search_com_port():
    coms = serial.tools.list_ports.comports()
    comlist = []
    for com in coms:
        comlist.append(com.device)
    print('Connected COM ports: ' + str(comlist))
    use_port = comlist[0]
    print('Use COM port: ' + use_port)

    return use_port


if __name__ == '__main__':
    # Search COM Ports
    use_port = search_com_port()

    # Init Serial Port Setting
    ser = serial.Serial(use_port)
    ser.baundrate = 9600
    ser.timeout = 5  # sec

    w_data = b'RV\n'
    r_size = 7
    r_data = uart_write_read(w_data, r_size)
    print('Reserved: {}'.format(r_data))
