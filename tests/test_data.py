import unittest
import os
import battlenet

PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')

battlenet.Connection.setup(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY, eventlet=True)


class DataTest(unittest.TestCase):
    pass
        
if __name__ == '__main__':
    unittest.main()
