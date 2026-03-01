"""
Unit tests for GitHub Actions workflow: mulesoft-code-review.yml
Tests validate the workflow configuration structure and settings.
"""

import yaml
import pytest
from pathlib import Path


@pytest.fixture
def workflow_config():
    """Load the workflow YAML file."""
    workflow_path = Path('.github/workflows/mulesoft-code-review.yml')
    with open(workflow_path, 'r') as f:
        return yaml.safe_load(f)


class TestWorkflowStructure:
    """Test the basic structure of the workflow."""

    def test_workflow_name(self, workflow_config):
        """Test that workflow has correct name."""
        assert workflow_config['name'] == 'Mulesoft Code Review', \
            "Workflow name should be 'Mulesoft Code Review'"

    def test_workflow_has_jobs(self, workflow_config):
        """Test that workflow contains jobs section."""
        assert 'jobs' in workflow_config, "Workflow must have 'jobs' section"
        assert len(workflow_config['jobs']) > 0, "Workflow must have at least one job"

    def test_job_exists(self, workflow_config):
        """Test that mulesoft-code-review job exists."""
        assert 'mulesoft-code-review' in workflow_config['jobs'], \
            "Job 'mulesoft-code-review' must be defined"


class TestWorkflowTriggers:
    """Test the trigger configuration of the workflow."""

    def test_pull_request_trigger_exists(self, workflow_config):
        """Test that workflow triggers on pull requests."""
        # YAML parses 'on' as True (boolean), so we check for both
        trigger_key = 'on' if 'on' in workflow_config else True
        assert trigger_key in workflow_config, "Workflow must have 'on' trigger section"
        assert 'pull_request' in workflow_config[trigger_key], \
            "Workflow must trigger on pull_request events"

    def test_pull_request_types(self, workflow_config):
        """Test that workflow triggers on correct PR event types."""
        # YAML parses 'on' as True (boolean)
        trigger_key = 'on' if 'on' in workflow_config else True
        pr_config = workflow_config[trigger_key]['pull_request']
        expected_types = ['opened', 'synchronize', 'reopened']

        assert 'types' in pr_config, "Pull request trigger must specify types"
        assert set(pr_config['types']) == set(expected_types), \
            f"PR types should be {expected_types}"

    def test_target_branches(self, workflow_config):
        """Test that workflow targets correct branches."""
        # YAML parses 'on' as True (boolean)
        trigger_key = 'on' if 'on' in workflow_config else True
        pr_config = workflow_config[trigger_key]['pull_request']
        expected_branches = ['main', 'develop', 'release/**']

        assert 'branches' in pr_config, "Pull request trigger must specify target branches"
        assert set(pr_config['branches']) == set(expected_branches), \
            f"Target branches should be {expected_branches}"


class TestJobConfiguration:
    """Test the job configuration."""

    def test_job_runs_on_ubuntu(self, workflow_config):
        """Test that job runs on ubuntu-latest."""
        job = workflow_config['jobs']['mulesoft-code-review']
        assert job['runs-on'] == 'ubuntu-latest', \
            "Job should run on 'ubuntu-latest'"

    def test_job_has_steps(self, workflow_config):
        """Test that job contains steps."""
        job = workflow_config['jobs']['mulesoft-code-review']
        assert 'steps' in job, "Job must have 'steps' section"
        assert len(job['steps']) > 0, "Job must have at least one step"

    def test_minimum_required_steps(self, workflow_config):
        """Test that job has minimum required steps."""
        job = workflow_config['jobs']['mulesoft-code-review']
        step_names = [step.get('name', '') for step in job['steps']]

        required_steps = [
            'Checkout Code Review Repository',
            'Checkout Target Repository',
            'Set up Python',
            'Install Dependencies',
            'Run Mulesoft Code Review',
            'Upload Review Artifacts'
        ]

        for required_step in required_steps:
            assert any(required_step in name for name in step_names), \
                f"Step '{required_step}' must be present in the workflow"


