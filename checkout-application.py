def loadPriceRules():
    rulesDict = {}
    with open('price-list.txt', 'r') as fp:
        for line in fp:
            lineSplit = line.strip().split(',')
            item = lineSplit[1]
            cmd = lineSplit[0]

            # Try to parse single price
            price = -1
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
            elif price > 0:
                itemDict.update({'PRICE': price})
            elif len(xfy) == 2 and xfy[0] > 0 and xfy[1] > 0:
                itemDict.update({'XFY': {'ITEMS': xfy[0], 'PRICE': xfy[1]}})
            else:
                print(
                    "Invalid commands detected please check the price-lists.txt and ensure all command are the proper "
                    "format")
                exit(1)
            rulesDict.update({item.upper(): itemDict})
    return rulesDict


def loadShoppingCart():
    cartDict = {}
    with open('shopping-cart.txt', 'r') as fp:
        for line in fp:
            cleanLine = line.strip().upper()

            # Item has already been seen increase the count
            if cleanLine in cartDict.keys():
                cartDict[cleanLine] = 1 + cartDict[cleanLine]
            # First time we see an item make a new entry
            else:
                cartDict[cleanLine] = 1
    return cartDict


def buildRecipt():
    pass


def displayRecipt():
    pass


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
        loadPriceRules()
        loadShoppingCart()
        buildRecipt()
        displayRecipt()
        endProgram = checkEndProgram()

    print('Program Ending')


if __name__ == '__main__':
    main()
