from userSettings.models import SettingsModel
from userSettings.classes import Settings

class SettingsManager():
    def addSettings(self, newSettings: Settings) -> bool:
        SettingsModel.objects.create(
            currency=newSettings.currency,
            cycle_duration=newSettings.cycle_duration,
            budget_threshold=newSettings.budget_threshold,
            language=newSettings.language,
            theme=newSettings.theme
        )
        return True
        

    def fetchSettings(self) -> Settings:
        settings = SettingsModel.objects.get(id=1)
        return self.createDataObject(settings.currency, settings.cycle_duration, settings.budget_threshold, settings.language, settings.theme)
    
    def updateSettings(self, newSettings: Settings) -> bool:
        SettingsModel.objects.filter(id=1).update(
            currency=newSettings.currency,
            cycle_duration=newSettings.cycle_duration,
            budget_threshold=newSettings.budget_threshold,
            language=newSettings.language,
            theme=newSettings.theme
        )
        return True
        
    def createDataObject(self, currency: str, cycle_duration: int, budget_threshold: int, language: str, theme: str): 
        return Settings(currency=currency,
                        cycle_duration=cycle_duration,
                        budget_threshold=budget_threshold,
                        language=language,
                        theme=theme)