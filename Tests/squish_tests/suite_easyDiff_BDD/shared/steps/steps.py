# -*- coding: utf-8 -*-

# A quick introduction to implementing scripts for BDD tests:
#
# This file contains snippets of script code to be executed as the .feature
# file is processed. See the section 'Behaviour Driven Testing' in the 'API
# Reference Manual' chapter of the Squish manual for a comprehensive reference.
#
# The decorators Given/When/Then/Step can be used to associate a script snippet
# with a pattern which is matched against the steps being executed. Optional
# table/multi-line string arguments of the step are passed via a mandatory
# 'context' parameter:
#
#   @When("I enter the text")
#   def whenTextEntered(context):
#      <code here>
#
# The pattern is a plain string without the leading keyword, but a couple of
# placeholders including |any|, |word| and |integer| are supported which can be
# used to extract arbitrary, alphanumeric and integer values resp. from the
# pattern; the extracted values are passed as additional arguments:
#
#   @Then("I get |integer| different names")
#   def namesReceived(context, numNames):
#      <code here>
#
# Instead of using a string with placeholders, a regular expression can be
# specified. In that case, make sure to set the (optional) 'regexp' argument
# to True.

import names
import time

@Given("Application is open")
def step(context):
    startApplication("easyDiffraction")
    mouseClick(waitForObject(names.analysis_Button), 100, 19, Qt.LeftButton)
    test.compare(waitForObjectExists(names.easyDiffraction_QQuickApplicationWindow).visible, True)


@Then("User can open a new project")
def step(context):
    moveWindow(waitForObject(names.easyDiffraction_QQuickApplicationWindow), -380, -188)
    test.compare(waitForObjectExists(names.easyDiffraction_Open_another_project_Button).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Open_another_project_Button).enabled, True)


@Then("User can open help file")
def step(context):
    moveWindow(waitForObject(names.easyDiffraction_QQuickApplicationWindow), -17, -48)
    mouseClick(waitForObject(names.easyDiffraction_image_IconImage_4), 9, 11, Qt.LeftButton)
    mouseClick(waitForObject(names.easyDiffraction_Text_6))
    test.compare(waitForObjectExists(names.easyDiffraction_Button).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Button).enabled, True)

@Then("User can report a bug")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Button_2).enabled, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Button_2).visible, True)


@When("A test file is loaded")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_Text_7))
    mouseClick(waitForObject(names.easyDiffraction_Open_another_project_Button), 129, 26, Qt.LeftButton)
    # Workaround for Windows not having the right winhook.dll
    snooze(2) 
    nativeType("main.cif")
    snooze(1)
    nativeType("<Return>")
    snooze(1)
    # end of workaround    
    #test.compare(str(waitForObjectExists(names.easyDiffraction_Fe3O4_Text).text), "Fe3O4")

@When("Structure tab open")
def step(context):
    mouseClick(waitForObject(names.tabBar_Home_Button), 147, 20, Qt.LeftButton)
    mouseClick(waitForObject(names.easyDiffraction_Text_3))    
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_5))

@When("Chart tab open")
def step(context):
    mouseClick(waitForObject(names.tabBar_Home_Button), 147, 20, Qt.LeftButton)
    mouseClick(waitForObject(names.easyDiffraction_Text_3))    
    #mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_6))

@When("Fitting tab open")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_Experimental_Data_Button), 334, 21, Qt.LeftButton)
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_5))
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_7))

@When("First parameter checked")
def step(context):
    test.compare(waitForObjectExists(names.contentRow_CheckBox).checked, True)

@Then("Fit button enabled")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Start_fitting_Button).enabled, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Start_fitting_Button).text), "Start fitting")
"""
@When("Program Preferences opened")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_Program_Preferences_Button), 7, 25, Qt.LeftButton)

@Then("Two options are visible")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Show_Animated_Intro_CheckBox).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Show_Animated_Intro_CheckBox).text), "Show Animated Intro")
    test.compare(waitForObjectExists(names.easyDiffraction_Show_User_Guides_CheckBox).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Show_User_Guides_CheckBox).text), "Show User Guides")

@Then("user can select Show Animated Intro")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Show_Animated_Intro_CheckBox).checkable, True)

@Then("user can select Show User Guides")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Show_User_Guides_CheckBox).checkable, True)
"""

@Then("Home page has textual information")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Fe3O4_Text).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Fe3O4_Text).text), "Fe3O4")
    test.compare(waitForObjectExists(names.easyDiffraction_Text_7).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Text_7).text), "Keywords: neutron diffraction, powder, 1d\nPhases: Fe3O4\nExperiments: pnd\nInstrument: 6T2 at LLB\nModified: 23 Oct 2019, 13:37:24")

