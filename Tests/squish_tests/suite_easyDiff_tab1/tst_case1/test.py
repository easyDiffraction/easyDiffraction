# -*- coding: utf-8 -*-

import names

def main():
    startApplication("easyDiffraction")
    mouseClick(waitForObject(names.label_MnemonicLabel))
    test.compare(str(waitForObjectExists(names.easyDiffraction_No_Project_Created_Opened_Text).text), "No Project Created/Opened")
    test.compare(waitForObjectExists(names.easyDiffraction_No_Project_Created_Opened_Text).visible, True)
    mouseClick(waitForObject(names.o_Rectangle), 915, 620, Qt.LeftButton)
    mouseClick(waitForObject(names.analysis_Button), 102, 30, Qt.LeftButton)
    #mouseClick(waitForObject(names.easyDiffraction_image_IconImage), 3, 5, Qt.LeftButton)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_Animated_Intro_CheckBox).checked, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_Animated_Intro_CheckBox).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_User_Guides_CheckBox).checked, False)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_User_Guides_CheckBox).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Examples_Button).enabled, False)
    test.compare(waitForObjectExists(names.easyDiffraction_Recent_Projects_Button).enabled, False)
    test.compare(waitForObjectExists(names.easyDiffraction_Experimental_Data_Button).enabled, False)
