import unittest
from unittest.mock import call, patch
import internals.coffeeEngine
import internals.machineStorage


class CoffeeEngineTests(unittest.TestCase):
    @patch("internals.promptHelpers.prompt_yn", return_value="n")
    @patch("internals.promptHelpers.prompt_range", return_value="1")
    def test_promptCustomer_customer_wants_weak_americano(self, _, __):
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = coffeeEngine.promptCustomer()

        self.assertEqual(order["customer_wants_milk"], "n")
        self.assertEqual(order["customer_coffee_strength"], "1")
        self.assertEqual(order["customer_wants_frothy_milk"], "n")

    @patch("internals.coffeeEngine.CoffeeEngine.process")
    def test_making_a_weak_americano(self, _):
        machine = internals.machineStorage.Machine()
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = {
            "customer_coffee_strength": "1",
            "customer_wants_milk": "n",
            "customer_wants_frothy_milk": "n",
        }

        result = coffeeEngine.makeACoffee(order, machine)
        self.assertEqual(result, "Here is your weak coffee")
        self.assertEqual(machine.beans_available, 240)
        self.assertEqual(machine.milk_available, 200)
        self.assertEqual(machine.water_available, 560)

    @patch("internals.promptHelpers.prompt_yn", return_value="n")
    @patch("internals.promptHelpers.prompt_range", return_value="2")
    def test_promptCustomer_customer_wants_medium_americano(self, _, __):
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = coffeeEngine.promptCustomer()

        self.assertEqual(order["customer_wants_milk"], "n")
        self.assertEqual(order["customer_coffee_strength"], "2")
        self.assertEqual(order["customer_wants_frothy_milk"], "n")

    @patch("internals.coffeeEngine.CoffeeEngine.process")
    def test_making_a_medium_americano(self, _):
        machine = internals.machineStorage.Machine()
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = {
            "customer_coffee_strength": "2",
            "customer_wants_milk": "n",
            "customer_wants_frothy_milk": "n",
        }

        result = coffeeEngine.makeACoffee(order, machine)
        self.assertEqual(result, "Here is your medium coffee")
        self.assertEqual(machine.beans_available, 230)
        self.assertEqual(machine.milk_available, 200)
        self.assertEqual(machine.water_available, 560)

    @patch("internals.promptHelpers.prompt_yn", return_value="n")
    @patch("internals.promptHelpers.prompt_range", return_value="3")
    def test_promptCustomer_customer_wants_strong_americano(self, _, __):
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = coffeeEngine.promptCustomer()

        self.assertEqual(order["customer_wants_milk"], "n")
        self.assertEqual(order["customer_coffee_strength"], "3")
        self.assertEqual(order["customer_wants_frothy_milk"], "n")

    @patch("internals.coffeeEngine.CoffeeEngine.process")
    def test_making_a_strong_americano(self, _):
        machine = internals.machineStorage.Machine()
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = {
            "customer_coffee_strength": "3",
            "customer_wants_milk": "n",
            "customer_wants_frothy_milk": "n",
        }

        result = coffeeEngine.makeACoffee(order, machine)
        self.assertEqual(result, "Here is your strong coffee")
        self.assertEqual(machine.beans_available, 220)
        self.assertEqual(machine.milk_available, 200)
        self.assertEqual(machine.water_available, 560)

    @patch("internals.promptHelpers.prompt_yn", return_value="y")
    @patch("internals.promptHelpers.prompt_range", return_value="3")
    def test_promptCustomer_customer_wants_strong_cappuccino(self, _, __):
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = coffeeEngine.promptCustomer()

        self.assertEqual(order["customer_wants_milk"], "y")
        self.assertEqual(order["customer_coffee_strength"], "3")
        self.assertEqual(order["customer_wants_frothy_milk"], "y")

    @patch("internals.coffeeEngine.CoffeeEngine.process")
    def test_making_a_strong_cappuccino(self, _):
        machine = internals.machineStorage.Machine()
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = {
            "customer_coffee_strength": "3",
            "customer_wants_milk": "y",
            "customer_wants_frothy_milk": "y",
        }

        result = coffeeEngine.makeACoffee(order, machine)
        self.assertEqual(result, "Here is your strong coffee with frothy milk")
        self.assertEqual(machine.beans_available, 220)
        self.assertEqual(machine.milk_available, 180)
        self.assertEqual(machine.water_available, 580)

    @patch("internals.promptHelpers.prompt_yn", side_effect=["y", "n"])
    @patch("internals.promptHelpers.prompt_range", return_value="1")
    def test_promptCustomer_customer_wants_weak_flat_white(self, _, __):
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = coffeeEngine.promptCustomer()

        self.assertEqual(order["customer_wants_milk"], "y")
        self.assertEqual(order["customer_coffee_strength"], "1")
        self.assertEqual(order["customer_wants_frothy_milk"], "n")

    @patch("internals.coffeeEngine.CoffeeEngine.process")
    def test_making_a_weak_flat_white(self, _):
        machine = internals.machineStorage.Machine()
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = {
            "customer_coffee_strength": "1",
            "customer_wants_milk": "y",
            "customer_wants_frothy_milk": "n",
        }

        result = coffeeEngine.makeACoffee(order, machine)
        self.assertEqual(result, "Here is your weak coffee with milk")
        self.assertEqual(machine.beans_available, 240)
        self.assertEqual(machine.milk_available, 180)
        self.assertEqual(machine.water_available, 580)

    @patch("internals.coffeeEngine.CoffeeEngine.process")
    def test_cant_make_coffee_without_enough_beans(self, _):
        machine = internals.machineStorage.Machine()
        machine.beans_available = 0
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = {
            "customer_coffee_strength": "1",
            "customer_wants_milk": "y",
            "customer_wants_frothy_milk": "n",
        }

        with patch("builtins.print") as mock_print:
            result = coffeeEngine.makeACoffee(order, machine)

        self.assertEqual(result, None)
        self.assertEqual(
            mock_print.call_args,
            call(
                "Unfortunately we do not have enough beans for this order. Please fill machine and try again."
            ),
        )

    @patch("internals.coffeeEngine.CoffeeEngine.process")
    def test_cant_make_coffee_without_enough_water(self, _):
        machine = internals.machineStorage.Machine()
        machine.water_available = 0
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = {
            "customer_coffee_strength": "1",
            "customer_wants_milk": "y",
            "customer_wants_frothy_milk": "n",
        }

        with patch("builtins.print") as mock_print:
            result = coffeeEngine.makeACoffee(order, machine)

        self.assertEqual(result, None)
        self.assertEqual(
            mock_print.call_args,
            call(
                "Unfortunately we do not have enough water for this order. Please fill machine and try again."
            ),
        )

    @patch("internals.coffeeEngine.CoffeeEngine.process")
    def test_cant_make_coffee_without_enough_milk(self, _):
        machine = internals.machineStorage.Machine()
        machine.milk_available = 0
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = {
            "customer_coffee_strength": "1",
            "customer_wants_milk": "y",
            "customer_wants_frothy_milk": "n",
        }

        with patch("builtins.print") as mock_print:
            result = coffeeEngine.makeACoffee(order, machine)

        self.assertEqual(result, None)
        self.assertEqual(
            mock_print.call_args,
            call(
                "Unfortunately we do not have enough milk for this order. Please fill machine and try again."
            ),
        )

    @patch("internals.coffeeEngine.CoffeeEngine.process")
    def test_no_milk_does_not_block_creating_americano(self, _):
        machine = internals.machineStorage.Machine()
        machine.milk_available = 0
        coffeeEngine = internals.coffeeEngine.CoffeeEngine()
        order = {
            "customer_coffee_strength": "1",
            "customer_wants_milk": "n",
            "customer_wants_frothy_milk": "n",
        }

        result = coffeeEngine.makeACoffee(order, machine)

        self.assertEqual(result, "Here is your weak coffee")
        self.assertEqual(machine.beans_available, 240)
        self.assertEqual(machine.milk_available, 0)
        self.assertEqual(machine.water_available, 560)
