from typing import override
from django.test import TestCase
from dashboard.classes import Settings
from dashboard.services import SettingsManager

class testSettingsManager(TestCase):
    @override
    def setUp(self):
        self.sample_settings = Settings(
            'EGP',
            10,
            100,
            'AR',
            'DARK'
        )
        self.settings_manager = SettingsManager()
        
    def test_create_settings(self):
        self.settings_manager.addSettings(self.sample_settings)
        settings = self.settings_manager.fetchSettings()
        return self.assertEqual(settings.currency, self.sample_settings.currency)
        
    def test_update_settings(self):
        self.settings_manager.addSettings(self.sample_settings)
        sample_settings_2 = Settings(
            'EGP',
            10,
            100,
            'AR',
            'LIGHT'
        )
        
        self.settings_manager.updateSettings(sample_settings_2)
        
        settings = self.settings_manager.fetchSettings()
        return self.assertEqual(settings.theme, sample_settings_2.theme)