class TestCheckoutSteps:
    """Test the checkout step configurations."""

    def test_code_review_checkout(self, workflow_config):
        """Test code review repository checkout configuration."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        checkout_step = next(
            (s for s in steps if s.get('name') == 'Checkout Code Review Repository'),
            None
        )

        assert checkout_step is not None, "Code review checkout step must exist"
        assert checkout_step['uses'] == 'actions/checkout@v4', \
            "Should use checkout@v4 action"
        assert 'with' in checkout_step, "Checkout step must have 'with' configuration"
        assert 'repository' in checkout_step['with'], \
            "Must specify repository to checkout"
        assert checkout_step['with']['ref'] == 'main', \
            "Should checkout main branch"
        assert checkout_step['with']['path'] == 'code-review', \
            "Should checkout to 'code-review' path"

    def test_target_repo_checkout(self, workflow_config):
        """Test target repository checkout configuration."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        checkout_step = next(
            (s for s in steps if 'Checkout Target Repository' in s.get('name', '')),
            None
        )

        assert checkout_step is not None, "Target repo checkout step must exist"
        assert checkout_step['uses'] == 'actions/checkout@v4', \
            "Should use checkout@v4 action"
        assert checkout_step['with']['path'] == 'target-repo', \
            "Should checkout to 'target-repo' path"
        assert checkout_step['with']['fetch-depth'] == 0, \
            "Should fetch full git history"


class TestPythonSetup:
    """Test Python environment setup."""

    def test_python_setup_step(self, workflow_config):
        """Test Python setup configuration."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        python_step = next(
            (s for s in steps if s.get('name') == 'Set up Python'),
            None
        )

        assert python_step is not None, "Python setup step must exist"
        assert python_step['uses'] == 'actions/setup-python@v4', \
            "Should use setup-python@v4 action"
        assert python_step['with']['python-version'] == '3.11', \
            "Should use Python 3.11"


class TestDependencyInstallation:
    """Test dependency installation step."""

    def test_install_dependencies_step(self, workflow_config):
        """Test dependency installation configuration."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        install_step = next(
            (s for s in steps if s.get('name') == 'Install Dependencies'),
            None
        )

        assert install_step is not None, "Install dependencies step must exist"
        assert 'run' in install_step, "Install step must have 'run' command"
        assert 'cd code-review' in install_step['run'], \
            "Should change to code-review directory"
        assert 'pip install -r requirements.txt' in install_step['run'], \
            "Should install dependencies from requirements.txt"


