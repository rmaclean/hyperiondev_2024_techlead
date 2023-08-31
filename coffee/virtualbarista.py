import internals.coffeeEngine
import internals.machineStorage
import internals.promptHelpers

def collect_and_process_order():
    order = coffeeEngine.promptCustomer()

    cup = machine.makeOrder(order)

    if cup is None:
        print(cup)


print(
    "Welcome, I am your virtual barista; today we only have coffee "
    + "(maybe one day we will do tea too)... how would you like your coffee?"
)

coffeeEngine = internals.coffeeEngine.CoffeeEngine()
machine = internals.machineStorage.Machine()

another_order_wanted = "y"

while another_order_wanted == "y":
    collect_and_process_order()

    another_order_wanted = internals.promptHelpers.prompt_yn("Would you like another drink?")
