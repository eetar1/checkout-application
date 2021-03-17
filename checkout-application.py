def loadPriceRules():
    pass


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
