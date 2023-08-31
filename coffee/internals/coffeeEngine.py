from prompt_toolkit.shortcuts import ProgressBar
import time
import internals.promptHelpers


class CoffeeEngine:
    def process(self):
        # this may take in values in a real system but it is just something
        # fun for this system to look like something is happening
        with ProgressBar() as pb:
            for _ in pb(range(10)):
                time.sleep(1)

    def makeACoffee(self, order, machine):
        waterNeeded = (
            machine.cup_size - (machine.cup_size * 0.05)
        )  # slightly less than the cup so it does not spill
        milkNeeded = 0  # no milk
        coffeeNeeded = 10
        coffeeStyle = " weak "
        withMilk = ""
        match order["customer_coffee_strength"]:
            # case "1": This is the default already handled
            case "2":
                coffeeNeeded = 20
                coffeeStyle = " medium "
            case "3":
                coffeeNeeded = 30
                coffeeStyle = " strong "

        if order["customer_wants_milk"] == "y":
            withMilk = " with milk"
            waterNeeded = machine.cup_size - (machine.cup_size * 0.15)  # need more space for milk
            milkNeeded = machine.cup_size * 0.10  # we think 10% milk is enough

            if order["customer_wants_frothy_milk"] == "y":
                withMilk = " with frothy milk"

        if coffeeNeeded > 0 and machine.beans_available < coffeeNeeded:
            print(
                "Unfortunately we do not have enough beans for this order. Please fill machine and try again."
            )
            return None

        if waterNeeded > 0 and machine.water_available < waterNeeded:
            print(
                "Unfortunately we do not have enough water for this order. Please fill machine and try again."
            )
            return None

        if milkNeeded > 0 and machine.milk_available < milkNeeded:
            print(
                "Unfortunately we do not have enough milk for this order. Please fill machine and try again."
            )
            return None

        # consume ingredients
        machine.beans_available -= coffeeNeeded
        machine.water_available -= waterNeeded
        machine.milk_available -= milkNeeded

        self.process()

        return f"Here is your{coffeeStyle}coffee{withMilk}"

    def promptCustomer(self):
        order = {
            "type": "coffee",
            "customer_wants_milk": None,
            "customer_coffee_strength": None,
            "customer_wants_frothy_milk": None,
        }


        customer_wants_milk = internals.promptHelpers.prompt_yn("Do you want milk in your coffee?")

        order["customer_wants_milk"] = customer_wants_milk

        customer_coffee_strength = internals.promptHelpers.prompt_range("How strong do you want your coffee?")

        order["customer_coffee_strength"] = customer_coffee_strength

        if customer_wants_milk == "y":
            customer_wants_frothy_milk = internals.promptHelpers.prompt_yn("Do you want the milk frothed?")
            order["customer_wants_frothy_milk"] = customer_wants_frothy_milk
        else:
            order["customer_wants_frothy_milk"] = "n"

        return order
