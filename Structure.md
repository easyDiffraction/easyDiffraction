* **Qml.qmlproject** (QML project file for QtCreator to see the whole QML structure)
* **Cpp.pro** (C++ project file for QtCreator, e.g. to simplify creation of QmlResource.qrc)
* **Python.pyproject** (Python project file for QtCreator to see the python logic and main QML file)
* **App**
	* **easyDiffraction.py** (Main Python file to run easyDiffraction; creates app; loads gui, imports, etc.)
	* **RhoChiQml.py** (Python proxy between RhoChi library and QML gui)
	* **Gui.qml** (Main QML gui file; contains ApplicationWindow: Toolbar, ContentArea, etc.; loads settings)
	* **Imports** (All the QML related stuff)
		* **easyDiffraction** (diffraction-dependent / specific)
			* **Settings.qml** (appName, appVersion, appUrl, etc.)
			* **Variables.qml**
			* **Resources**
				* **Examples** (Fe3O4\_6T2\_0T\_powder\_1d, etc.)
				* **Icons** (App.icns, App.ico, etc.)
		* **easyAnalysis** (technique-independent / generic)
			* **Logic** (Some JavaScript files used for GUI prototype; should not be used in Python-based project)
			* **Resources**
				* **Style.qml** (GUI style file: colors, dimentions, fonts, etc.)
				* **Variables.qml** (toolbarCurrentIndex, etc.)
				* **Fonts** (Fonts used in GUI - to be independent on system fon ts)
				* **Icon** (Icons used in GUI)
			* **App**
				* **Intro.qml** (Introduction screen with animation when program is just started)
				* **Elements** (Different custom QML elements used in different parts of GUI, e.g. GroupBox, ParametersTable, etc.)
				* **Menubar** (Currently not in use)
				* **Toolbar** (Application toolbar with button to switch between the workflow steps, e.g. Experimental Data, Sample Model, Analysis, etc.)
					* **Toolbar.qml** (Realisation of toolbar, based on TabBar)
					* **Button.qml** (Custom base-button for Toolbar)  
					* **Buttons** (Custom Toolbar buttons, based on **Button.qml**. E.g. Home.qml, ExperimentalData.qml, etc.)
				* **ContentArea** (The rest of application window, without toolbar. It contains MainArea and Sidebar)
					* **ContentArea.qml** (Realisation of ContentArea, based on StackLayout)
					* **Button.qml** (Custom base-button for both MainArea and Sidebar)
					* **Buttons** (Custom Toolbar buttons, based on **Button.qml**. E.g. Add.qml, Save.qml, Remove.qml)
					* **MainArea** (Application main area)
						* **Pages** (Different main area states: Home, ExperimentalData, etc.)
							* **Home**
								* **Project.qml**
							* **ExperimentalData**
								* **PlotView.qml**
								* **TableView.qml**
								* **TextView.qml**
							* **SampleModel**
								* **StructureView.qml**
								* **TextView.qml**
							* **Analysis**
								* **Fitting.qml** 
								* **Constraints.qml** 
								* **Editor.qml** 
							* **Summary**
								* **Logbook.qml** 
					* **Sidebar** (Application sidebar)
						* **Pages** (Different sidebar states: Home, ExperimentalData, etc.)
							* **Home**
								* ... 
							* **ExperimentalData**
								* ... 
							* **SampleModel**
								* **StructureView.qml**
								* **TextView.qml**
								* **StructureView**
									* **Controls** (Basic controls sidebar tab)
									* **Settings** (Advanced controls sidebar tab)
								* **TextView**
									* **Controls** (Basic controls sidebar tab)
									* **Settings** (Advanced controls sidebar tab)
							* **Analysis**
								* ... 
							* **Summary**
								* ... 