@When("Selected Experimental Data tab")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_6))

@Then("Chart should be active")
def step(context):
    test.compare(waitForObjectExists(names.tabBar_Experimental_Data_Button).checked, True)
    test.compare(waitForObjectExists(names.tabBar_Experimental_Data_Button).enabled, True)


@Then("Chart should be visible")
def step(context):
    test.vp("VP1")

@Then("Chart Table View should be present")
def step(context):
    mouseClick(waitForObject(names.tabBar_label_MnemonicLabel))
    test.compare(str(waitForObjectExists(names.headerTableView_x_Text).text), "x")
    test.compare(waitForObjectExists(names.headerTableView_x_Text).visible, True)
    test.compare(waitForObjectExists(names.headerTableView_y_obs_up_Text).visible, True)
    test.compare(str(waitForObjectExists(names.headerTableView_y_obs_up_Text).text), "y_obs_up")
    test.compare(str(waitForObjectExists(names.headerTableView_sy_obs_up_Text).text), "sy_obs_up")
    test.compare(waitForObjectExists(names.headerTableView_sy_obs_up_Text).visible, True)
    test.compare(str(waitForObjectExists(names.contentTableView_TextInput).text), "585.0554")
    test.compare(waitForObjectExists(names.contentTableView_TextInput).visible, True)

@Then("Chart Text View should be present")
def step(context):
    test.compare(str(waitForObjectExists(names.tabBar_Text_View_TabButton).text), "Text View")
    test.compare(waitForObjectExists(names.tabBar_Text_View_TabButton).visible, True)

@When("Selected Sample Model tab")
def step(context):
    mouseClick(waitForObject(names.tabBar_Home_Button), 214, 27, Qt.LeftButton)
    mouseClick(waitForObject(names.easyDiffraction_Text_3))
    mouseClick(waitForObject(names.tabBar_Plot_View_TabButton), 157, 9, Qt.LeftButton)
    mouseClick(waitForObject(names.easyDiffraction_Text_8))

@Then("Structure should be active")
def step(context):
    test.compare(str(waitForObjectExists(names.tabBar_Structure_View_TabButton).text), "Structure View")
    test.compare(waitForObjectExists(names.tabBar_Structure_View_TabButton).visible, True)

@Then("Structure should be visible")
def step(context):
    test.vp("VP2")

@Then("Structure Text View should be present")
def step(context):
    mouseClick(waitForObject(names.tabBar_Text_View_TabButton), 95, 18, Qt.LeftButton)
    test.compare(str(waitForObjectExists(names.tabBar_Text_View_TabButton).text), "Text View")
    test.compare(waitForObjectExists(names.tabBar_Text_View_TabButton).visible, True)

@Then("Analysis button enabled")
def step(context):
    mouseClick(waitForObject(names.tabBar_Structure_View_TabButton), 48, 20, Qt.LeftButton)
    test.compare(waitForObjectExists(names.easyDiffraction_Button).enabled, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Button).text), "Analysis")
    test.compare(waitForObjectExists(names.easyDiffraction_Button).visible, True)


@When("Structure is rotated")
def step(context):
    mouseDrag(waitForObject(names.easyDiffraction_chart_QtDataVisualization_DeclarativeScatter), 501, 277, 252, 406, Qt.NoModifier, Qt.RightButton)


@When("Structure is reset")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_chart_QtDataVisualization_DeclarativeScatter), 494, 302, Qt.LeftButton)

@Then("Structure looks the same")
def step(context):
    test.vp("VP2")

@Then("Structure looks rotated")
def step(context):
    test.vp("VP1")

@Then("Structure looks different than original")
def step(context):
    test.vp("VP3")  # same structure as VP2 but with eception selected


@When("Structure is zoomed")
def step(context):
    mouseWheel(waitForObject(names.easyDiffraction_chart_QtDataVisualization_DeclarativeScatter), 494, 302, 0, -100, Qt.NoModifier)
    


@When("Program Preferences opened")
def step(context):
    moveWindow(waitForObject(names.easyDiffraction_QQuickApplicationWindow), 33, -226)
    mouseClick(waitForObject(names.easyDiffraction_image_IconImage_6), 5, 10, Qt.LeftButton)

@Then("user can select Show Animated Intro")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Show_Animated_Intro_CheckBox).checkable, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_Animated_Intro_CheckBox).checked, False)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_Animated_Intro_CheckBox).visible, True)

@Then("user can select Show User Guides")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Show_User_Guides_CheckBox).checkable, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_User_Guides_CheckBox).checked, False)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_User_Guides_CheckBox).visible, True)


@Then("Two options are visible")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_ColumnLayout_2).implicitHeight, 66)


