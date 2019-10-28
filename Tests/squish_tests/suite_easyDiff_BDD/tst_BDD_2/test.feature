Feature: Settings access

	When the users open easyDiffraction,
	they can click on Program Preferences and
	customise the settings of the tooltips

    DAS-164


    Scenario: Settings can be accessed

        Given Application is open

         When Program Preferences opened
         Then Two options are visible
         And user can select Show Animated Intro
         And user can select Show User Guides


