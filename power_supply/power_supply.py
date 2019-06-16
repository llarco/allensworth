"""Classes for interfacing with a power supply."""
import abc
import enum
import logging
import serial
import typing


class PowerSupplyInterface(abc.ABC):
  """Base class for interfacing with a power supply."""

  @abc.abstractmethod
  def set_voltage_level(self, voltage: float) -> bool:
    """Sets the voltage level in Volts."""
    pass

  @abc.abstractmethod
  def set_current_level(self, current: float) -> bool:
    """Sets the current level in Amps."""
    pass

  @abc.abstractmethod
  def get_voltage_level(self) -> float:
    """Returns the voltage level setting value in Volts."""
    pass

  @abc.abstractmethod
  def get_current_level(self) -> float:
    """Returns the current level setting value in Amps."""
    pass

  @abc.abstractmethod
  def get_display_voltage(self) -> float:
    """Returns the display voltage in Volts."""
    pass

  @abc.abstractmethod
  def get_display_current(self) -> float:
    """Returns the display current in Amps."""
    pass

  @abc.abstractmethod
  def set_output_on(self) -> None:
    """Sets the output to ON."""
    pass

  @abc.abstractmethod
  def set_output_off(self) -> None:
    """Sets the output to OFF."""
    pass


class BkPrecision1685BSeriesPowerSupply(PowerSupplyInterface):
  """Class to interface with a BK Precision 1685B Series power supply.

  Based on the BK Precision 1685B, 1687B, and 1688B Programming Manual:
  https://bkpmedia.s3.amazonaws.com/downloads/programming_manuals/en-us/168xB_programming_manual.pdf

  Args:
    name: Name of the device.
    port: Device name, e.g. '/dev/ttyUSB0'.
    model: Device model. Must be either 1685B, 1687B, or 1688B.
  """

  Model = enum.Enum('Model', '1685B 1687B 1688B')
  Mode = enum.Enum('Mode', 'CC CV')

  def __init__(self, name: str, port: str, model: Model,
               timeout_seconds: float = 5.0):
    super(BkPrecision1685BSeriesPowerSupply, self).__init__()
    assert name is not None
    assert model is not None
    self._name = name
    self._model = model
    self._serial = serial.Serial(port=port, baudrate=9600,
                                 bytesize=serial.EIGHTBITS,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 timeout=timeout_seconds)

  @property
  def name(self):
    return self._name

  def close(self) -> None:
    self._serial.close()

  def _reset_buffer(self) -> None:
    self._serial.reset_input_buffer()
    self._serial.reset_output_buffer()

  def _value_to_string(self, value: float) -> str:
    return str(int(value * 10)).zfill(3)

  def _send_command(self, command: str, value: float = None) -> typing.Union[
          typing.Dict[str, typing.Any], bool]:
    message = command
    if value is not None:
      assert 0.0 <= value <= 99.9
      message += self._value_to_string(value)
    self._reset_buffer()
    self._serial.write(message + '\r')
    response = self._serial.read_until(b'\r')

    if command not in ['GETS', 'GETD']:
      return response.decode().rstrip() == 'OK'

    confirm = self._serial.read_until(b'\r')
    if confirm.decode().rstrip() != 'OK':
      logging.error(('Response to command `%s` did not return OK. Response '
                     'was: %s'), command, response.decode().rstrip())
      return None
    value = response.decode().rstrip()

    if command == 'GETS':
      if len(value) != 6:
        logging.error(('Response to command GETS did not return a valid '
                       'response length. Response was: %s'), value)
        return None
      else:
        voltage = int(value[:3])
        current = int(value[-3:])
        return {'voltage': voltage / 10.0, 'current': current / 10.0}
    elif command == 'GETD':
      if len(value) != 9:
        logging.error(('Response to command GETD did not return a valid '
                       'response length. Response was: %s'), value)
        return None
      else:
        voltage = int(value[:4])
        current = int(value[4:8])
        status = int(value[-1])
        return {
            'voltage': voltage / 100.0,
            'current': current / 100.0,
            'status': (BkPrecision1685BSeriesPowerSupply.Mode.CV if status == 0
                       else BkPrecision1685BSeriesPowerSupply.Mode.CC)
        }

  def get_voltage_level(self) -> float:
    response = self._send_command('GETS')
    if response is None:
      return None
    return response['voltage']

  def get_current_level(self) -> float:
    response = self._send_command('GETS')
    if response is None:
      return None
    return response['current']

  def get_display_voltage(self) -> float:
    response = self._send_command('GETD')
    if response is None:
      return None
    return response['voltage']

  def get_display_current(self) -> float:
    response = self._send_command('GETD')
    if response is None:
      return None
    return response['current']

  def set_voltage_level(self, voltage: float) -> bool:
    return self._send_command('VOLT010')

  def set_current_level(self, current: float) -> bool:
    return self._send_command('CURR025')

  def set_output_on(self) -> None:
    return self._send_command('SOUT0')

  def set_output_off(self) -> None:
    return self._send_command('SOUT1')
