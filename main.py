import os
import logging
import subprocess
import sys
import pulumi
from operations.common_operations import CommonOperations
from operations.compute_operations import ComputeOperations
from operations.vertexai_operations import VertexAIOperations
from operations.cloud_run_operations import CloudRunOperations
from operations.api_gateway_operations import ApiGatewayOperations
from operations.secrets_manager_operations import SecretsManagerOperations
from report import ReportService
from operations.cli import main as cli_main

# Setup logging
log_dir = './tmp/log'
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(log_dir, 'error.log'))
    ]
)

# Initialize operation classes
common_ops = CommonOperations()
compute_ops = ComputeOperations()
vertexai_ops = VertexAIOperations()
cloud_run_ops = CloudRunOperations()
api_gateway_ops = ApiGatewayOperations()
secrets_ops = SecretsManagerOperations()

def authenticate_gcloud():
    """Authenticate with gcloud CLI if not already authenticated."""
    try:
        result = subprocess.run(['gcloud', 'auth', 'list'], capture_output=True, text=True)
        if "ACTIVE" not in result.stdout:
            logging.info("No active gcloud authentication found. Authenticating...")
            subprocess.run(['gcloud', 'auth', 'login'], check=True)
        else:
            logging.info("Already authenticated with gcloud.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during gcloud authentication: {e}")
        sys.exit(1)

def get_gcloud_info():
    """Get the current Google Cloud project, region, and user information."""
    try:
        project = subprocess.run(['gcloud', 'config', 'get-value', 'project'], capture_output=True, text=True).stdout.strip()
        region = subprocess.run(['gcloud', 'config', 'get-value', 'compute/region'], capture_output=True, text=True).stdout.strip()
        if not region:
            region = "australia-southeast1"  # Set default region if not configured
            subprocess.run(['gcloud', 'config', 'set', 'compute/region', region], check=True)
        account = subprocess.run(['gcloud', 'config', 'get-value', 'account'], capture_output=True, text=True).stdout.strip()

        logging.info(f"Project: {project}")
        logging.info(f"Region: {region}")
        logging.info(f"User Account: {account}")

        return project, region, account
    except subprocess.CalledProcessError as e:
        logging.error(f"Error retrieving gcloud configuration: {e}")
        sys.exit(1)

def change_project():
    """Prompt the user to change the current Google Cloud project."""
    change = input("Would you like to change the current project? (yes/no): ").strip().lower()
    if change in ['yes', 'y']:
        new_project = input("Enter the new Google Cloud project ID: ").strip()
        try:
            subprocess.run(['gcloud', 'config', 'set', 'project', new_project], check=True)
            logging.info(f"Project changed to: {new_project}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error changing the project: {e}")
            sys.exit(1)

def summarize_active_services():
    """Summarize active services in the current Google Cloud project."""
    instances, buckets = common_ops.get_resources()

    summary = f"Active Compute Instances: {len(instances)}\nActive Storage Buckets: {len(buckets)}"
    logging.info("Active Services Summary:\n" + summary)
    return summary

def confirm_action(action_description):
    """Prompt the user to confirm a potentially destructive action."""
    confirmation = input(f"Are you sure you want to {action_description}? (yes/no): ").strip().lower()
    if confirmation not in ['yes', 'y']:
        logging.info(f"Action '{action_description}' cancelled by user.")
        sys.exit(0)

def stop_all_instances():
    """Stop all compute instances after user confirmation."""
    confirm_action("stop all compute instances")
    common_ops.stop_all_instances()

def delete_all_resources():
    """Delete all resources after user confirmation."""
    confirm_action("delete all resources")
    common_ops.delete_all_resources()

    # Generate report using ReportService


def main():
    """Main function to run the Google Cloud session summary and Pulumi operations."""
    authenticate_gcloud()
    project, region, account = get_gcloud_info()
    change_project()
    summarize_active_services()

    # Example of stopping all instances with confirmation
    stop_all_instances()

    # Example of deleting all resources with confirmation
    delete_all_resources()

    report_service = ReportService()
    report_service.generate_report()
    report_service.list_errors()
    # Example usage of Pulumi with initialized operation classes
    # Create a compute instance
    compute_instance = compute_ops.create_instance(name="my-instance", zone=region)

    # Query all resources and output to console
    common_ops.query_all_resources()

    # Create a VertexAI model
    vertexai_model = vertexai_ops.create_model(model_name="my-model", project_id=project, region=region)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If invoked from the CLI with arguments, handle with the CLI tool
        cli_main()
    else:
        # If invoked directly, run the main function
        main()
