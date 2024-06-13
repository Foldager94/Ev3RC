import _thread
import Queue

class ArduinoController:
    def __init__(self, connection):
        self.connection = connection
        self.queue = Queue()
        self.running = True
        _thread.start_new_thread(self.controller, ())

    def controller(self):
        while self.running:
            command = self.queue.get()
            self.executer(command)

    def executer(self, command):
        if command == "Start-fan":
            self.fan_start()
        elif command == "Stop-fan":
            self.fan_stop()
        elif command == "Open-latch":
            self.latch_open()
        elif command == "Close-latch":
            self.latch_close()
        elif command == "Test-fan":
            self.fan_test()
        else:
            print(f"Command not found: {command}")

    def fan_start(self):
        try:
            self.connection.write(b'f')
        except Exception as e:
            print(e)

    def fan_stop(self):
        try:
            self.connection.write(b'F')
        except Exception as e:
            print(e)

    def latch_open(self):
        try:
            self.connection.write(b'l')
        except Exception as e:
            print(e)

    def latch_close(self):
        try:
            self.connection.write(b'L')
        except Exception as e:
            print(e)

    def fan_test(self):
        try:
            self.connection.write(b't')
        except Exception as e:
            print(e)

    def queue_put(self, value):
        self.queue.put(value)

    def stop_controller(self):
        self.running = False
        self.queue.put(None)
