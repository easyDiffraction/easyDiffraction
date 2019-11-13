Feature: DAS-171

    When a fitting is performed, the results can be viewed and saved

    Scenario: Fit results

        Given Application is open
        When A test file is loaded
        And Analysis tab is open
        And Fitting started
        Then Wait for fitting finished

        When Fitting finished
        Then Fitting details are shown
        And Optimized parameters are displayed
        And Error for optimized parameters is displayed
        And Fitting can be performed

		When Summary tab is open
		Then Text report is available
		And Export report is available

       When Analysis tab is open
       And All parameters are deselected
       Then Wait for bad fitting finished

