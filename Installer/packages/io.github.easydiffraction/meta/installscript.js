
function Component()
{

//installer.executeDetached("set", "QWE2=qwe3");
    // default constructor
  //  installer.installationFinished.connect(this, Component.prototype.installationFinishedPageIsShown);





    //installer.setDefaultPageVisible(QInstaller.Introduction, false);
    //installer.setDefaultPageVisible(QInstaller.TargetDirectory, false);
    if (installer.isInstaller())
    {
        installer.setDefaultPageVisible(QInstaller.ComponentSelection, false); //******// works for Installer, but not for Updater !?
    }
    installer.setDefaultPageVisible(QInstaller.LicenseCheck, false);//******//
    //installer.setDefaultPageVisible(QInstaller.StartMenuSelection, false);
    //installer.setDefaultPageVisible(QInstaller.ReadyForInstallation, false);
    //installer.setDefaultPageVisible(QInstaller.PerformInstallation, false);
    //installer.setDefaultPageVisible(QInstaller.PerformInstallation, false);


}

// dont work
Component.prototype.installationFinishedPageIsShown = function()
{
    try {
        if (installer.isInstaller() && installer.status == QInstaller.Success) {
            //var args = ["PATH=%PATH;@TargetDir@"]
            //installer.executeDetached("set", args);
            ///installer.executeDetached("set", "QWE2=qwe2");
        }
    } catch(e) {
        console.log(e);
    }
}


// here we are creating the operation chain which will be processed at the real installation part later
Component.prototype.createOperations = function()
{

    // call default implementation to actually install the registeredfile
    component.createOperations();


//    var sep = ":";
//    if (installer.value("os") == "win") { sep = ";" }
//    var path = installer.environmentVariable("PATH") + sep + installer.value("TargetDir")
//    QMessageBox.warning("delete.question", "Installer", path, QMessageBox.Yes | QMessageBox.No);

    //component.addOperation("EnvironmentVariable", "FARSA_DIR", "@TargetDir@", true);


    // http://danlec.com/st4k#questions/43111510
    // https://bugreports.qt.io/browse/QTIFW-527
    // https://forum.qt.io/topic/30227/solved-qt-installer-framework-question-about-setting-enviroment-variables/2
    // https://stackoverflow.com/questions/43111510/qt-installer-framework-how-to-add-my-program-to-windows-system-variable-path
    // dont work

        // Add to system path
        //var sep = ":";
        //if (installer.value("os") == "win") { sep = ";" }
        //component.addOperation("EnvironmentVariable",
        //"PATH",
        //"DAVINCI_DIR",
        //installer.environmentVariable("PATH") + sep + "@TargetDir@",
        //"@TargetDir@",
        //true, // persistently
        //false // for all users
        //);



    if (systemInfo.productType === "windows")
    {
        // Add desktop shortcut for the app
        component.addOperation("CreateShortcut",
          "@TargetDir@/@ProductName@/@ProductName@.exe",
          "@DesktopDir@/@ProductName@.lnk",
          "workingDirectory=@TargetDir@@ProductName@",
          "iconPath=@TargetDir@/@ProductName@/@ProductName@.exe", "iconId=0",
          "description=@ProductName@");
        // Add start menu shortcut for the app
        component.addOperation("CreateShortcut",
          "@TargetDir@/@ProductName@/@ProductName@.exe",
          "@StartMenuDir@/@ProductName@/@ProductName@.lnk",
          "workingDirectory=@TargetDir@/@ProductName@",
          "iconPath=@TargetDir@/@ProductName@/@ProductName@.exe", "iconId=0",
          "description=@ProductName@");
        // Add start menu shortcut for the app uninstaller
        component.addOperation("CreateShortcut",
          "@TargetDir@/@ProductName@Uninstaller.exe",
          "@StartMenuDir@/@ProductName@/@ProductName@Uninstaller.lnk",
          "workingDirectory=@TargetDir@",
          "iconPath=@TargetDir@/@ProductName@Uninstaller.exe", "iconId=0",
          "description=@ProductName@Uninstaller");
    }

    if (installer.value("os") == "x11")
    {
        component.addOperation( "CreateDesktopEntry",
                                "@TargetDir@/easyDiffraction.desktop",
                                "Comment=A scientific software for modelling and analysis of the neutron diffraction data.\nType=Application\nExec=@TargetDir@/@ProductName@\nPath=@TargetDir@\nName=easyDiffraction\nGenericName=easyDiffraction\nIcon=@TargetDir@/@ProductName@.png\nTerminal=false\nCategories=Science;Office;" );
        component.addOperation("Copy", "@TargetDir@/easyDiffraction.desktop", "@HomeDir@/Desktop/easyDiffraction.desktop");
    }







}
