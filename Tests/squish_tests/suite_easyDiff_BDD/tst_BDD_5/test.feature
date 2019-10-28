Feature: DAS-166

    When visualising the experimental data,
    the users can show the coordinates,
    zoom in/out and reset the plot to its default state

    Scenario: Chart view interaction

         Given Application is open
         When A test file is loaded
         And Experimental Data tab open

		 # Assure chart shown
         Then Chart looks like the default

		 # peak coordinates shown
		 #
		 # UNDOABLE WITH QML
		 #
         #When A peak is clicked
         #Then Coordinates are shown

         # Zoom in
         When Chart is zoomed in
         Then Chart looks different than original

         # Reset
         When Right button clicked
         Then Chart looks like the default
