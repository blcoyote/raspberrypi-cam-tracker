from servo_controller import ServoController


controller = ServoController(horizontal_pin=23, vertical_pin=22)


controller.move_servos(90, 90)
controller.move_servos(45, 45)
