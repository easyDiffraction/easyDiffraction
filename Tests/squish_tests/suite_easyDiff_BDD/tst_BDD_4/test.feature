Feature: DAS-166

	When a file is opened, the content can be visualized
		as chart
		as structure and
		as text and the user can move to the next stage of analysis

    Scenario: Structure view interaction

         Given Application is open
         When A test file is loaded
         And Structure tab open

		# show the coordinates

		# rotate structure
         When Structure is rotated
         Then Structure looks rotated

         # go back
         When Structure is reset
         Then Structure looks the same

         # zoom in
         When Structure is zoomed
         Then Structure looks zoomed


