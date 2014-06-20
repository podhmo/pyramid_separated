# -*- coding:utf-8 -*-
import unittest
import os.path

HERE = os.path.abspath(os.path.dirname(__file__))


class Tests(unittest.TestCase):
    def _getCommonIniFilePath(self):
        return os.path.join(HERE, "common.ini")

    def setUp(self):
        common_ini_path = self._getCommonIniFilePath()
        if os.path.exists(common_ini_path):
            os.remove(common_ini_path)

        with open(common_ini_path, "w") as wf:
            wf.write("""\
[common]
sqlalchemy.url = sqlite://
extra.option = common
""")

    def test_it(self):
        from pyramid.testing import testConfig
        settings = {
            "sqlalchemy.url": "sqlite:///tmp/foo.db",
            "common.inifile": self._getCommonIniFilePath()
        }

        with testConfig(settings=settings) as config:
            config.include("pyramid_separated")

            self.assertNotIn("extra.option", config.registry.settings)

            config.add_config_file("common.inifile", category="common", overwrite=False)

            self.assertEqual(config.registry.settings["sqlalchemy.url"], "sqlite:///tmp/foo.db")
            self.assertIn("extra.option", config.registry.settings)

    def test_it__with_overwrite_true(self):
        from pyramid.testing import testConfig

        settings = {
            "sqlalchemy.url": "sqlite:///tmp/foo.db",
            "common.inifile": self._getCommonIniFilePath()
        }

        with testConfig(settings=settings) as config:
            config.include("pyramid_separated")
            config.add_config_file("common.inifile", category="common", overwrite=True)
            self.assertEqual(config.registry.settings["sqlalchemy.url"], "sqlite://")

    def test_it__config_file_is_not_found__raise_configration_error(self):
        from pyramid.testing import testConfig
        from pyramid.exceptions import ConfigurationError

        settings = {
            "sqlalchemy.url": "sqlite:///tmp/foo.db",
            "common.inifile": "/dummy/notfound.ini"
        }

        with testConfig(settings=settings) as config:
            config.include("pyramid_separated")

            with self.assertRaises(ConfigurationError):
                config.add_config_file("common.inifile", category="common", overwrite=False)
