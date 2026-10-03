*** Settings ***
Documentation     Regression test suite for Todo App API covering edge cases and error handling.
Resource          ../resources/common.robot
Suite Setup       Setup Api Test Suite
Suite Teardown    Teardown Api Test Suite

*** Test Cases ***
TC2.1: Task Validation Rejects Empty Title
    [Documentation]    Verify API returns 422 when creating a task with an empty title.
    [Tags]             regression    tasks    validation
    ${status}=         Create Task With Invalid Data    title=
    Should Be Equal As Integers    ${status}    422

TC2.2: Task Not Found Handling Returns 404
    [Documentation]    Verify GET, PATCH, and DELETE on non-existent task IDs return 404.
    [Tags]             regression    tasks    errors
    Get Nonexistent Task          999999
    Update Nonexistent Task       999999    title=New Title
    Delete Nonexistent Task       999999

TC2.3: Tag Duplicate Name Returns Conflict
    [Documentation]    Verify creating a tag with an already existing name returns 409 Conflict.
    [Tags]             regression    tags
    ${tag}=            Create Tag    name=unique-regression-tag    color=\#3B82F6
    Should Be True                ${tag}[id] > 0
    ${status}=         Create Duplicate Tag Should Fail    name=unique-regression-tag
    Should Be Equal As Integers    ${status}    409

TC2.4: Task Filtering By Status
    [Documentation]    Verify filtering tasks by pending and completed status.
    [Tags]             regression    tasks    filtering
    ${task1}=          Create Task    title=Regression Pending Task    is_completed=False
    ${task2}=          Create Task    title=Regression Done Task       is_completed=True

    ${pending}=        List Tasks    status=pending
    ${completed}=      List Tasks    status=completed

    # Verify pending list contains task1 and none are completed
    ${has_task1}=      Set Variable    ${False}
    FOR    ${t}    IN    @{pending}
        IF    ${t}[id] == ${task1}[id]
            ${has_task1}=    Set Variable    ${True}
        END
        Should Be True    not ${t}[is_completed]
    END
    Should Be True    ${has_task1}

    # Verify completed list contains task2 and all are completed
    ${has_task2}=      Set Variable    ${False}
    FOR    ${t}    IN    @{completed}
        IF    ${t}[id] == ${task2}[id]
            ${has_task2}=    Set Variable    ${True}
        END
        Should Be True    ${t}[is_completed]
    END
    Should Be True    ${has_task2}

TC2.5: Task Filtering By Priority
    [Documentation]    Verify filtering tasks by priority returns only tasks with matching priority.
    [Tags]             regression    tasks    filtering
    ${t_high}=         Create Task    title=Priority High Task      priority=high
    ${t_low}=          Create Task    title=Priority Low Task       priority=low

    ${high_tasks}=     List Tasks    priority=high
    FOR    ${t}    IN    @{high_tasks}
        Should Be Equal As Strings    ${t}[priority]    high
    END

TC2.6: Task Keyword Search
    [Documentation]    Verify keyword search matches on title and description.
    [Tags]             regression    tasks    search
    ${t_search}=       Create Task    title=AlphaOmegaSearchTarget    description=KeywordSpecificNotes

    ${results_title}=  List Tasks    search=AlphaOmegaSearchTarget
    Should Be True     len(${results_title}) >= 1
    Should Be Equal As Strings    ${results_title}[0][title]    AlphaOmegaSearchTarget

    ${results_notes}=  List Tasks    search=KeywordSpecificNotes
    Should Be True     len(${results_notes}) >= 1

TC2.7: Task Tag Association And Dissociation
    [Documentation]    Verify attaching and removing tags to a task dynamically.
    [Tags]             regression    tags    tasks
    ${tag}=            Create Tag    name=dynamic-tag    color=\#EC4899
    ${task}=           Create Task    title=Task for Tagging
    ${tag_id}=         Set Variable    ${tag}[id]
    ${task_id}=        Set Variable    ${task}[id]

    # Attach tag
    Attach Tag To Task    tag_id=${tag_id}    task_id=${task_id}
    ${tagged_tasks}=   Get Tasks For Tag    ${tag_id}
    Should Be True     len(${tagged_tasks}) == 1
    Should Be Equal As Integers    ${tagged_tasks}[0][id]    ${task_id}

    # Detach tag
    Detach Tag From Task    tag_id=${tag_id}    task_id=${task_id}
    ${tagged_after}=   Get Tasks For Tag    ${tag_id}
    Should Be True     len(${tagged_after}) == 0
