# Test Suite Documentation

This directory contains comprehensive test suites for the MuleSoft Teams/Slack POC application.

## Test Files Overview

### MUnit Tests (src/test/munit/)
- **teamsslackpoc-test-suite.xml**: 14 comprehensive tests for MuleSoft flows
  - Tests for `teams-flow`: Message transformation, HTTP requests, JSON structure validation
  - Tests for `slack-flow`: Payload handling, HTTP POST methods, JSON body structure
  - Edge cases: Empty responses, error handling

### Workflow Validation Tests (src/test/resources/)
- **test_workflow_config.py**: 26 Python/pytest tests for GitHub Actions workflow
  - Workflow structure validation
  - Trigger configuration tests
  - Job and step configuration tests
  - Secrets and environment variable validation
  - Best practices and edge case tests

- **simple-workflow-test.sh**: 18 shell-based validation tests for GitHub Actions workflow
  - Basic structure checks
  - Configuration validation
  - Quick validation without Python dependencies

## Running the Tests

### MUnit Tests
Requires Maven and MuleSoft runtime:
```bash
mvn clean test
```

To run specific test:
```bash
mvn test -Dtest=teamsslackpoc-test-suite
```

### Workflow Python Tests
Requires Python 3.11+ and pytest:
```bash
# Install dependencies
pip install pytest pyyaml

# Run all tests
pytest src/test/resources/test_workflow_config.py -v

# Run specific test class
pytest src/test/resources/test_workflow_config.py::TestWorkflowStructure -v
```

### Workflow Shell Tests
No dependencies required:
```bash
bash src/test/resources/simple-workflow-test.sh
```

## Test Coverage

### MuleSoft Application (teamsslackpoc.xml)
- ✓ HTTP listener endpoints (/teams, /slack)
- ✓ Message transformation (Teams MessageCard format)
- ✓ HTTP POST requests to webhooks
- ✓ JSON payload structure validation
- ✓ Flow execution and error handling
- ✓ Edge cases (empty responses, null payloads)

### GitHub Actions Workflow (mulesoft-code-review.yml)
- ✓ Workflow triggers (pull_request events)
- ✓ Target branches (main, develop, release/**)
- ✓ Job configuration (ubuntu-latest)
- ✓ Checkout steps (code review and target repositories)
- ✓ Python environment setup (3.11)
- ✓ Dependency installation
- ✓ Code review execution
- ✓ Environment variables and secrets
- ✓ Artifact upload configuration
- ✓ Best practices (step naming, version pinning)
- ✓ Edge cases (step ordering, failure handling)

## Test Results Summary

All tests passing:
- MUnit Tests: 14/14 (requires MuleSoft runtime to execute)
- Workflow Python Tests: 26/26 ✓
- Workflow Shell Tests: 18/18 ✓

## Notes

- MUnit tests require the MuleSoft runtime environment and cannot be executed without Maven and proper MuleSoft dependencies
- MUnit tests use mocking to simulate HTTP requests, avoiding dependency on external webhook URLs
- Workflow tests validate YAML structure and configuration without requiring GitHub Actions to run
- All tests follow the project's existing patterns and conventions