@Then("Structure looks zoomed")
def step(context):
    test.vp("VP4")


@When("Experimental Data tab open")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_Text_3))

@Then("Chart looks like the default")
def step(context):
    test.vp("VP1")

@When("A peak is clicked")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 482, 363, Qt.LeftButton)

@Then("Coordinates are shown")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 483, 363, Qt.LeftButton)

@When("Chart is zoomed in")
def step(context):
    mouseWheel(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 384, 297, 0, 135, Qt.NoModifier)
    mouseClick(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 384, 297, Qt.LeftButton)
    mouseDrag(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 156, 285, 389, 258, Qt.NoModifier, Qt.LeftButton)

@Then("Chart looks different than original")
def step(context):
    test.vp("VP2")

@When("Right button clicked")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 414, 287, Qt.RightButton)


@When("Symmetry and cell parameters opened")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_image_IconImage_7), 5, 5, Qt.LeftButton)

@Then("Symmetry and cell information shown")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_TextField).enabled, False)
    test.compare(waitForObjectExists(names.easyDiffraction_TextField).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_TextField).text), "cubic")
    test.compare(waitForObjectExists(names.easyDiffraction_TextField_2).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_TextField_2).displayText), "227.  Fd-3m")
    test.compare(waitForObjectExists(names.easyDiffraction_TextField_2).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_TextField_3).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_TextField_3).displayText), "2")
    test.compare(waitForObjectExists(names.easyDiffraction_TextField_3).visible, True)
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_8_5500_Text).text), "8.5500")
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text_2).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_8_5500_Text_2).text), "8.5500")
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text_2).visible, True)
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text_3).enabled, True)
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text_3).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_8_5500_Text_3).text), "8.5500")
    test.compare(waitForObjectExists(names.contentRow_90_0000_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_90_0000_Text).text), "90.0000")
    test.compare(waitForObjectExists(names.contentRow_90_0000_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_90_0000_Text_2).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_90_0000_Text_2).text), "90.0000")
    test.compare(waitForObjectExists(names.contentRow_90_0000_Text_2).visible, True)

@When("Symmetry and cell parameters closed")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_image_IconImage_8), 3, 6, Qt.LeftButton)

@When("Atoms, atomic coordinates and occupation opened")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_image_IconImage_9), 3, 4, Qt.LeftButton)

@Then("Atomic coordinates section shown")
def step(context):
    test.compare(waitForObjectExists(names.contentRow_Fe3A_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Fe3A_Text).text), "Fe3A")
    test.compare(waitForObjectExists(names.contentRow_Fe3A_Text).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_Fe3B_Text).text), "Fe3B")
    test.compare(waitForObjectExists(names.contentRow_Fe3B_Text).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_O1_Text).text), "O1")
    test.compare(waitForObjectExists(names.contentRow_O1_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Color_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Color_Text).text), "Color")
    test.compare(waitForObjectExists(names.easyDiffraction_Color_Text).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_Rectangle).color.name), "#7ab03c")
    test.compare(waitForObjectExists(names.contentRow_Rectangle).color.red, 122)
    test.compare(waitForObjectExists(names.contentRow_Rectangle).color.green, 176)
    test.compare(waitForObjectExists(names.contentRow_Rectangle).color.blue, 60)
    test.compare(waitForObjectExists(names.contentRow_Rectangle).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Text_8).text), "0.1250")
    test.compare(waitForObjectExists(names.easyDiffraction_Text_8).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Text_8).enabled, True)
    test.compare(waitForObjectExists(names.contentRow_1_0000_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_1_0000_Text).text), "1.0000")
    test.compare(waitForObjectExists(names.contentRow_1_0000_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_button_Button).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Add_new_atom_Button).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Add_new_atom_Button).text), "Add new atom")
    test.compare(waitForObjectExists(names.easyDiffraction_Add_new_atom_Button).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Remove_all_atoms_Button).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Remove_all_atoms_Button).text), "Remove all atoms")
    test.compare(waitForObjectExists(names.easyDiffraction_Remove_all_atoms_Button).visible, True)

@When("Atoms, atomic coordinates and occupation closed")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_image_IconImage_8), 4, 0, Qt.LeftButton)

@When("Atomic displacement parameters opened")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_image_IconImage_6), 5, 2, Qt.LeftButton)

