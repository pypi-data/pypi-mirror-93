::������������������зֲ�ʽ���ԣ�ǰ��������ִ��start_server.bat�ű�������hub�Լ�����node�ڵ�
::��������selenium-server-standalone����
@echo off
start /D "LocalSeleniumServer/selenium_run_script" run_by_chrome.bat
start /D "LocalSeleniumServer/selenium_run_script" run_by_firefox.bat
start /D "LocalSeleniumServer/selenium_run_script" run_by_ie.bat