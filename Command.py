class Command:
    def __init__(self, speed:int = 0, angle:float = 0, command_type = ""):
        self._speed = speed
        self._angle = angle
        self._command_type = self._define_command_type() if command_type == "" else command_type

    def speed(self):
        return self._speed

    def angle(self):
        return self._angle

    def command_type(self):
        return self._command_type

    def _define_command_type(self):
        if self._speed == 123456 and self._angle == 123456:
            return "test"
        if self._speed == 0 and self._angle == 0.0:
            return "stop"
        elif self._speed != 0 and self._angle == 0.0:
            return "straight"
        elif self._speed == 0 and self._angle != 0:
            return "turn"
        elif self._speed != 0 and self._angle != 0:
            return "strafe"
        elif self._speed == 123 and self._angle == 123:
            return "strafe"
        return "Unknow command"
