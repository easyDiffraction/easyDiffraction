set SQUISHPATH=c:\util\Squish651_Qt513_vs2017
set SQUISH_SERVER_HOST=127.0.0.1
set SQUISH_SERVER_PORT=4322
set TESTSUITE=%~dp0\suite_easyDiff
set REPORTPATH=%~dp0\report
set PYTHONPATH=C:\Anaconda\envs\p27

cd %SQUISHPATH%\bin

squishrunner --host %SQUISH_SERVER_HOST% --port %SQUISH_SERVER_PORT% --testsuite %TESTSUITE% --reportgen xml2.1,%REPORTPATH%/report.xml

cd %REPORTPATH%

%PYTHONPATH%\python.exe %SQUISHPATH%\examples\regressiontesting\squishxml2html.py --dir HTMLReports *.xml

HTMLReports\index.html

cd %TESTSUITE%

