# Coffee System Demo

This app is a small demo of a virtual barista, who can make you a coffee.

## Setup

This uses Python 3.11 and requirements can be installed with PiP, for example: `pip3 install -r requirements.txt`

## Running it

As easy as possible: `python virtualbarista.py`

### Development Tools

If you want to lint the code, you can run `./lint.sh`
If you want to run the unit tests, you can run `./test.sh`

## Adding Tea

So you want to add tea to the system, or any other drink. The idea is the number of changes are minimal.

1. Create a new engine, like we have for coffee which knows how to prompt for a user and make the item
2. Modifier the machine storage for new ingredients and match up the order type to the correct processing code
3. Add a check the virtual barista to ask what drink someone wants and then run the relevant prompt

### Additional

I did not create an interface/abstract class for the engine since it is not ideal to have a single implementation - if you are adding more drinks, defining that may help with consistency going forward, something like this:

```python
class Engine():
  @abstractmethod
  def promptCustomer(self):
    pass
```

### How does this support team collaboration?

This is an interesting question since it is pretty small in nature but if it grew the fact that each engine is isolated will help keep code logical. The unit tests and documentation also provide guidance on how it works.
As mentioned above, I built this code for the purpose outlined but in a team situation more specific aspects like having an Engine abstract class that everything is based on would mean it is easy to have a simple list to store the engines in and potentially a single place to configure the machine.

Support for linting is also added and in a real system, I would use githooks to enforce unit tests and linting as a prepush check to help keep it consistent.
