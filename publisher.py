"""Publishes data to the cloud."""

import argparse
from power_supply import power_supply
import typing

parser = argparse.ArgumentParser()
parser.add_argument('--google_cloud_project_id', type=str, required=True,
                    help='Google Cloud project ID.')
parser.add_argument('--pubsub_topic_name', type=str, required=True,
                    help='Pub/Sub topic name.')


class Publisher(object):
  def __init__(self, power_supplies: typing.List[
          power_supply.BkPrecision1685BSeriesPowerSupply],
          google_cloud_project_id: str,
          pubsub_topic_name: str):
    self.power_supplies = power_supplies
    self.google_cloud_project_id = google_cloud_project_id
    self.pubsub_topic_name = pubsub_topic_name

  def _read_data(self):
    data = {}
    for ps in self.power_supplies:
      data.update({
          ps.name: {
              'voltage_level': ps.get_voltage_level(),
              'current_level': ps.get_current_level(),
              'display_voltage': ps.get_display_voltage(),
              'display_current': ps.get_display_current()
          }
      })
    return data.copy()

  def read_data_and_publish(self):
    unused_data = self._read_data()
    # TODO: publish data to PubSub.


def main():
  args = parser.parse_args()

  bk_power_supply_1 = power_supply.BkPrecision1685BSeriesPowerSupply(
      name='Power Supply 1', port='/dev/ttyUSB0',
      model=power_supply.BkPrecision1685BSeriesPowerSupply.Model['1685B'])

  bk_power_supply_2 = power_supply.BkPrecision1685BSeriesPowerSupply(
      name='Power Supply 2', port='/dev/ttyUSB1',
      model=power_supply.BkPrecision1685BSeriesPowerSupply.Model['1685B'])

  publisher = Publisher(power_supplies=[bk_power_supply_1, bk_power_supply_2],
                        google_cloud_project_id=args.google_cloud_project_id,
                        pubsub_topic_name=args.pubsub_topic_name)

  while True:
    publisher.read_data_and_publish()


if __name__ == "__main__":
  main()
