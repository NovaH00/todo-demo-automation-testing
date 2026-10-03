*** Settings ***
Documentation     Smoke tests for Todo App API verifying critical paths.
Resource          ../resources/common.robot
Suite Setup       Setup Api Test Suite
Suite Teardown    Teardown Api Test Suite

*** Test Cases ***
TC1.1: Health Check Endpoint Responds Ok
    [Documentation]    Verify the health check endpoint returns 200 and healthy status.
    [Tags]             smoke    health
    ${health}=         Check Health
    Should Be Equal As Strings    ${health}[status]    ok
    Should Be Equal As Strings    ${health}[app]       Todo App API

TC1.2: Basic Task Lifecycle
    [Documentation]    Verify full lifecycle of creating, getting, updating, and deleting a task.
    [Tags]             smoke    tasks
    ${task}=           Create Task    title=Smoke Test Task    priority=high
    Should Be True                ${task}[id] > 0
    Should Be Equal As Strings    ${task}[title]           Smoke Test Task
    Should Be Equal As Strings    ${task}[priority]        high
    Should Be True                not ${task}[is_completed]

    ${task_id}=        Set Variable    ${task}[id]
    ${fetched}=        Get Task    ${task_id}
    Should Be Equal As Strings    ${fetched}[title]        Smoke Test Task

    ${updated}=        Update Task    ${task_id}    is_completed=True
    Should Be True                ${updated}[is_completed]

    Delete Task        ${task_id}
    Get Nonexistent Task          ${task_id}

TC1.3: Basic List Creation
    [Documentation]    Verify creating and retrieving a list.
    [Tags]             smoke    lists
    ${list}=           Create Todo List    name=Smoke List    color=\#2563EB
    Should Be True                ${list}[id] > 0
    Should Be Equal As Strings    ${list}[name]     Smoke List
    Should Be Equal As Strings    ${list}[color]    \#2563EB

    ${fetched}=        Get Todo List    ${list}[id]
    Should Be Equal As Strings    ${fetched}[name]  Smoke List

TC1.4: Basic Tag Creation
    [Documentation]    Verify creating and retrieving a tag.
    [Tags]             smoke    tags
    ${tag}=            Create Tag    name=smoke-tag    color=\#10B981
    Should Be True                ${tag}[id] > 0
    Should Be Equal As Strings    ${tag}[name]      smoke-tag
