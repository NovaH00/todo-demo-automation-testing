*** Settings ***
Documentation     Global keywords and configurations for Todo Application tests.
Library           Browser    timeout=10s    auto_closing_level=SUITE
Library           TodoApiLibrary.py

*** Variables ***
${SERVER_PORT}    8899
${BASE_URL}       http://127.0.0.1:${SERVER_PORT}
${BROWSER}        chromium
${HEADLESS}       False
${SPEED}          0.2s

*** Keywords ***
Setup Api Test Suite
    Initialize Database

Teardown Api Test Suite
    Close Database

Setup UI Test Suite
    [Arguments]    ${port}=${SERVER_PORT}    ${headless}=${HEADLESS}    ${speed}=${SPEED}
    ${url}=    Start Test Server    port=${port}
    Set Suite Variable    ${BASE_URL}    ${url}
    New Browser    browser=${BROWSER}    headless=${headless}    slowMo=${speed}
    New Page    ${BASE_URL}

Teardown UI Test Suite
    Close Browser    ALL
    Stop Test Server

Open Browser Application
    [Arguments]    ${url}=${BASE_URL}    ${browser}=${BROWSER}    ${headless}=${HEADLESS}    ${speed}=${SPEED}
    New Browser    browser=${browser}    headless=${headless}    slowMo=${speed}
    New Page    ${url}

Close Browser Application
    Close Browser    ALL

Set Browser Speed
    [Arguments]    ${speed}
    Set Global Variable    ${SPEED}    ${speed}

Set Selenium Speed
    [Arguments]    ${speed}
    Set Global Variable    ${SPEED}    ${speed}
