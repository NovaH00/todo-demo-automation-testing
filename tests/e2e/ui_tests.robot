*** Settings ***
Documentation     End-to-End browser UI tests for Todo Application.
Resource          ../resources/common.robot
Suite Setup       Setup UI Test Suite
Suite Teardown    Teardown UI Test Suite

*** Test Cases ***
TC4.1: View The Todo Application
    [Documentation]    Open the browser and verify the Todo application loads.
    [Tags]             ui    e2e
    Get Title          contains    Todo
    Get Text           text=Task Ledger    ==    Task Ledger
    Get Text           text=API Live       ==    API Live

TC4.2: Create And Complete A Task In UI
    [Documentation]    Type a new task into the input and toggle its completion.
    [Tags]             ui    e2e
    Fill Text          input[placeholder*="Add a new task"]    Verify Playwright browser integration
    Keyboard Key       press    Enter
    Wait For Elements State    text=Verify Playwright browser integration    visible    timeout=5s
    Click              button[aria-label="Mark complete"]
    Wait For Elements State    div.line-through:has-text("Verify Playwright browser integration")    visible    timeout=5s

TC4.3: Edit Task Details In Modal
    [Documentation]    Open edit modal by clicking task title, modify notes, and save.
    [Tags]             ui    e2e
    Click              text=Verify Playwright browser integration
    Wait For Elements State    h2:has-text("Edit Task")    visible    timeout=5s
    Fill Text          textarea[placeholder*="Add optional notes"]    Verified with Robot Framework Playwright library
    Click              button:has-text("Save changes")
    Wait For Elements State    h2:has-text("Edit Task")    detached    timeout=5s
    Wait For Elements State    text=Verified with Robot Framework Playwright library    visible    timeout=5s

TC4.4: Create Additional Tasks For Filtering
    [Documentation]    Create active tasks to test filtering and search.
    [Tags]             ui    e2e
    Fill Text          input[placeholder*="Add a new task"]    Design landing page wireframe
    Keyboard Key       press    Enter
    Wait For Elements State    text=Design landing page wireframe    visible    timeout=5s
    Fill Text          input[placeholder*="Add a new task"]    Implement PostgreSQL migration
    Keyboard Key       press    Enter
    Wait For Elements State    text=Implement PostgreSQL migration    visible    timeout=5s

TC4.5: Filter Tasks By Status In Toolbar
    [Documentation]    Filter tasks using Active, Done, and All toolbar buttons.
    [Tags]             ui    e2e
    # Switch to Active tasks only
    Click              button:text-is("Active")
    Wait For Elements State    text=Design landing page wireframe    visible    timeout=5s
    Wait For Elements State    text=Verify Playwright browser integration    detached    timeout=5s

    # Switch to Done tasks only
    Click              button:text-is("Done")
    Wait For Elements State    text=Verify Playwright browser integration    visible    timeout=5s
    Wait For Elements State    text=Design landing page wireframe    detached    timeout=5s

    # Switch back to All tasks
    Click              button:text-is("All")
    Wait For Elements State    text=Design landing page wireframe    visible    timeout=5s
    Wait For Elements State    text=Verify Playwright browser integration    visible    timeout=5s

TC4.6: Search Tasks By Keyword
    [Documentation]    Type into the search input and verify matching items appear.
    [Tags]             ui    e2e
    Fill Text          input[placeholder="Search tasks..."]    PostgreSQL
    Wait For Elements State    text=Implement PostgreSQL migration    visible    timeout=5s
    Wait For Elements State    text=Design landing page wireframe    detached    timeout=5s

    # Clear search
    Fill Text          input[placeholder="Search tasks..."]    ${EMPTY}
    Wait For Elements State    text=Design landing page wireframe    visible    timeout=5s

TC4.7: Create Project List In Modal
    [Documentation]    Open the list modal from sidebar, submit a new list, and verify it appears.
    [Tags]             ui    e2e
    Click              button[title="Create new list"]
    Wait For Elements State    h2:has-text("New List")    visible    timeout=5s
    Fill Text          input[placeholder*="Engineering, Work"]    Frontend Redesign
    Click              button:has-text("Create list")
    Wait For Elements State    h2:has-text("New List")    detached    timeout=5s
    Wait For Elements State    button:has-text("Frontend Redesign")    visible    timeout=5s

TC4.8: Create New Tag In Modal
    [Documentation]    Open the tag modal from sidebar, submit a new tag, and verify it appears.
    [Tags]             ui    e2e
    Click              button[title="Create new tag"]
    Wait For Elements State    h2:has-text("New Tag")    visible    timeout=5s
    Fill Text          input[placeholder*="urgent, frontend"]    automation
    Click              button:has-text("Create tag")
    Wait For Elements State    h2:has-text("New Tag")    detached    timeout=5s
    Wait For Elements State    button:has-text("automation")    visible    timeout=5s

TC4.9: Switch Navigation Views
    [Documentation]    Switch views in the sidebar to verify navigation.
    [Tags]             ui    e2e
    Click              button:has-text("Today")
    Wait For Elements State    h1:has-text("Due Today")    visible    timeout=5s
    Click              button:has-text("All Tasks")
    Wait For Elements State    h1:has-text("All Tasks")    visible    timeout=5s

TC4.10: Delete A Task From UI
    [Documentation]    Delete a task using row action button and verify removal from ledger.
    [Tags]             ui    e2e
    Hover              div.group:has-text("Implement PostgreSQL migration")
    Click              div.group:has-text("Implement PostgreSQL migration") >> button[title="Delete task"]
    Wait For Elements State    text=Implement PostgreSQL migration    detached    timeout=5s
