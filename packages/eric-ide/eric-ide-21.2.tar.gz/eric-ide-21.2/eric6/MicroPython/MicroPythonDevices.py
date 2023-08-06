# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing some utility functions and the MicroPythonDevice base
class.
"""

import logging
import os

from PyQt5.QtCore import pyqtSlot, QObject

from E5Gui.E5Application import e5App

import UI.PixmapCache
import Preferences


SupportedBoards = {
    "esp": {
        "ids": [
            (0x1A86, 0x7523),       # HL-340
            (0x10C4, 0xEA60),       # CP210x
            (0x0403, 0x6001),       # M5Stack ESP32 device"),
            (0x0403, 0x6001),       # FT232/FT245 (XinaBox CW01, CW02)
            (0x0403, 0x6010),       # FT2232C/D/L/HL/Q (ESP-WROVER-KIT)
            (0x0403, 0x6011),       # FT4232
            (0x0403, 0x6014),       # FT232H
            (0x0403, 0x6015),       # Sparkfun ESP32
            (0x0403, 0x601C),       # FT4222H
        ],
        "description": "ESP8266, ESP32",
        "icon": "esp32Device",
        "port_description": "",
    },
    
    "circuitpython": {
        "ids": [
            (0x2B04, 0xC00C),       # Particle Argon
            (0x2B04, 0xC00D),       # Particle Boron
            (0x2B04, 0xC00E),       # Particle Xenon
            (0x239A, None),         # Any Adafruit Boards
            (0x1209, 0xBAB1),       # Electronic Cats Meow Meow
            (0x1209, 0xBAB2),       # Electronic Cats CatWAN USBStick
            (0x1209, 0xBAB3),       # Electronic Cats Bast Pro Mini M0
            (0x1209, 0xBAB6),       # Electronic Cats Escornabot Makech
            (0x1B4F, 0x8D22),       # SparkFun SAMD21 Mini Breakout
            (0x1B4F, 0x8D23),       # SparkFun SAMD21 Dev Breakout
            (0x1209, 0x2017),       # Mini SAM M4
            (0x1209, 0x7102),       # Mini SAM M0
            (0x04D8, 0xEC72),       # XinaBox CC03
            (0x04D8, 0xEC75),       # XinaBox CS11
            (0x04D8, 0xED5E),       # XinaBox CW03
            (0x3171, 0x0101),       # 8086.net Commander
            (0x04D8, 0xED94),       # PyCubed
            (0x04D8, 0xEDBE),       # SAM32
            (0x1D50, 0x60E8),       # PewPew Game Console
            (0x2886, 0x802D),       # Seeed Wio Terminal
            (0x2886, 0x002F),       # Seeed XIAO
            (0x1B4F, 0x0016),       # Sparkfun Thing Plus - SAMD51
            (0x2341, 0x8057),       # Arduino Nano 33 IoT board
            (0x04D8, 0xEAD1),       # DynOSSAT-EDU-EPS
            (0x04D8, 0xEAD2),       # DynOSSAT-EDU-OBC
            (0x1209, 0x4DDD),       # ODT CP Sapling M0
            (0x1209, 0x4DDE),       # ODT CP Sapling M0 w/ SPI Flash
            (0x054C, 0x0BC2),       # Spresense
        ],
        "description": "CircuitPython Board",
        "icon": "circuitPythonDevice",
        "port_description": "",
    },
    
    "bbc_microbit": {
        "ids": [
            (0x0D28, 0x0204),       # micro:bit
        ],
        "description": "BBC micro:bit",
        "icon": "microbitDevice",
        "port_description": "BBC micro:bit CMSIS-DAP",
    },
    
    "calliope": {
        "ids": [
            (0x0D28, 0x0204),       # Calliope mini
        ],
        "description": "Calliope mini",
        "icon": "calliope_mini",
        "port_description": "DAPLink CMSIS-DAP",
    },
    
    "pyboard": {
        "ids": [
            (0xF055, 0x9800),       # Pyboard in CDC mode
            (0xF055, 0x9801),       # Pyboard in CDC+HID mode
            (0xF055, 0x9802),       # Pyboard in CDC+MSC mode
        ],
        "description": "PyBoard",
        "icon": "micropython48",
        "port_description": "",
    },
}

IgnoredBoards = (
    (0x8086, 0x9c3d),
)


def getSupportedDevices():
    """
    Function to get a list of supported MicroPython devices.
    
    @return set of tuples with the board type and description
    @rtype set of tuples of (str, str)
    """
    boards = []
    for board in SupportedBoards:
        boards.append(
            (board, SupportedBoards[board]["description"]))
    return boards


def getFoundDevices():
    """
    Function to check the serial ports for supported MicroPython devices.
    
    @return tuple containing a list of tuples with the board type, a
        description and the serial port it is connected at for known device
        types and a list of tuples with VID, PID and description for unknown
        devices
    @rtype tuple of (list of tuples of (str, str, str), list of tuples of
        (int, int, str)
    """
    from PyQt5.QtSerialPort import QSerialPortInfo
    
    foundDevices = []
    unknownDevices = []
    
    availablePorts = QSerialPortInfo.availablePorts()
    for port in availablePorts:
        supported = False
        vid = port.vendorIdentifier()
        pid = port.productIdentifier()
        for board in SupportedBoards:
            if ((vid, pid) in SupportedBoards[board]["ids"] or
                    (vid, None) in SupportedBoards[board]["ids"]):
                if board in ("bbc_microbit", "calliope"):
                    # both boards have the same VID and PID
                    # try to differentiate based on port description
                    if (
                        port.description().strip() !=
                        SupportedBoards[board]["port_description"]
                    ):
                        continue
                foundDevices.append(
                    (board, SupportedBoards[board]["description"],
                     port.portName()))
                supported = True
        if not supported:
            if vid and pid and (vid, pid) not in IgnoredBoards:
                unknownDevices.append((vid, pid, port.description()))
                logging.debug("Unknown device: (0x%04x:0x%04x %s)",
                              vid, pid, port.description())
    
    return foundDevices, unknownDevices


def getDeviceIcon(boardName, iconFormat=True):
    """
    Function to get the icon for the given board.
    
    @param boardName name of the board
    @type str
    @param iconFormat flag indicating to get an icon or a pixmap
    @type bool
    @return icon for the board (iconFormat == True) or
        a pixmap (iconFormat == False)
    @rtype QIcon or QPixmap
    """
    if boardName in SupportedBoards:
        iconName = SupportedBoards[boardName]["icon"]
    else:
        # return a generic MicroPython icon
        iconName = "micropython48"
    
    if iconFormat:
        return UI.PixmapCache.getIcon(iconName)
    else:
        return UI.PixmapCache.getPixmap(iconName)


def getDevice(deviceType, microPythonWidget):
    """
    Public method to instantiate a specific MicroPython device interface.
    
    @param deviceType type of the device interface
    @type str
    @param microPythonWidget reference to the main MicroPython widget
    @type MicroPythonWidget
    @return instantiated device interface
    @rtype MicroPythonDevice
    """
    if deviceType == "esp":
        from .EspDevices import EspDevice
        return EspDevice(microPythonWidget)
    elif deviceType == "circuitpython":
        from .CircuitPythonDevices import CircuitPythonDevice
        return CircuitPythonDevice(microPythonWidget)
    elif deviceType in ("bbc_microbit", "calliope"):
        from .MicrobitDevices import MicrobitDevice
        return MicrobitDevice(microPythonWidget, deviceType)
    elif deviceType == "pyboard":
        from .PyBoardDevices import PyBoardDevice
        return PyBoardDevice(microPythonWidget)
    else:
        # nothing specific requested
        return MicroPythonDevice(microPythonWidget)


class MicroPythonDevice(QObject):
    """
    Base class for the more specific MicroPython devices.
    """
    def __init__(self, microPythonWidget, parent=None):
        """
        Constructor
        
        @param microPythonWidget reference to the main MicroPython widget
        @type MicroPythonWidget
        @param parent reference to the parent object
        @type QObject
        """
        super(MicroPythonDevice, self).__init__(parent)
        
        self.microPython = microPythonWidget
    
    def setButtons(self):
        """
        Public method to enable the supported action buttons.
        """
        self.microPython.setActionButtons(
            open=False, save=False,
            run=False, repl=False, files=False, chart=False)
    
    def forceInterrupt(self):
        """
        Public method to determine the need for an interrupt when opening the
        serial connection.
        
        @return flag indicating an interrupt is needed
        @rtype bool
        """
        return True
    
    def deviceName(self):
        """
        Public method to get the name of the device.
        
        @return name of the device
        @rtype str
        """
        return self.tr("Unsupported Device")
    
    def canStartRepl(self):
        """
        Public method to determine, if a REPL can be started.
        
        @return tuple containing a flag indicating it is safe to start a REPL
            and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return False, self.tr("REPL is not supported by this device.")
    
    def setRepl(self, on):
        """
        Public method to set the REPL status and dependent status.
        
        @param on flag indicating the active status
        @type bool
        """
        pass
    
    def canStartPlotter(self):
        """
        Public method to determine, if a Plotter can be started.
        
        @return tuple containing a flag indicating it is safe to start a
            Plotter and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return False, self.tr("Plotter is not supported by this device.")
    
    def setPlotter(self, on):
        """
        Public method to set the Plotter status and dependent status.
        
        @param on flag indicating the active status
        @type bool
        """
        pass
    
    def canRunScript(self):
        """
        Public method to determine, if a script can be executed.
        
        @return tuple containing a flag indicating it is safe to start a
            Plotter and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return False, self.tr("Running scripts is not supported by this"
                              " device.")
    
    def runScript(self, script):
        """
        Public method to run the given Python script.
        
        @param script script to be executed
        @type str
        """
        pass
    
    def canStartFileManager(self):
        """
        Public method to determine, if a File Manager can be started.
        
        @return tuple containing a flag indicating it is safe to start a
            File Manager and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return False, self.tr("File Manager is not supported by this device.")
    
    def setFileManager(self, on):
        """
        Public method to set the File Manager status and dependent status.
        
        @param on flag indicating the active status
        @type bool
        """
        pass
    
    def supportsLocalFileAccess(self):
        """
        Public method to indicate file access via a local directory.
        
        @return flag indicating file access via local directory
        @rtype bool
        """
        return False        # default
    
    def getWorkspace(self):
        """
        Public method to get the workspace directory.
        
        @return workspace directory used for saving files
        @rtype str
        """
        return (Preferences.getMultiProject("Workspace") or
                os.path.expanduser("~"))
    
    def sendCommands(self, commandsList):
        """
        Public method to send a list of commands to the device.
        
        @param commandsList list of commands to be sent to the device
        @type list of str
        """
        rawOn = [       # sequence of commands to enter raw mode
            b'\x02',            # Ctrl-B: exit raw repl (just in case)
            b'\r\x03\x03\x03',  # Ctrl-C three times: interrupt any running
                                # program
            b'\r\x01',          # Ctrl-A: enter raw REPL
        ]
        newLine = [b'print("\\n")\r', ]
        commands = [c.encode("utf-8)") + b'\r' for c in commandsList]
        commands.append(b'\r')
        commands.append(b'\x04')
        rawOff = [b'\x02']
        commandSequence = rawOn + newLine + commands + rawOff
        self.microPython.commandsInterface().executeAsync(commandSequence)
    
    @pyqtSlot()
    def handleDataFlood(self):
        """
        Public slot handling a data floof from the device.
        """
        pass
    
    def addDeviceMenuEntries(self, menu):
        """
        Public method to add device specific entries to the given menu.
        
        @param menu reference to the context menu
        @type QMenu
        """
        pass
    
    def hasTimeCommands(self):
        """
        Public method to check, if the device supports time commands.
        
        The default returns True.
        
        @return flag indicating support for time commands
        @rtype bool
        """
        return True
    
    def hasDocumentationUrl(self):
        """
        Public method to check, if the device has a configured documentation
        URL.
        
        @return flag indicating a configured documentation URL
        @rtype bool
        """
        return bool(self.getDocumentationUrl())
    
    def getDocumentationUrl(self):
        """
        Public method to get the device documentation URL.
        
        @return documentation URL of the device
        @rtype str
        """
        return ""
    
    def hasFirmwareUrl(self):
        """
        Public method to check, if the device has a configured firmware
        download URL.
        
        @return flag indicating a configured firmware download URL
        @rtype bool
        """
        return bool(self.getFirmwareUrl())
    
    def getFirmwareUrl(self):
        """
        Public method to get the device firmware download URL.
        
        @return firmware download URL of the device
        @rtype str
        """
        return ""
    
    def downloadFirmware(self):
        """
        Public method to download the device firmware.
        """
        url = self.getFirmwareUrl()
        if url:
            e5App().getObject("UserInterface").launchHelpViewer(url)
