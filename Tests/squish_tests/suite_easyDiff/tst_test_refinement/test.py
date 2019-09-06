# -*- coding: utf-8 -*-

import names

def main():
    startApplication("easyDiffraction")
    mouseClick(waitForObject(names.analysis_Button_2), 110, 26, Qt.LeftButton)    
    mouseClick(waitForObject(names.easyDiffraction_Open_another_project_Button), 129, 26, Qt.LeftButton)
    # Workaround for Windows not having the right winhook.dll
    snooze(5) 
    nativeType("full.rcif")
    snooze(1)
    nativeType("<Return>")
    snooze(1)
    # end of workaround        
    mouseClick(waitForObject(names.easyDiffraction_Text))
    mouseClick(waitForObject(names.easyDiffraction_Text_2))
    mouseClick(waitForObject(names.easyDiffraction_Text_3))
    mouseClick(waitForObject(names.easyDiffraction_Text_4))
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_2))
    test.compare(waitForObjectExists(names.tabBar_Analysis_Button).enabled, True)
    test.compare(str(waitForObjectExists(names.tabBar_Analysis_Button).text), "Analysis")
    test.compare(waitForObjectExists(names.o_Rectangle_3).parent.rowCount, 25)
    mouseClick(waitForObject(names.tabBar_label_MnemonicLabel_2))
    test.compare(waitForObjectExists(names.o_Rectangle_4).enabled, True)
    test.compare(waitForObjectExists(names.o_Rectangle_4).visible, True)
    test.compare(waitForObjectExists(names.o_Rectangle_4).parent.rowCount, 2)
    mouseClick(waitForObject(names.tabBar_label_MnemonicLabel))
    test.compare(waitForObjectExists(names.easyDiffraction_Next_step_Summary_Button).enabled, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Next_step_Summary_Button).text), "Next step: Summary")
    mouseClick(waitForObject(names.tabbar_label_MnemonicLabel))
