"""Classes for interfacing with a power supply."""
import abc

class PowerSupplyInterface(abc.ABC):
  """Base class for interfacing with a power supply."""

  @abc.abstractmethod
  def set_voltage_level(self, voltage):
    """Sets the voltage level."""
    pass

  @abc.abstractmethod
  def set_current_level(self, current):
    """Sets the current level."""
    pass

  @abc.abstractmethod
  def get_voltage_level(self):
    """Returns the voltage level setting value."""
    pass

  @abc.abstractmethod
  def get_current_level(self):
    """Returns the current level setting value."""
    pass

  @abc.abstractmethod
  def get_display_voltage(self):
    """Returns the display voltage."""
    pass

  @abc.abstractmethod
  def get_display_current(self):
    """Returns the display current."""
    pass

  @abc.abstractmethod
  def set_output_on(self):
    """Sets the output to ON."""
    pass

  @abc.abstractmethod
  def set_output_off(self):
    """Sets the output to OFF."""
    pass