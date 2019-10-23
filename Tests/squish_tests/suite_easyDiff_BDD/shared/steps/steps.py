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


@Given("File is loaded")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_Text_7))
    mouseClick(waitForObject(names.easyDiffraction_Open_another_project_Button), 129, 26, Qt.LeftButton)
    # Workaround for Windows not having the right winhook.dll
    snooze(5) 
    nativeType("main.rcif")
    snooze(1)
    nativeType("<Return>")
    snooze(1)
    # end of workaround    
    test.compare(str(waitForObjectExists(names.easyDiffraction_Fe3O4_Text).text), "Fe3O4")

@When("Structure tab open")
def step(context):
    mouseClick(waitForObject(names.tabBar_Home_Button), 147, 20, Qt.LeftButton)
    mouseClick(waitForObject(names.easyDiffraction_Text_3))    
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_5))

@Then("Structure should be visible")
def step(context):
    test.vp("VP1")


@When("Chart tab open")
def step(context):
    mouseClick(waitForObject(names.tabBar_Home_Button), 147, 20, Qt.LeftButton)
    mouseClick(waitForObject(names.easyDiffraction_Text_3))    
    #mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_6))

@Then("Chart should be visible")
def step(context):
    test.vp("VP2")


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