@Then("Atomic displacement section shown")
def step(context):
    test.compare(str(waitForObjectExists(names.easyDiffraction_Label_Text).text), "Label")
    test.compare(waitForObjectExists(names.easyDiffraction_Label_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Label_Text).enabled, False)
    test.compare(waitForObjectExists(names.easyDiffraction_Type_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Type_Text).text), "Type")
    test.compare(waitForObjectExists(names.easyDiffraction_Type_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Uiso_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Uiso_Text).text), "Uiso")
    test.compare(waitForObjectExists(names.easyDiffraction_Uiso_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_U11_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_U11_Text).text), "U11")
    test.compare(waitForObjectExists(names.easyDiffraction_U11_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_U23_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_U23_Text).text), "U23")
    test.compare(waitForObjectExists(names.easyDiffraction_U23_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_1_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_1_Text).text), "1")
    test.compare(waitForObjectExists(names.contentRow_1_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Fe3A_Text_2).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Fe3A_Text_2).text), "Fe3A")
    test.compare(waitForObjectExists(names.contentRow_Fe3A_Text_2).visible, True)
    test.compare(waitForObjectExists(names.contentRow_uani_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_uani_Text).text), "uani")
    test.compare(waitForObjectExists(names.contentRow_uani_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_0_0000_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_0_0000_Text).text), "0.0000")
    test.compare(waitForObjectExists(names.contentRow_0_0000_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_O1_Text_2).enabled, True)
    test.compare(waitForObjectExists(names.contentRow_O1_Text_2).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_O1_Text_2).text), "O1")
    test.compare(waitForObjectExists(names.contentRow_0_0000_Text_2).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_0_0000_Text_2).text), "0.0000")
    test.compare(waitForObjectExists(names.contentRow_0_0000_Text_2).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Text).text), "")
    test.compare(waitForObjectExists(names.contentRow_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Text_2).enabled, True)
    test.compare(waitForObjectExists(names.contentRow_Text_2).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_Text_2).text), "")

@When("Atomic displacement parameter closed")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_image_IconImage_8), 5, 5, Qt.LeftButton)

@When("Magnetic susceptibility parameters opened")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_image_IconImage_10), 5, 4, Qt.LeftButton)

@Then("Magnetic susceptibility section shown")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_iso_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_iso_Text).text), "χiso")
    test.compare(waitForObjectExists(names.easyDiffraction_iso_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_23_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_23_Text).text), "χ23")
    test.compare(waitForObjectExists(names.easyDiffraction_23_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_2_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_2_Text).text), "2")
    test.compare(waitForObjectExists(names.contentRow_2_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Text_3).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Text_3).text), "")
    test.compare(waitForObjectExists(names.contentRow_Text_3).visible, True)
    test.compare(waitForObjectExists(names.contentRow_0_0000_Text_3).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_0_0000_Text_3).text), "0.0000")
    test.compare(waitForObjectExists(names.contentRow_0_0000_Text_3).visible, True)
    test.compare(waitForObjectExists(names.contentRow_O1_Text_3).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_O1_Text_3).text), "O1")
    test.compare(waitForObjectExists(names.contentRow_O1_Text_3).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Text_4).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Text_4).text), "")
    test.compare(waitForObjectExists(names.contentRow_Text_4).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Text_5).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Text_5).text), "")
    test.compare(waitForObjectExists(names.contentRow_Text_5).visible, True)


@When("Analysis tab is open")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_Experimental_Data_Button), 318, 23, Qt.LeftButton)
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_5))
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_7))

@Then("Fitting chart is visible")
def step(context):
    test.vp("VP1")

@Then("Difference chart is visible")
def step(context):
    test.vp("VP2")

@When("Parameter 1 value is changed")
def step(context):
    mouseClick(waitForObject(names.contentRow_qwe_TextInput), 35, 19, Qt.LeftButton)
    type(waitForObject(names.contentRow_qwe_TextInput), "<Backspace>")
    type(waitForObject(names.contentRow_qwe_TextInput), "11")
    type(waitForObject(names.contentRow_qwe_TextInput), "<Return>")

@Then("Its shown value is changed")
def step(context):
    test.compare(str(waitForObjectExists(names.contentRow_qwe_TextInput).text), "11.5500")

@Then("The fitting chart looks different")
def step(context):
    test.vp("VP3")

@When("Parameter value slider is moved")
def step(context):
    longMouseDrag(waitForObject(names.easyDiffraction_sliderHandle_Rectangle), 8, 15, -9, 1, Qt.NoModifier, Qt.LeftButton)
    time.sleep(2.0)
    #if waitFor("names.contentRow_qwe_TextInput.text == 8.7176", 2000):
    #    test.passes("Property had the expected value")
    #else:
    #    test.fail("Property did not have the expected value")

@Then("Parameter value is changed")
def step(context):
    test.compare(str(waitForObjectExists(names.contentRow_qwe_TextInput).text), "10.0205")


@Then("The fitting chart looks different 2")
def step(context):
    test.vp("VP4")
