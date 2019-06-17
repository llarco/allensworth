import json
import unittest
from unittest import mock

import publisher
from power_supply import power_supply


class TestPublisher(unittest.TestCase):

  def setUp(self):
    super(TestPublisher, self).setUp()
    self.google_cloud_project_id = 'google_cloud_project_id'
    self.pubsub_topic_name = 'pubsub_topic_name'
    self.power_supplies = []
    for i in [1, 2]:
      mock_power_supply_1 = mock.MagicMock(
          spec=power_supply.BkPrecision1685BSeriesPowerSupply)
      power_supply_obj = mock_power_supply_1.return_value
      power_supply_obj.name = 'Power Supply {0}'.format(i)
      power_supply_obj.get_voltage_level.return_value = float(i)
      power_supply_obj.get_current_level.return_value = float(i) + 0.1
      power_supply_obj.get_display_voltage.return_value = float(i) + 0.2
      power_supply_obj.get_display_current.return_value = float(i) + 0.3
      self.power_supplies.append(power_supply_obj)

  @mock.patch('time.time_ns', mock.MagicMock(return_value=12345))
  @mock.patch('google.cloud.pubsub_v1.PublisherClient', autospec=True)
  def test_read_and_publish(self, mock_publisher_client):

    topic_name = 'projects/{0}/topics/{1}'.format(self.google_cloud_project_id,
                                                  self.pubsub_topic_name)
    mock_publisher_client.return_value.topic_path.return_value = topic_name

    data_publisher = publisher.Publisher(
        self.power_supplies, self.google_cloud_project_id,
        self.pubsub_topic_name)
    data_publisher.read_data_and_publish()

    for ps in self.power_supplies:
      ps.get_voltage_level.assert_called_once_with()
      ps.get_current_level.assert_called_once_with()
      ps.get_display_voltage.assert_called_once_with()
      ps.get_display_current.assert_called_once_with()

    mock_publisher_client.return_value.topic_path.assert_called_once_with(
        self.google_cloud_project_id, self.pubsub_topic_name)

    mock_publisher_client.return_value.publish.assert_called_with(
        topic_name,
        data=json.dumps({
            'time_ns': 12345,
            'Power Supply 1': {
                'voltage_level': 1.0,
                'current_level': 1.1,
                'display_voltage': 1.2,
                'display_current': 1.3},
            'Power Supply 2': {
                'voltage_level': 2.0,
                'current_level': 2.1,
                'display_voltage': 2.2,
                'display_current': 2.3}}))


if __name__ == '__main__':
  unittest.main()
