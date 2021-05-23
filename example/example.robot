*** Settings ***
Library     Collections
Library	    AppiumLibrary
Library     ${CURDIR}/../RobotStf    ${STF_HOST}   ${STF_TOKEN}


*** Test Cases ***
first:
    ${resource1}     RobotStf.lock    requirements={"version":"9"}    wait_timeout=2     #timeout_seconds=2
    #${resource2}     lock    requirements={"version":"10"}   wait_timeout=2     #timeout_seconds=2

    setup_appium        ${resource1}
    #setup_appium        ${resource2}

    Log                 ${resource1}
    #Log                 ${resource2}

    ${appium_uri}=	Get From Dictionary	 ${resource1}	appium_uri

    ${appiumClient}=    Open Application  ${appium_uri}
    ...    platformName=Android
    ...    deviceName=somename
    ...    packageName=com.android.calculator2
    ...    appActivity=com.android.calculator2.Calculator
    ...    automationName=UiAutomator2
    ...    newCommandTimeout=10000
    Capture Page Screenshot

    teardown_appium     ${resource1}
    #teardown_appium     ${resource2}
    unlock              ${resource1}
    #unlock              ${resource2}

