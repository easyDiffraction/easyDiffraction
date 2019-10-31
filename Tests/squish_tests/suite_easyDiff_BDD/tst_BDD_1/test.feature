# This is a sample .feature file
# Squish feature files use the Gherkin language for describing features, a short example
# is given below. You can find a more extensive introduction to the Gherkin format at
# https://github.com/cucumber/cucumber/wiki/Gherkin
Feature: Check of the initial state

On start, the application should open the main window

    Scenario: Open application and make sure all elements are present

        Given Application is open
         Then User can open a new project
          And User can open help file
          And User can report a bug


