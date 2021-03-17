def loadPriceRules():
    rulesDict = {}
    with open('price-list.txt', 'r') as fp:
        for line in fp:
            lineSplit = line.strip().split(',')
            item = lineSplit[1]
            cmd = lineSplit[0]

            # Try to parse single price
            try:
                price = float(cmd)
            except:
                price = -1

            # Try to parse XFY
            xfy = cmd.upper().split("F")
            try:
                if len(xfy) > 1:
                    xfy[0] = float(xfy[0])
                    xfy[1] = float(xfy[1])
                else:
                    xfy[0] = -1
            except:
                xfy[0] = -1

            itemDict = rulesDict.get(item.upper()) if item.upper() in rulesDict.keys() else {}

            if cmd.upper() == 'BOGO':
                itemDict.update({'BOGO': True})
            elif cmd.upper() == 'BO50':
                itemDict.update({'BO50': True})
            elif price > 0.01:
                itemDict.update({'PRICE': price})
            elif len(xfy) == 2 and xfy[0] > 0 and xfy[1] > 0:
                itemDict.update({'XFY': {'ITEMS': xfy[0], 'PRICE': xfy[1]}})
            else:
                print(
                    "Invalid commands detected. Please check the price-lists.txt and ensure all command are the proper "
                    "format. The invalid rule is " + line.strip())
                exit(1)
            rulesDict.update({item.upper(): itemDict})
    return rulesDict


def loadShoppingCart():
    cartDict = {}
    with open('shopping-cart.txt', 'r') as fp:
        for line in fp:
            # Remove the new line
            cleanLine = line.strip().upper()

            # Item has already been seen increase the count
            if cleanLine in cartDict.keys():
                cartDict[cleanLine] = 1 + cartDict[cleanLine]
            # First time we see an item make a new entry
            else:
                cartDict[cleanLine] = 1
    return cartDict


# Assuming that the user should always get the lowest possible price
def computeLowestPrice(item, rule):
    cost = 0.0
    numItems = item[1]
    price = rule.get('PRICE') if rule is not None else None
    if price is None:
        print('Item ' + item[0] + ' is missing a price')
        exit(1)

    if 'XFY' in rule.keys():
        # Price per unit of all the deals
        xfyPPU = rule.get('XFY').get('PRICE') / rule.get('XFY').get('ITEMS')
        bogoPPU = price / 2

        # The xfy provides a lower price than the BOGO so if possible it should be used first
        if xfyPPU < bogoPPU:
            while numItems >= rule.get('XFY').get('ITEMS'):
                cost += rule.get('XFY').get('PRICE')
                numItems -= rule.get('XFY').get('ITEMS')
    if 'BOGO' in rule.keys() and numItems > 0:
        while numItems > 0:
            cost += price
            numItems = numItems - 2 if numItems >= 2 else 0
    elif 'BO50' in rule.keys() and numItems > 0:
        while numItems > 0:
            cost += price * 1.5
            numItems = numItems - 2 if numItems >= 2 else 0
    cost += price * numItems
    return cost


def buildRecipt(items, rules):
    receipt = []
    totalPrice = 0.0

    for item in items.items():
        lowestPrice = computeLowestPrice(item, rules.get(item[0]))
        lineItem = str(item[0]) + ' x' + str(item[1]) + ' ${:.2f}'.format(lowestPrice)
        totalPrice += lowestPrice
        receipt.append(lineItem)

    # Add total
    finalLine = 'Total ${:.2f}'.format(totalPrice)
    receipt.append(finalLine)

    #  Empty line for formatting
    receipt.append('')
    return receipt


def displayRecipt(output):
    for line in output:
        print(line)


def checkEndProgram():
    while True:
        resp = input('Would you like to enter another transaction? Y/N')
        if resp.upper() == 'Y':
            return False
        elif resp.upper() == 'N':
            return True
        else:
            print('Input not accepted please only enter Y or N')


def main():
    endProgram = False
    while not endProgram:
        rulesDict = loadPriceRules()
        cartItems = loadShoppingCart()
        recipt = buildRecipt(cartItems, rulesDict)
        displayRecipt(recipt)
        endProgram = checkEndProgram()

    print('Program Ending')


if __name__ == '__main__':
    main()
