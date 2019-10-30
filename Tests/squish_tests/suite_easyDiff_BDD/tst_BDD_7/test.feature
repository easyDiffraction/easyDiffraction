Feature: DAS-169

	When a file is opened and a fittable parameter is checked,
	the value of the parameter can be changed live and its
	influence on the diffraction spectrum displayed.

    Scenario: Response to fittable changes

         Given Application is open
         When A test file is loaded
         And Analysis tab is open

         Then Fitting chart is visible
         And Difference chart is visible

         When Parameter 1 value is changed
         Then Its shown value is changed
         And The fitting chart looks different

         When Parameter value slider is moved
         Then Parameter value is changed
         And The fitting chart looks different 2



