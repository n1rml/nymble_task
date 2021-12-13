import serial, time
import _thread as thread

#configs
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 2400
DATA_TO_SEND  = 'Finance Minister Arun Jaitley Tuesday hit out at former RBI governor Raghuram Rajan for predicting that the next banking crisis would be triggered by MSME lending, saying postmortem is easierthan taking action when it was required. Rajan, who had as the chief economist at IMF warned of impending financial crisis of 2008, in a note to a parliamentary committee warned against ambitious credit targets and loan waivers, saying that they could be the sources of next banking crisis. Government should focus on sources of the next crisis, not just the last one.'

def get_time_ms():
    return int(round(time.time() * 1000))

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0)

def send_message():
    ser.write(DATA_TO_SEND.encode())
    thread.start_new_thread(send_message, ())

file = open('uart_log.txt', 'w')

char_read_count = 0
char_read_speed = 0

last_time = get_time_ms()

thread.start_new_thread(send_message, ())


while True:

    if (get_time_ms() - last_time) >= 100:
        last_time = get_time_ms()
        char_read_speed = char_read_count * 100
        char_read_count = 0

    if ser.in_waiting >= 24:
        try:
            new_read = ser.read(24).decode()
            char_read_count += len(new_read)
            file.write(new_read)
            print('data : {}   actual data rate : {} \r\n'.format(new_read,char_read_speed), end='')
        except UnicodeDecodeError:
            pass
        except:
            pass