class TestCodeReviewExecution:
    """Test code review execution step."""

    def test_code_review_step(self, workflow_config):
        """Test code review execution configuration."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        review_step = next(
            (s for s in steps if s.get('name') == 'Run Mulesoft Code Review'),
            None
        )

        assert review_step is not None, "Code review step must exist"
        assert 'env' in review_step, "Code review step must have environment variables"
        assert 'run' in review_step, "Code review step must have 'run' command"

    def test_code_review_environment_variables(self, workflow_config):
        """Test environment variables for code review."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        review_step = next(
            (s for s in steps if s.get('name') == 'Run Mulesoft Code Review'),
            None
        )

        required_env_vars = ['GITHUB_TOKEN', 'OPENAI_API_KEY', 'REPO_NAME', 'PR_NUMBER']

        for env_var in required_env_vars:
            assert env_var in review_step['env'], \
                f"Environment variable '{env_var}' must be configured"

    def test_code_review_command(self, workflow_config):
        """Test code review execution command."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        review_step = next(
            (s for s in steps if s.get('name') == 'Run Mulesoft Code Review'),
            None
        )

        assert 'cd code-review' in review_step['run'], \
            "Should change to code-review directory"
        assert 'python mulesoft_enhanced_validation.py' in review_step['run'], \
            "Should execute mulesoft_enhanced_validation.py"


class TestSecretsConfiguration:
    """Test secrets usage in the workflow."""

    def test_pat_token_secret(self, workflow_config):
        """Test PAT_TOKEN secret usage."""
        workflow_str = yaml.dump(workflow_config)
        assert 'secrets.PAT_TOKEN' in workflow_str, \
            "Workflow must use PAT_TOKEN secret"

    def test_openai_api_key_secret(self, workflow_config):
        """Test OPENAI_API_KEY secret usage."""
        workflow_str = yaml.dump(workflow_config)
        assert 'secrets.OPENAI_API_KEY' in workflow_str, \
            "Workflow must use OPENAI_API_KEY secret"


class TestArtifactUpload:
    """Test artifact upload configuration."""

    def test_upload_artifacts_step(self, workflow_config):
        """Test artifact upload step configuration."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        upload_step = next(
            (s for s in steps if s.get('name') == 'Upload Review Artifacts'),
            None
        )

        assert upload_step is not None, "Upload artifacts step must exist"
        assert upload_step['uses'] == 'actions/upload-artifact@v4', \
            "Should use upload-artifact@v4 action"
        assert upload_step.get('if') == 'always()', \
            "Should upload artifacts always, even on failure"

    def test_artifact_configuration(self, workflow_config):
        """Test artifact upload configuration details."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        upload_step = next(
            (s for s in steps if s.get('name') == 'Upload Review Artifacts'),
            None
        )

        assert upload_step['with']['name'] == 'code-review-results', \
            "Artifact name should be 'code-review-results'"
        assert upload_step['with']['path'] == 'code-review/review-results.json', \
            "Artifact path should be 'code-review/review-results.json'"
        assert upload_step['with']['retention-days'] == 30, \
            "Artifact retention should be 30 days"


class TestWorkflowBestPractices:
    """Test workflow best practices and edge cases."""

    def test_all_steps_have_names(self, workflow_config):
        """Test that all steps have descriptive names."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        for i, step in enumerate(steps):
            assert 'name' in step, f"Step at index {i} must have a 'name' field"
            assert len(step['name']) > 0, f"Step at index {i} must have a non-empty name"

    def test_actions_use_specific_versions(self, workflow_config):
        """Test that all actions use specific versions (not @main or @master)."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        for step in steps:
            if 'uses' in step:
                action = step['uses']
                assert '@main' not in action and '@master' not in action, \
                    f"Action '{action}' should use specific version, not @main or @master"

    def test_no_hardcoded_credentials(self, workflow_config):
        """Test that no hardcoded credentials exist in workflow."""
        workflow_str = yaml.dump(workflow_config).lower()

        # Check for common patterns that might indicate hardcoded credentials
        sensitive_patterns = ['password:', 'api_key:', 'token:', 'secret:']

        for pattern in sensitive_patterns:
            if pattern in workflow_str:
                # Make sure it's referencing secrets, not hardcoded
                assert 'secrets.' in workflow_str, \
                    f"Found '{pattern}' - ensure it uses GitHub secrets"


class TestEdgeCases:
    """Test edge cases and regression scenarios."""

    def test_step_order_is_correct(self, workflow_config):
        """Test that steps are in logical order."""
        job = workflow_config['jobs']['mulesoft-code-review']
        step_names = [step.get('name', '') for step in job['steps']]

        # Checkouts should come before setup
        checkout_indices = [i for i, name in enumerate(step_names)
                           if 'Checkout' in name]
        python_index = next((i for i, name in enumerate(step_names)
                           if 'Set up Python' in name), None)

        if python_index is not None:
            for checkout_idx in checkout_indices:
                assert checkout_idx < python_index, \
                    "Checkout steps should come before Python setup"

    def test_working_directory_consistency(self, workflow_config):
        """Test that working directories are used consistently."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        # Count steps that use code-review directory
        code_review_steps = [s for s in steps
                           if 'run' in s and 'cd code-review' in s['run']]

        assert len(code_review_steps) >= 2, \
            "Should have at least 2 steps using code-review directory"

    def test_artifact_upload_runs_on_failure(self, workflow_config):
        """Test that artifacts are uploaded even when previous steps fail."""
        job = workflow_config['jobs']['mulesoft-code-review']
        steps = job['steps']

        upload_step = next(
            (s for s in steps if s.get('name') == 'Upload Review Artifacts'),
            None
        )

        assert upload_step.get('if') == 'always()', \
            "Artifacts should be uploaded even on failure for debugging"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])