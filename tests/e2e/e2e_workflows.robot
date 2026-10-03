*** Settings ***
Documentation     End-to-End user workflows for Todo App API.
Resource          ../resources/common.robot
Suite Setup       Setup Api Test Suite
Suite Teardown    Teardown Api Test Suite

*** Test Cases ***
TC3.1: Complete Project Execution Journey
    [Documentation]    Simulate full user journey: create project list, tags, tasks, complete work, and filter.
    [Tags]             e2e    projects
    # Step 1: Create a project list
    ${list}=           Create Todo List    name=Mobile Launch    description=Q4 Mobile Release    color=\#7C3AED
    ${list_id}=        Set Variable    ${list}[id]
    Should Be True     ${list_id} > 0

    # Step 2: Create tags for roles
    ${tag_ui}=         Create Tag    name=ui    color=\#3B82F6
    ${tag_api}=        Create Tag    name=api   color=\#10B981
    ${tag_ui_id}=      Set Variable    ${tag_ui}[id]
    ${tag_api_id}=     Set Variable    ${tag_api}[id]

    # Step 3: Add tasks to the project list with tags
    ${ui_tag_list}=    BuiltIn.Create List    ${tag_ui_id}
    ${api_tag_list}=   BuiltIn.Create List    ${tag_api_id}

    ${t1}=             Create Task    title=Design Mockups    priority=high      list_id=${list_id}    tag_ids=${ui_tag_list}
    ${t2}=             Create Task    title=Build Auth API    priority=high      list_id=${list_id}    tag_ids=${api_tag_list}
    ${t3}=             Create Task    title=Write Docs        priority=medium    list_id=${list_id}

    # Step 4: Verify list has all tasks
    ${tasks_in_list}=  Get Tasks For Todo List    ${list_id}
    Should Be True     len(${tasks_in_list}) == 3

    # Step 5: Complete Task 1
    ${t1_updated}=     Update Task    ${t1}[id]    is_completed=True
    Should Be True     ${t1_updated}[is_completed]

    # Step 6: Filter tasks in list by status
    ${pending}=        List Tasks    list_id=${list_id}    status=pending
    Should Be True     len(${pending}) == 2

    ${completed}=      List Tasks    list_id=${list_id}    status=completed
    Should Be True     len(${completed}) == 1
    Should Be Equal As Integers    ${completed}[0][id]    ${t1}[id]

    # Step 7: Delete list
    Delete Todo List   ${list_id}

TC3.2: Schedule Planning And Rescheduling Workflow
    [Documentation]    Simulate timeline planning: create scheduled tasks, verify overview, and batch reschedule.
    [Tags]             e2e    schedule
    ${past_date}=      Get Relative Iso Date    days_offset=-3
    ${today_date}=     Get Relative Iso Date    days_offset=0    hours_offset=2
    ${future_date}=    Get Relative Iso Date    days_offset=4

    # Create tasks across time horizons
    ${t_overdue}=      Create Task    title=Overdue Milestone       due_date=${past_date}
    ${t_today}=        Create Task    title=Today Review            due_date=${today_date}
    ${t_upcoming}=     Create Task    title=Next Week Deployment    due_date=${future_date}

    # Check Overview counts
    ${overview}=       Get Schedule Overview
    Should Be True     ${overview}[overdue_count] >= 1
    Should Be True     ${overview}[today_count] >= 1
    Should Be True     ${overview}[upcoming_count] >= 1

    # Batch reschedule overdue task to next week
    ${reschedule_date}=   Get Relative Iso Date    days_offset=5
    ${overdue_ids}=       BuiltIn.Create List    ${t_overdue}[id]
    ${rescheduled}=       Reschedule Tasks    task_ids=${overdue_ids}    new_due_date=${reschedule_date}
    Should Be True        len(${rescheduled}) == 1
    Should Be Equal As Integers    ${rescheduled}[0][id]    ${t_overdue}[id]

    # Verify task is no longer in overdue list
    ${overdue_list}=   Get Overdue Tasks
    FOR    ${task}    IN    @{overdue_list}
        Should Not Be Equal As Integers    ${task}[id]    ${t_overdue}[id]
    END
