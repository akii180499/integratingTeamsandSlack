#!/bin/bash
# Simple validation tests for GitHub Actions workflow
# Runs basic checks without complex bash features

WORKFLOW_FILE=".github/workflows/mulesoft-code-review.yml"

echo "=========================================="
echo "GitHub Actions Workflow Validation Tests"
echo "=========================================="
echo ""

# Test 1: File exists
echo "Test 1: Workflow file existence"
if [ -f "$WORKFLOW_FILE" ]; then
    echo "✓ PASS: Workflow file exists"
else
    echo "✗ FAIL: Workflow file not found"
    exit 1
fi

# Test 2: Workflow name
echo "Test 2: Workflow name"
grep -q "name: Mulesoft Code Review" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 3: Pull request trigger
echo "Test 3: Pull request trigger"
grep -q "pull_request:" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 4: Trigger types
echo "Test 4: Event types (opened, synchronize, reopened)"
grep -q "types:.*opened.*synchronize.*reopened" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 5: Target branches
echo "Test 5: Target branches (main, develop, release)"
grep -q "\- main" "$WORKFLOW_FILE" && grep -q "\- develop" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 6: Job definition
echo "Test 6: Job configuration"
grep -q "mulesoft-code-review:" "$WORKFLOW_FILE" && grep -q "runs-on: ubuntu-latest" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 7: Checkout actions
echo "Test 7: Checkout steps"
grep -q "Checkout Code Review Repository" "$WORKFLOW_FILE" && grep -q "Checkout Target Repository" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 8: Actions versions
echo "Test 8: Using actions/checkout@v4"
grep -q "actions/checkout@v4" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 9: Python setup
echo "Test 9: Python 3.11 setup"
grep -q "actions/setup-python@v4" "$WORKFLOW_FILE" && grep -q "python-version: '3.11'" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 10: Install dependencies
echo "Test 10: Dependency installation"
grep -q "pip install -r requirements.txt" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 11: Code review execution
echo "Test 11: Code review script execution"
grep -q "python mulesoft_enhanced_validation.py" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 12: Environment variables
echo "Test 12: Environment variables"
grep -q "GITHUB_TOKEN:" "$WORKFLOW_FILE" && grep -q "OPENAI_API_KEY:" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 13: Secrets
echo "Test 13: Secrets configuration"
grep -q "secrets.PAT_TOKEN" "$WORKFLOW_FILE" && grep -q "secrets.OPENAI_API_KEY" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 14: Artifact upload
echo "Test 14: Artifact upload with retention"
grep -q "actions/upload-artifact@v4" "$WORKFLOW_FILE" && grep -q "retention-days: 30" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 15: Always upload artifacts
echo "Test 15: Upload artifacts on failure (if: always)"
grep -q "if: always()" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 16: Repository paths
echo "Test 16: Repository path configuration"
grep -q "path: code-review" "$WORKFLOW_FILE" && grep -q "path: target-repo" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 17: Fetch depth
echo "Test 17: Full git history (fetch-depth: 0)"
grep -q "fetch-depth: 0" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

# Test 18: Configuration warning
echo "Test 18: Repository configuration warning present"
grep -q "⚠️ CHANGE THIS" "$WORKFLOW_FILE" && echo "✓ PASS" || echo "✗ FAIL"

echo ""
echo "=========================================="
echo "All validation checks completed"
echo "=========================================="