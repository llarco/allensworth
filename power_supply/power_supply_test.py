import unittest
from unittest import mock

import power_supply


class TestPowerSupplyAbstractClass(unittest.TestCase):

  def test_instantiate_abstract_interface(self):
    with self.assertRaises(TypeError):
      # pylint: disable=abstract-class-instantiated
      power_supply.PowerSupplyInterface()


class TestBkPrecision1685BSeriesPowerSupply(unittest.TestCase):

  def setUp(self):
    super(TestBkPrecision1685BSeriesPowerSupply, self).setUp()
    serial_patcher = mock.patch('serial.Serial', autospec=True)
    self.addCleanup(serial_patcher.stop)
    self.mock_serial = serial_patcher.start()

    self.name = 'Test Power Supply'
    self.port = '/dev/test'
    self.model = power_supply.BkPrecision1685BSeriesPowerSupply.Model['1685B']
    self.power_supply = power_supply.BkPrecision1685BSeriesPowerSupply(
        self.name, self.port, self.model)

  def test_set_voltage_level(self):
    mock_serial = self.mock_serial.return_value
    mock_serial.read_until.return_value = b'OK\r'

    self.assertTrue(self.power_supply.set_voltage_level(1.0))
    self.assert_serial_called_without_response(mock_serial, 'VOLT010\r')

  def test_set_current_level(self):
    mock_serial = self.mock_serial.return_value
    mock_serial.read_until.return_value = b'OK\r'

    self.assertTrue(self.power_supply.set_current_level(2.5))
    self.assert_serial_called_without_response(mock_serial, 'CURR025\r')

  def test_get_voltage_level(self):
    mock_serial = self.mock_serial.return_value
    mock_serial.read_until.side_effect = [b'111222\r', b'OK\r']

    voltage = self.power_supply.get_voltage_level()
    self.assertAlmostEqual(voltage, 11.1)
    self.assert_serial_called_with_response(mock_serial, 'GETS\r')

  def test_get_current_level(self):
    mock_serial = self.mock_serial.return_value
    mock_serial.read_until.side_effect = [b'111222\r', b'OK\r']

    current = self.power_supply.get_current_level()
    self.assertAlmostEqual(current, 22.2)
    self.assert_serial_called_with_response(mock_serial, 'GETS\r')

  def test_get_display_voltage(self):
    mock_serial = self.mock_serial.return_value
    mock_serial.read_until.side_effect = [b'030201450\r', b'OK\r']

    voltage = self.power_supply.get_display_voltage()
    self.assertAlmostEqual(voltage, 3.02)
    self.assert_serial_called_with_response(mock_serial, 'GETD\r')

  def test_get_display_current(self):
    mock_serial = self.mock_serial.return_value
    mock_serial.read_until.side_effect = [b'030201450\r', b'OK\r']

    current = self.power_supply.get_display_current()
    self.assertAlmostEqual(current, 1.45)
    self.assert_serial_called_with_response(mock_serial, 'GETD\r')

  def assert_serial_called_without_response(self, mock_serial: mock.Mock,
                                            command: str):
    mock_serial.write.assert_called_with(command)
    mock_serial.read_until.assert_called_with(b'\r')
    mock_serial.reset_input_buffer.assert_called_once()
    mock_serial.reset_output_buffer.assert_called_once()

  def assert_serial_called_with_response(self, mock_serial: mock.Mock,
                                         command: str):
    mock_serial.write.assert_called_with(command)
    mock_serial.read_until.assert_called_with(b'\r')
    mock_serial.read_until.assert_called_with(b'\r')
    mock_serial.reset_input_buffer.assert_called_once()
    mock_serial.reset_output_buffer.assert_called_once()


if __name__ == '__main__':
  unittest.main()
