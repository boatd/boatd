import os

import boatd


class TestDriver(object):
    def setup(self):
        self.directory, _ = os.path.split(__file__)

        configuration = {
            'scripts': {
                'driver': os.path.join(self.directory, 'driver.py')
            }
        }
        self.mock_config = boatd.Config(configuration)

        self.driver_file = os.path.join(self.directory,
            self.mock_config.scripts.driver)

    def test_driver_file(self):
        assert os.path.isfile(self.driver_file)

    def test_loading_driver(self):
        assert boatd.load_driver(self.mock_config)

    def test_pony_exists(self):
        driver = boatd.load_driver(self.mock_config)
        assert driver.handlers.get('pony')

    def test_pony_runs(self):
        driver = boatd.load_driver(self.mock_config)
        pony = driver.handlers.get('pony')
        assert pony() == 'magic'

    def test_heading(self):
        driver = boatd.load_driver(self.mock_config)
        heading = driver.handlers.get('heading')
        assert heading() == 2.43

    def test_handler_decorators(self):
        driver = boatd.load_driver(self.mock_config)

        @driver.handler('test_handler_decorators')
        def test():
            return 'test passed'

        func = driver.handlers.get('test_handler_decorators')
        assert func() == 'test passed'

    def test_empty_hardware(self):
        driver = boatd.load_driver(self.mock_config)
        assert len(driver.some_hardware) == 0

    def test_set_rudder(self):
        driver = boatd.load_driver(self.mock_config)
        rudder = driver.handlers.get('rudder')
        rudder(10)
        assert driver.some_hardware.get('rudder') == 10

    def test_set_rudder_multiple(self):
        driver = boatd.load_driver(self.mock_config)
        rudder = driver.handlers.get('rudder')
        rudder(20)
        rudder(-10)
        assert driver.some_hardware.get('rudder') == -10

    def test_bad_driver(self):
        self.mock_config.scripts.driver = os.path.join(self.directory,
                                                       'bad_driver.py')
        try:
            driver = boatd.load_driver(self.mock_config)
        except SyntaxError:
            pass
        except Exception as e:
            assert False, 'An exception other than SyntaxError was raised: {}'.format(e)
        else:
            assert False, 'No exception was raised'
