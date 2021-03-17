# Checkout Application

This application is used to take in an input of items in a shopping cart, and a list of price rules. The application
will then apply the price rules to the items and calculate the price sent on each item and the total price of the
transaction. The system will always calculate the lowest possible price for the transaction. The shopping cart and price
rules should both be defined in files. These files can be changed while the application is running and each distinct run
will apply the latest rules and cart.

## Input format

The input for the shopping cart and the price rules should be placed in their own file and 
encoded in a standard string format a .txt file is recommended. See the ```*-example``` files for a visual example.
The names of items and commands are case-insensitive.  

### Cart

The format of items in the cart file is that each item should be placed on its own line. For example

Apple

Apple

This will add two apples to the cart. If the input was Apple,Apple or AppleApple. This will not function as expected. This
will produce the items Apple,Apple and AppleApple

### Price Rules

This application currently supports four different commands for the pricing of items. Each command tuple should be on its
own line, and a comma should separate the command from the target item.

#### Regular price

The first is to set a regular price of an item. This is required for all items in the system. If an item does not have a
regular price the system will throw an error and exit. The format of this command is ```X.XX,ITEM ```. The number set
for the price must be positive and at least 0.01. The system will also truncate prices to 2 decimal places as this is
convention with currency.

#### Buy one, get one free

The system will accept a command to apply a discount of buy one, get one free. The format of this command
is ```BOGO,ITEM```. If an odd number of items are in the cart, and the bogo is applied you will not receive any discount
in the final item.

#### Buy one, get one 50% off

The system will accept a command to apply a discount of 50% to a second item when an item is purchased at full price.
The format of this command is ```BO50,ITEM```. That is B O Five Zero. If there are an odd number of items to apply the
discount to then the final item will be applied at full price.

#### X item for Y price

The system will accept a command to apply a special price for a lot of items. An example of this is buy three apples for a
dollar. The format of this command is ``` XFY,ITEM```. Where X is the size of the lot required to apply the discount and
Y is the price of the lot. This discount will only be applied if it provides a better price than the regular price of
the item

## Restrictions

### Multiple Price Rules

The system is currently implemented to only work with a single discount available for each item. If multiple discounts
are set for an item, the system will not error, but the guarantee of the lowest price calculation is no longer valid.

### Ignores Free Items

If there is a BOGO deal on an item, and an odd number of items exists in the cart, the customer will receive the item at
regular price. This situation brings a question should the customer have another one of the items added to their cart?
They have technically paid for it. There is also the option of having the item be discounted by 50%. The system could
also notify them and let the customer decide.

### Rule Overwrite

Currently, if a price rule for an item is defined twice then the system will use the one defined later in the files. For
example if you set a three for five rule on apples and then later in the file you set a two for five. The system will use the two for
five rule as it was defined later.

## Running the application

This application requires a full installation of python3 to run. It requires sys,os and unittest from the standard
python library.

To run the application in interactive mode

```python3 checkout_application.py <Rules-File> <Cart-File>```

To run the unit tests

```python3 checkout_application_tests.py ```