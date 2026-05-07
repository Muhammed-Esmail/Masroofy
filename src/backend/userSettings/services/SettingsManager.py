from userSettings.models import SettingsModel
from userSettings.classes import Settings

class SettingsManager():
    """
    A service class for managing global application settings and user preferences.

    This manager handles the persistence and retrieval of configuration data such 
    as currency, theme, and budget thresholds. It assumes a single-user 
    configuration model where settings are stored in a primary record.
    """

    def addSettings(self, newSettings: Settings) -> bool:
        """
        Creates a new settings record in the database.

        Args:
            newSettings (Settings): The settings data object containing 
                preferences to be saved.

        Returns:
            bool: True if the record was successfully created.
        """
        SettingsModel.objects.create(
            currency=newSettings.currency,
            cycle_duration=newSettings.cycle_duration,
            budget_threshold=newSettings.budget_threshold,
            language=newSettings.language,
            theme=newSettings.theme
        )
        return True

    def fetchSettings(self) -> Settings:
        """
        Retrieves the primary application settings record.

        Note:
            This method specifically looks for the record with ID 1.

        Returns:
            Settings: A business object populated with the user preferences.

        Raises:
            SettingsModel.DoesNotExist: If the settings record has not been 
                initialized in the database.
        """
        settings = SettingsModel.objects.get(id=1)
        return self.createDataObject(
            settings.currency, 
            settings.cycle_duration, 
            settings.budget_threshold, 
            settings.language, 
            settings.theme
        )
    
    def updateSettings(self, newSettings: Settings) -> bool:
        """
        Updates the primary settings record with new values.

        Args:
            newSettings (Settings): The updated data object to apply.

        Returns:
            bool: True if the update operation was executed.
        """
        SettingsModel.objects.filter(id=1).update(
            currency=newSettings.currency,
            cycle_duration=newSettings.cycle_duration,
            budget_threshold=newSettings.budget_threshold,
            language=newSettings.language,
            theme=newSettings.theme
        )
        return True
        
    def createDataObject(
        self, 
        currency: str, 
        cycle_duration: int, 
        budget_threshold: int, 
        language: str, 
        theme: str
    ) -> Settings: 
        """
        Factory method to convert database fields into a Settings business object.

        Args:
            currency (str): The chosen currency symbol or code.
            cycle_duration (int): Length of the budget cycle in days.
            budget_threshold (int): Percentage at which to trigger alerts.
            language (str): User's preferred UI language.
            theme (str): UI theme identifier (e.g., 'Dark', 'Light').

        Returns:
            Settings: A populated Settings object.
        """
        return Settings(
            currency=currency,
            cycle_duration=cycle_duration,
            budget_threshold=budget_threshold,
            language=language,
            theme=theme
        )