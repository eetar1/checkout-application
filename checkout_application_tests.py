import os
import unittest

import checkout_application as app


class Tests(unittest.TestCase):
    def test_one_item_success(self):
        with open('tests/test1-cart.txt', 'w+') as fp:
            fp.write("APPLE")
        with open('tests/test1-rules.txt', 'w+') as fp:
            fp.write(".75,APPLE")

        # There should be a rule for apple
        rules = app.loadPriceRules("tests/test1-rules.txt")
        assert len(rules.keys()) == 1
        assert 'APPLE' in rules.keys()
        assert rules.get('APPLE').get('PRICE') == .75
        # An apple should be in the cart
        items = app.loadShoppingCart('tests/test1-cart.txt')
        assert len(items.keys()) == 1
        assert 'APPLE' in rules.keys()
        assert items.get('APPLE') == 1

        price = 0.0
        for item in items.items():
            assert len(item) == 2
            price = app.computeLowestPrice(item, rules.get(item[0]))
        assert price == .75

        receipt = app.buildRecipt(items, rules)
        # One line item, total and the empty format entry
        assert len(receipt) == 3
        assert receipt[0] == 'APPLE x1 $0.75'
        assert receipt[1] == 'Total $0.75'

        os.remove('tests/test1-cart.txt')
        os.remove('tests/test1-rules.txt')

    def test_no_input_files_fail(self):
        with self.assertRaises(SystemExit) as cm:
            app.loadShoppingCart('')
        self.assertEqual(cm.exception.code, 1)

        with self.assertRaises(SystemExit) as cm:
            app.loadPriceRules('')
        self.assertEqual(cm.exception.code, 1)

    def test_invalid_commands_fail(self):
        # Test bad formatted command no price
        with open('tests/test3-rules.txt', 'w+') as fp:
            fp.write(",APPLE")

        with self.assertRaises(SystemExit) as cm:
            app.loadPriceRules('tests/test3-rules.txt')
        self.assertEqual(cm.exception.code, 1)

        os.remove('tests/test3-rules.txt')

        # Test no item
        with open('tests/test3-rules.txt', 'w+') as fp:
            fp.write(".75,")

        with self.assertRaises(SystemExit) as cm:
            app.loadPriceRules('tests/test3-rules.txt')
        self.assertEqual(cm.exception.code, 1)

        os.remove('tests/test3-rules.txt')

        # Test invalid XFY format
        with open('tests/test3-rules.txt', 'w+') as fp:
            fp.write("XFY,APPLE")

        with self.assertRaises(SystemExit) as cm:
            app.loadPriceRules('tests/test3-rules.txt')
        self.assertEqual(cm.exception.code, 1)

        os.remove('tests/test3-rules.txt')

        # Test negative price
        with open('tests/test3-rules.txt', 'w+') as fp:
            fp.write("-5,APPLE")

        with self.assertRaises(SystemExit) as cm:
            app.loadPriceRules('tests/test3-rules.txt')
        self.assertEqual(cm.exception.code, 1)

        os.remove('tests/test3-rules.txt')

        # Test price less than a penny
        with open('tests/test3-rules.txt', 'w+') as fp:
            fp.write("0.001,APPLE")

        with self.assertRaises(SystemExit) as cm:
            app.loadPriceRules('tests/test3-rules.txt')
        self.assertEqual(cm.exception.code, 1)

        os.remove('tests/test3-rules.txt')

    def test_apply_proms_success(self):
        # Test BOGO
        with open('tests/test4-cart.txt', 'w+') as fp:
            fp.write("APPLE\nAPPLE\nAPPLE\n")
        with open('tests/test4-rules.txt', 'w+') as fp:
            fp.write(".75,APPLE\nBOGO,APPLE")

        rules = app.loadPriceRules("tests/test4-rules.txt")
        assert len(rules.get('APPLE').keys()) == 2
        items = app.loadShoppingCart('tests/test4-cart.txt')

        price = 0.0
        # BOGO should apply and get one of the items for free
        for item in items.items():
            assert len(item) == 2
            price = app.computeLowestPrice(item, rules.get(item[0]))
        assert price == .75 * 2

        os.remove("tests/test4-rules.txt")

        # Test BO50
        with open('tests/test4-rules.txt', 'w+') as fp:
            fp.write(".75,APPLE\nBO50,APPLE")

        rules = app.loadPriceRules("tests/test4-rules.txt")
        assert len(rules.get('APPLE').keys()) == 2
        items = app.loadShoppingCart('tests/test4-cart.txt')

        price = 0.0
        # BOGO should apply and get one of the items for free
        for item in items.items():
            assert len(item) == 2
            price = app.computeLowestPrice(item, rules.get(item[0]))
        assert price == .75 + .75 * 1.5

        os.remove("tests/test4-cart.txt")
        os.remove("tests/test4-rules.txt")

    def test_xfy_worse_price_success(self):
        with open('tests/test5-cart.txt', 'w+') as fp:
            fp.write("APPLE\nAPPLE\nAPPLE\n")
        with open('tests/test5-rules.txt', 'w+') as fp:
            fp.write(".75,APPLE\n5F5,APPLE")
        price = 0.0

        rules = app.loadPriceRules("tests/test5-rules.txt")
        assert len(rules.get('APPLE').keys()) == 2
        items = app.loadShoppingCart('tests/test5-cart.txt')

        # XFY is providing a worse price ensure that the better price is taken
        for item in items.items():
            assert len(item) == 2
            price = app.computeLowestPrice(item, rules.get(item[0]))
        assert price == .75 * 3

        os.remove("tests/test5-rules.txt")
        os.remove("tests/test5-cart.txt")

    def test_capitalization_equal_success(self):
        with open('tests/test6-cart.txt', 'w+') as fp:
            fp.write('JUICE\n')
            fp.write('JUICe\n')
            fp.write('juice\n')

        items = app.loadShoppingCart('tests/test6-cart.txt')
        assert items.get('JUICE') == 3
        os.remove('tests/test6-cart.txt')

    def test_full_success(self):
        with open('tests/test7-cart.txt', 'w+') as fp:
            # Items do not have to be in order
            for x in range(300):
                fp.write("APPLE\n")
            for x in range(300):
                fp.write('JUICE\n')
            for x in range(301):
                fp.write("APPLE\n")

        with open('tests/test7-rules.txt', 'w+') as fp:
            fp.write(".75,APPLE\nBOGO,APPLE\n1,JUICE")
        items = app.loadShoppingCart('tests/test7-cart.txt')
        rules = app.loadPriceRules("tests/test7-rules.txt")
        receipt = app.buildRecipt(items, rules)

        # Assert all the prices are correct and all expected items are there
        assert receipt[0] == 'APPLE x601 $225.75'
        assert receipt[1] == 'JUICE x300 $300.00'
        assert receipt[2] == 'Total $525.75'

        os.remove('tests/test7-cart.txt')
        os.remove('tests/test7-rules.txt')


if __name__ == '__main__':
    unittest.main()
