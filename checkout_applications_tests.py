import checkout_application as app

def test_one_item_success():
    with open("tests/test1-cart.txt") as fp:
        fp.write("APPLE")
    with open("tests/test1-rules.txt") as fp:
        fp.write(".75,APPLE")
