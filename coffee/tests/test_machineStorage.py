import unittest
from unittest.mock import call, patch
import internals.machineStorage


class MachineStorageTests(unittest.TestCase):
    def test_creating_a_machine_sets_it_up_correctly(self):
        machine = internals.machineStorage.Machine()
        self.assertEqual(machine.beans_available, 250)
        self.assertEqual(machine.water_available, 750)
        self.assertEqual(machine.milk_available, 200)
        self.assertEqual(machine.cup_size, 200)

    @patch("internals.coffeeEngine.CoffeeEngine.makeACoffee", return_value="Done")
    def test_asked_to_make_a_coffee_invokes_coffee_engine(self, mock_coffee_maker):
        machine = internals.machineStorage.Machine()
        result = machine.makeOrder({"type": "coffee"})
        mock_coffee_maker.assert_called()
        self.assertEqual(result, "Done")

    @patch("internals.coffeeEngine.CoffeeEngine.makeACoffee")
    def test_asked_to_make_a_tea_does_nothing(self, mock_coffee_maker):
        machine = internals.machineStorage.Machine()
        with patch("builtins.print") as mock_print:
            result = machine.makeOrder({"type": "tea"})

        mock_coffee_maker.assert_not_called()
        self.assertEqual(result, None)
        self.assertEqual(
            mock_print.call_args,
            call(
                "Sorry, I do not know how to make tea yet"
            ),
        )
