# Test Report: Todo Application

This report lists every automated test implemented for the Todo application. Unit tests are excluded from this report.

All 23 test cases appear below with their unique test identifier and full name.

---

## Complete Test Catalog

| Test ID | Test Name | Suite Type | Source File | Description |
|---|---|---|---|---|
| **TC1.1** | TC1.1: Health Check Endpoint Responds Ok | Smoke | `tests/smoke/smoke_tests.robot` | Verify `/health` returns status `ok` and HTTP status code 200. |
| **TC1.2** | TC1.2: Basic Task Lifecycle | Smoke | `tests/smoke/smoke_tests.robot` | Create, fetch, update, and delete a single task. |
| **TC1.3** | TC1.3: Basic List Creation | Smoke | `tests/smoke/smoke_tests.robot` | Create a list and verify its name and color attributes. |
| **TC1.4** | TC1.4: Basic Tag Creation | Smoke | `tests/smoke/smoke_tests.robot` | Create a tag and verify its name and color attributes. |
| **TC2.1** | TC2.1: Task Validation Rejects Empty Title | Regression | `tests/regression/regression_tests.robot` | Verify the API rejects empty task titles with HTTP 422. |
| **TC2.2** | TC2.2: Task Not Found Handling Returns 404 | Regression | `tests/regression/regression_tests.robot` | Verify GET, PATCH, and DELETE on non-existent task IDs return HTTP 404. |
| **TC2.3** | TC2.3: Tag Duplicate Name Returns Conflict | Regression | `tests/regression/regression_tests.robot` | Verify creating an existing tag name returns HTTP 409 Conflict. |
| **TC2.4** | TC2.4: Task Filtering By Status | Regression | `tests/regression/regression_tests.robot` | Filter tasks by completion status (`pending` vs `completed`). |
| **TC2.5** | TC2.5: Task Filtering By Priority | Regression | `tests/regression/regression_tests.robot` | Filter tasks by priority levels (`high`, `medium`, `low`). |
| **TC2.6** | TC2.6: Task Keyword Search | Regression | `tests/regression/regression_tests.robot` | Search tasks by keywords in title and description fields. |
| **TC2.7** | TC2.7: Task Tag Association And Dissociation | Regression | `tests/regression/regression_tests.robot` | Attach a tag to a task and remove the tag link. |
| **TC3.1** | TC3.1: Complete Project Execution Journey | E2E API | `tests/e2e/e2e_workflows.robot` | Multi-step journey: create list, add tagged tasks, complete work, and delete list. |
| **TC3.2** | TC3.2: Schedule Planning And Rescheduling Workflow | E2E API | `tests/e2e/e2e_workflows.robot` | Create past, present, and future tasks, inspect overview, and batch reschedule. |
| **TC4.1** | TC4.1: View The Todo Application | E2E Browser UI | `tests/e2e/ui_tests.robot` | Load the web application and verify page title, header, and live API indicator. |
| **TC4.2** | TC4.2: Create And Complete A Task In UI | E2E Browser UI | `tests/e2e/ui_tests.robot` | Type a task, press Enter, verify in ledger, and toggle complete checkbox. |
| **TC4.3** | TC4.3: Edit Task Details In Modal | E2E Browser UI | `tests/e2e/ui_tests.robot` | Open edit modal by clicking task title, update notes, and save changes. |
| **TC4.4** | TC4.4: Create Additional Tasks For Filtering | E2E Browser UI | `tests/e2e/ui_tests.robot` | Add multiple tasks to populate the active queue for filter tests. |
| **TC4.5** | TC4.5: Filter Tasks By Status In Toolbar | E2E Browser UI | `tests/e2e/ui_tests.robot` | Click "Active", "Done", and "All" segmented control buttons to filter items. |
| **TC4.6** | TC4.6: Search Tasks By Keyword | E2E Browser UI | `tests/e2e/ui_tests.robot` | Type search terms into the search bar and verify live list filtering. |
| **TC4.7** | TC4.7: Create Project List In Modal | E2E Browser UI | `tests/e2e/ui_tests.robot` | Open list modal, enter list name, submit form, and verify sidebar display. |
| **TC4.8** | TC4.8: Create New Tag In Modal | E2E Browser UI | `tests/e2e/ui_tests.robot` | Open tag modal, enter tag name, submit form, and verify sidebar chip display. |
| **TC4.9** | TC4.9: Switch Navigation Views | E2E Browser UI | `tests/e2e/ui_tests.robot` | Navigate between Today and All Tasks in sidebar, checking view headers. |
| **TC4.10** | TC4.10: Delete A Task From UI | E2E Browser UI | `tests/e2e/ui_tests.robot` | Hover task item row, click delete icon, and verify task removal. |

