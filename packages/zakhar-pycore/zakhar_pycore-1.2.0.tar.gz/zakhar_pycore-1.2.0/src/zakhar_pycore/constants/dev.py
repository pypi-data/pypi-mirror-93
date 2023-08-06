# *************************************************************************
#
# Copyright (c) 2021 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

from .addr import ADDR
from .cmd import CMD, NO_CMD
from .regs import REGS


class INTERFACES:
    i2c = "i2c"
    none = None


class DEV:
    class MOVING_PLATFORM:
        addr = ADDR.I2C.MOTORS
        cmd = CMD.MOVE
        interface = INTERFACES.i2c
        name = "moving_platform"
        reg = REGS.MOVING_PLATFORM

    class SENSOR_PLATFORM:
        addr = ADDR.I2C.SENSORS
        cmd = NO_CMD
        interface = INTERFACES.i2c
        name = "sensor_platform"
        reg = REGS.SENSOR_PLATFORM

    class FACE_MODULE:
        addr = ADDR.I2C.FACE
        cmd = CMD.FACE
        interface = INTERFACES.i2c
        name = "face_platform"
        reg = REGS.FACE_MODULE
