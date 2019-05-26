import unittest

import power_supply

class TestPowerSupplyAbstractClass(unittest.TestCase):

  def test_instantiate_abstract_interface(self):
    with self.assertRaises(TypeError):
      power_supply_interface = power_supply.PowerSupplyInterface()


if __name__ == '__main__':
    unittest.main()