---

## Detailed Test Specifications

### Smoke Tests (TC1)
- **TC1.1: Health Check Endpoint Responds Ok**  
  Calls `/health` and confirms HTTP status 200 with JSON payload `{"status": "ok", "app": "Todo App API"}`.
- **TC1.2: Basic Task Lifecycle**  
  Creates a task, verifies non-zero ID, fetches task details, marks completed, deletes task, and confirms 404 on re-fetch.
- **TC1.3: Basic List Creation**  
  Creates a list with name and hex color code, verifies stored list data.
- **TC1.4: Basic Tag Creation**  
  Creates a tag with name and color, verifies stored tag data.

### Regression Tests (TC2)
- **TC2.1: Task Validation Rejects Empty Title**  
  Sends a POST request with an empty title string and validates HTTP status 422.
- **TC2.2: Task Not Found Handling Returns 404**  
  Queries ID `999999` with GET, PATCH, and DELETE, validating HTTP 404 responses.
- **TC2.3: Tag Duplicate Name Returns Conflict**  
  Creates a tag, then attempts to create another tag with the same name. Validates HTTP 409.
- **TC2.4: Task Filtering By Status**  
  Creates one pending task and one completed task. Validates filtering with `status=pending` and `status=completed`.
- **TC2.5: Task Filtering By Priority**  
  Creates high-priority and low-priority tasks. Validates filtering with `priority=high`.
- **TC2.6: Task Keyword Search**  
  Creates a task with unique title and notes. Validates searching by title query and by notes query.
- **TC2.7: Task Tag Association And Dissociation**  
  Links a tag to a task, checks `/tags/{id}/tasks`, unlinks tag, and checks task count drops to zero.

### End-to-End API Workflows (TC3)
- **TC3.1: Complete Project Execution Journey**  
  Simulates a real project workflow: creates list `Mobile Launch`, creates tags `ui` and `api`, creates 3 tasks, marks one complete, verifies counts, and deletes the list.
- **TC3.2: Schedule Planning And Rescheduling Workflow**  
  Creates tasks with overdue, current day, and future deadlines. Verifies `/schedule/overview` metrics, then batch reschedules overdue tasks.

### End-to-End Browser UI Tests (TC4)
- **TC4.1: View The Todo Application**  
  Loads Chromium, navigates to application URL, and asserts title "Todo App - Task Ledger" and "API Live" badge.
- **TC4.2: Create And Complete A Task In UI**  
  Enters task title into main input, presses Enter, checks element visibility, and clicks tactile checkbox to verify line-through styling.
- **TC4.3: Edit Task Details In Modal**  
  Clicks task title to open edit modal, updates task description textarea, saves changes, and verifies ledger text.
- **TC4.4: Create Additional Tasks For Filtering**  
  Inputs two additional active tasks into the ledger.
- **TC4.5: Filter Tasks By Status In Toolbar**  
  Clicks Active, Done, and All buttons in toolbar, asserting correct visible and detached element states.
- **TC4.6: Search Tasks By Keyword**  
  Enters "PostgreSQL" into search input, asserts filtered result, clears input, and asserts full list restores.
- **TC4.7: Create Project List In Modal**  
  Clicks "+ List" button in sidebar, fills name "Frontend Redesign", submits modal, and asserts list button in sidebar.
- **TC4.8: Create New Tag In Modal**  
  Clicks "+ Tag" button in sidebar, fills name "automation", submits modal, and asserts tag button in sidebar.
- **TC4.9: Switch Navigation Views**  
  Clicks "Today" in sidebar, verifies "Due Today" heading, clicks "All Tasks", verifies "All Tasks" heading.
- **TC4.10: Delete A Task From UI**  
  Hovers over task item row, clicks trash icon button, and verifies task element detaches from DOM.
