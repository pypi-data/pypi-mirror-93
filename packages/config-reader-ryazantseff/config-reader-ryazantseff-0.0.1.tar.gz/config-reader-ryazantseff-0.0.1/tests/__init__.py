import asyncio, logging, unittest
from config_reader import Config

class MyTest(unittest.TestCase):
    def setUp(self):
        Config(path='/root/tests/config.json')

    def tearDown(self):
        Config.drop()
   
    def test_config1(self):
        Config().put('field1', 'value1')
        self.assertEqual(Config().get('field1'), 'value1')
        Config().put('field1', 'value2')
        self.assertEqual(Config().get('field1'), 'value2')
        Config().put('field2', 'value4')
        self.assertEqual(Config().get('field2'), 'value4')
        Config().writeCfg()

class MyTest2(unittest.TestCase):
    def setUp(self):
        Config(path='/root/tests/config.json')

    def tearDown(self):
        Config.drop()

    def test_config2(self):
        self.assertEqual(Config().get('field2'), 'value4')
        Config().put('field3', 'value5')
        Config().put('field3', 'description', field='desc')
        self.assertEqual(Config().get('field3'), 'value5')
        self.assertEqual(Config().get('field3', field='desc'), 'description')
        Config().writeCfg()


class MyTest3(unittest.TestCase):
    def setUp(self):
        Config(path='/root/tests/config.json')

    def tearDown(self):
        Config.drop()

    def test_config3(self):
        Config().delete('field3')
        Config().writeCfg()


if __name__ == '__main__':
    unittest.main()
