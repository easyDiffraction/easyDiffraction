Feature: DAS-165

	When a file is opened, the content can be visualized
		as chart
		as structure and
		as text and the user can move to the next stage of analysis

    Scenario: Open a file and check the views on it

        Given Application is open
         When A test file is loaded

         Then Home page has textual information

		 # Experimental data tab
         When Selected Experimental Data tab
         Then Chart should be active
         And Chart should be visible
         And Chart Table View should be present
         And Chart Text View should be present

         # Sample Model tab
         When Selected Sample Model tab
         Then Structure should be active
         And Structure should be visible
         And Structure Text View should be present

 		# further analysis
 		And Analysis button enabled

