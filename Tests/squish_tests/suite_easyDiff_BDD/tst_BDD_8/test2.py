Feature: DAS-170
Feature: DAS-170

    When a file is opened and a fittable parameter is checked,
    fitting can be performed

    Scenario: Fittability

        Given Application is open
        When A test file is loaded
        And Analysis tab is open

        Then Default parameters are checked for fitting
        And Error values are not present
        And Fitting can be performed 




