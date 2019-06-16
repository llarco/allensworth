import unittest
from unittest import mock

import publisher
from power_supply import power_supply


class TestPublisher(unittest.TestCase):

  def setUp(self):
    super(TestPublisher, self).setUp()
    self.google_cloud_project_id = 'google_cloud_project_id'
    self.pubsub_topic_name = 'pubsub_topic_name'
    mock_power_supply_1 = mock.MagicMock(
        spec=power_supply.BkPrecision1685BSeriesPowerSupply)
    self.power_supply_1 = mock_power_supply_1.return_value
    mock_power_supply_2 = mock.MagicMock(
        spec=power_supply.BkPrecision1685BSeriesPowerSupply)
    self.power_supply_2 = mock_power_supply_2.return_value
    self.power_supplies = [self.power_supply_1, self.power_supply_2]

  def test_read_and_publish(self):
    data_publisher = publisher.Publisher(
        self.power_supplies, self.google_cloud_project_id,
        self.pubsub_topic_name)
    data_publisher.read_data_and_publish()

    for ps in self.power_supplies:
      ps.get_voltage_level.assert_called_once_with()
      ps.get_current_level.assert_called_once_with()
      ps.get_display_voltage.assert_called_once_with()
      ps.get_display_current.assert_called_once_with()


if __name__ == '__main__':
  unittest.main()
