// https://doc.qt.io/qtinstallerframework/scripting-installer.html

function Controller()
{
//installer.executeDetached("set", "QWE2=qwe4");
}

Controller.prototype.IntroductionPageCallback = function()
{
    var page = gui.currentPageWidget();
    if (page != null)
    {
        //page.title = "Introduction";

        if (installer.isInstaller())
        {
            var msg = "";
            msg += "<p>Welcome to the easyDiffraction Setup Wizard.</p>";
            msg += "<p>easyDiffraction is a scientific software for modelling and analysis of the neutron diffraction data.</p>";
            msg += "<p>For more details, visit <a href=\"http://easyDiffraction.github.io\">easyDiffraction.github.io</a></p>";
            page.MessageLabel.setText(msg);
        }
        if (installer.isUninstaller())
        {
                gui.clickButton(buttons.NextButton);//******//
        }
        if (installer.isUpdater())
        {
                gui.clickButton(buttons.NextButton);//******//
        }
    }
}

Controller.prototype.TargetDirectoryPageCallback = function()
{
    //var page = gui.currentPageWidget();
    //if (page != null)
    //{
        //page.TargetDirectoryLineEdit.textChanged.connect(this, Controller.prototype.targetChanged);
        //Controller.prototype.targetChanged(page.TargetDirectoryLineEdit.text);
    //}
}

Controller.prototype.targetChanged = function(path)
{
    if (installer.fileExists(path))
    {
        var question = path + "\ndirectory already exists. Do you want to overwrite previous installation?";
        var result = QMessageBox.warning("delete.question", "Installer", question, QMessageBox.Yes | QMessageBox.No);
        if (result == QMessageBox.Yes)
        {
            if (installer.value("os") == "mac")
            {
                installer.performOperation("Execute", ["rm", "-r", "-f", path]);
            }
            else if (installer.value("os") == "win")
            {
                //installer.performOperation("Execute", ["rd", "/s", "/q", path]);

                QMessageBox.warning("delete.question", "Installer", path, QMessageBox.Yes | QMessageBox.No);

                installer.performOperation("Execute", ["rmdir", "/s", "/q", path]);

                QMessageBox.warning("delete.question", "Installer", "ok1", QMessageBox.Yes | QMessageBox.No);

                installer.performOperation("Execute", ["rd", "/s", "/q", path]);

                QMessageBox.warning("delete.question", "Installer", "ok2", QMessageBox.Yes | QMessageBox.No);
            }
            else
            { //if (installer.value("os") == "x11") {
                installer.performOperation("Execute", ["rm", "-r", "-f", path]);
            }
        }
    }
}


Controller.prototype.ComponentSelectionPageCallback = function()
{
    var page = gui.currentPageWidget();
    if (page != null)
    {
        ///page.visible = false;
        ///page.title = " ";
        //page.selectAll();
        //gui.clickButton(buttons.NextButton);
        //if (installer.isUpdater())
        //{
        // Temporary solution, as setDefaultPageVisible = false in installscript.js
        // works for Installer, but not for Updater !?
//******//            gui.clickButton(buttons.NextButton);
        //}
    }
}


Controller.prototype.LicenseAgreementPageCallback = function()
{
    var page = gui.currentPageWidget();
    if (page != null)
    {
        ///page.title = " ";
        //page.AcceptLicenseRadioButton.visible = false;
        //page.RejectLicenseRadioButton.visible = false;
        ///page.AcceptLicenseRadioButton.checked = true;
        //installer.setDefaultPageVisible(QInstaller.LicenseCheck, false);
    }
}

Controller.prototype.StartMenuDirectoryPageCallback = function()
{
    var page = gui.currentPageWidget();
    if (page != null)
    {
        //page.title = " ";
    }
}

Controller.prototype.ReadyForInstallationPageCallback = function()
{
    var page = gui.currentPageWidget();
    if (page != null)
    {
        //page.title = "C";
        //page.visible = false;
        //gui.clickButton(buttons.NextButton);
    }
}

Controller.prototype.PerformInstallationPageCallback = function()
{
    var page = gui.currentPageWidget();
    if (page != null)
    {
        ///page.title = " ";
        //gui.clickButton(buttons.NextButton);
    }
}

Controller.prototype.FinishedPageCallback = function()
{
    if (installer.status == QInstaller.Success)
    {
        var page = gui.currentPageWidget();
        if (page != null) {
            if (installer.isInstaller())
            {
                //page.hide();
                //page.visible = false;
                //var app = installer.value("ProductName");
                //var question = "Completing the "+app+" Wizard. Do you want to run "+app+" now?";
                //var result = QMessageBox.question("runapp.question", "Installer", question,
                //                                    QMessageBox.Yes | QMessageBox.No);
                //if (result == QMessageBox.Yes)
                //{
                //    Controller.prototype.runApp();
                //}
                //gui.clickButton(buttons.FinishButton);
            }
            if (installer.isUpdater())
            {
                ///Controller.prototype.runApp();
                ///gui.clickButton(buttons.FinishButton);
            }
            if (installer.isUninstaller())
            {
            }
        }
    }
}

Controller.prototype.runApp = function()
{
    var path = "file:///" + installer.value("TargetDir") + "/" + installer.value("ProductName");

    if (installer.value("os") == "mac")
    {
        QDesktopServices.openUrl(path + ".app");
    }
    else if (installer.value("os") == "win")
    {
        QDesktopServices.openUrl(path + ".exe");
    }
    else
    { //if (installer.value("os") == "x11") {
        QDesktopServices.openUrl(path);
    }
}
