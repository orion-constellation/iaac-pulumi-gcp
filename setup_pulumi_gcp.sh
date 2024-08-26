#!/bin/bash

# Function to check and authenticate with gcloud if not already authenticated
authenticate_gcloud() {
  echo "Authenticating with Google Cloud..."
  gcloud auth application-default login
}

# Function to set the Google Cloud project for Pulumi
set_gcp_project() {
  echo "Retrieving current Google Cloud project..."
  current_project=$(gcloud config get-value project)
  echo "Current Google Cloud project is: $current_project"

  read -p "Would you like to change the current project? (yes/no): " change
  if [[ "$change" == "yes" || "$change" == "y" ]]; then
    echo "Fetching available projects..."
    projects=$(gcloud projects list --format="value(projectId)")
    project_array=($projects)
    
    echo "Available Google Cloud projects:"
    for i in "${!project_array[@]}"; do
      echo "$((i+1)). ${project_array[$i]}"
    done

    read -p "Enter the number of the project you want to select: " project_number
    if [[ "$project_number" -ge 1 && "$project_number" -le "${#project_array[@]}" ]]; then
      selected_project=${project_array[$((project_number-1))]}
      echo "Setting Google Cloud project to: $selected_project"
      pulumi config set gcp:project $selected_project
      gcloud config set project $selected_project
    else
      echo "Invalid selection. Exiting..."
      exit 1
    fi
  else
    echo "Using the current project: $current_project"
    pulumi config set gcp:project $current_project
  fi
}

# Function to ensure Pulumi is properly configured
configure_pulumi() {
  echo "Ensuring Pulumi is properly configured..."
  pulumi stack select || pulumi stack init
}

# Main script execution
echo "Starting setup for Pulumi with Google Cloud..."

authenticate_gcloud

set_gcp_project

configure_pulumi

echo "Setup complete. You are now ready to use Pulumi with Google Cloud."
