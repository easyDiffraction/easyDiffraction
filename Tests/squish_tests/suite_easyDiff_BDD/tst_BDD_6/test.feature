Feature: DAS-168

	When visualising the structure of the sample model,
	the users can display qualitative information about the structure
	by clicking on “Symmetry and cell parameters”, ”Atoms,
	atomic coordinates and occupations.

    Scenario: Structural information

         Given Application is open
         When A test file is loaded
         And Structure tab open

		 # Symmetry and cell
         When Symmetry and cell parameters opened
         Then  Symmetry and cell information shown

         # Atoms, coordinates and occupation
         When Symmetry and cell parameters closed
         And Atoms, atomic coordinates and occupation opened
         Then Atomic coordinates section shown

         # Atomic displacement parameters
         When Atoms, atomic coordinates and occupation closed
         And Atomic displacement parameters opened
         Then Atomic displacement section shown

         # Magnetic susceptibility parameters
         When Atomic displacement parameter closed
         And Magnetic susceptibility parameters opened
         Then Magnetic susceptibility section shown