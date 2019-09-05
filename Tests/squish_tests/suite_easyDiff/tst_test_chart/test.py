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
    mouseClick(waitForObject(names.label_MnemonicLabel))
    mouseClick(waitForObject(names.easyDiffraction_Text))
    mouseClick(waitForObject(names.easyDiffraction_Text_2))
    moveWindow(waitForObject(names.easyDiffraction_QQuickApplicationWindow), 331, 56)
    test.compare(waitForObjectExists(names.tabBar_Plot_View_TabButton).enabled, True)
    test.compare(str(waitForObjectExists(names.tabBar_Plot_View_TabButton).text), "Plot View")
    test.compare(waitForObjectExists(names.tabBar_Table_View_TabButton).enabled, True)
    test.compare(str(waitForObjectExists(names.tabBar_Table_View_TabButton).text), "Table View")
    test.compare(waitForObjectExists(names.easyDiffraction_topChart_QtCharts_DeclarativeChart).enabled, True)
    test.compare(waitForObjectExists(names.easyDiffraction_topChart_QtCharts_DeclarativeChart).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Sample_Model_Button).enabled, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Sample_Model_Button).text), "Sample Model")
    mouseClick(waitForObject(names.tabBar_label_MnemonicLabel_2))
    test.compare(waitForObjectExists(names.o_Rectangle_2).visible, True)
    test.compare(waitForObjectExists(names.o_Rectangle_2).enabled, True)
    mouseClick(waitForObject(names.tabBar_label_MnemonicLabel))
    test.compare(waitForObjectExists(names.textArea_TextArea).enabled, True)
    test.compare(waitForObjectExists(names.textArea_TextArea).visible, True)
    test.compare(waitForObjectExists(names.textArea_TextArea).lineCount, 384)
