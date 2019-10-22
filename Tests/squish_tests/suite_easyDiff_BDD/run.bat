set SQUISHPATH=C:\util\Squish_6.5.1_mingw

set SQUISH_SERVER_HOST=127.0.0.1

set SQUISH_SERVER_PORT=4322

set TESTSUITE=C:\Users\piotrrozyczko\suite_EZDiff

set REPORTPATH=C:\Users\piotrrozyczko\suite_EZDiff\report.html

set PYTHONPATH=C:\Anaconda\envs\p27

cd %SQUISHPATH%\bin

squishrunner --host %SQUISH_SERVER_HOST% --port %SQUISH_SERVER_PORT% --testsuite %TESTSUITE% --reportgen xml2.1,%REPORTPATH%/report.xml

cd %REPORTPATH%

%PYTHONPATH%\python.exe %SQUISHPATH%\examples\regressiontesting\squishxml2html.py --dir HTMLReports *.xml

HTMLReports\index.html

pause


