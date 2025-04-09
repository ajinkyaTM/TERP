import os
import xml.etree.ElementTree as ET
import subprocess

# Define paths (adjust these according to your project structure)
METADATA_DIR = 'force-app/main/default'  # Your Salesforce metadata directory
PACKAGE_XML = 'package.xml'
DESTRUCTIVE_XML = 'destructiveChanges.xml'

# Function to generate package.xml
def generate_package_xml(created_or_modified_components):
    # Create the root element for package.xml
    package = ET.Element("Package")
    package.set("xmlns", "http://soap.sforce.com/2006/04/metadata")

    # Create the metadata types and members for modified/created components
    for metadata_type, members in created_or_modified_components.items():
        types_element = ET.SubElement(package, "types")
        for member in members:
            member_element = ET.SubElement(types_element, "members")
            member_element.text = member
        name_element = ET.SubElement(types_element, "name")
        name_element.text = metadata_type

    # Add API version (Salesforce version you're working with)
    version_element = ET.SubElement(package, "version")
    version_element.text = "52.0"  # Adjust based on your Salesforce version

    # Convert the element tree to a string and save it
    tree = ET.ElementTree(package)
    tree.write(PACKAGE_XML, encoding='utf-8', xml_declaration=True)
    print(f"Generated {PACKAGE_XML}")

# Function to generate destructiveChanges.xml
def generate_destructive_xml(deleted_components):
    # Create the root element for destructiveChanges.xml
    destructive_changes = ET.Element("DestructiveChanges")
    destructive_changes.set("xmlns", "http://soap.sforce.com/2006/04/metadata")

    # Create the metadata types and members for deleted components
    for metadata_type, members in deleted_components.items():
        types_element = ET.SubElement(destructive_changes, "types")
        for member in members:
            member_element = ET.SubElement(types_element, "members")
            member_element.text = member
        name_element = ET.SubElement(types_element, "name")
        name_element.text = metadata_type

    # Convert the element tree to a string and save it
    tree = ET.ElementTree(destructive_changes)
    tree.write(DESTRUCTIVE_XML, encoding='utf-8', xml_declaration=True)
    print(f"Generated {DESTRUCTIVE_XML}")

# Function to compare two branches and identify changes
def get_changed_components(base_branch, target_branch):
    # Fetch changes from the git repository
    diff_command = f"git diff --name-status {base_branch}..{target_branch}"
    result = subprocess.run(diff_command, shell=True, capture_output=True, text=True)

    # Store components categorized by change type
    created_or_modified = {}
    deleted = {}

    # Parse the git diff output
    for line in result.stdout.splitlines():
        status, file_path = line.split('\t')
        # Assuming metadata is inside force-app/main/default or similar directory
        if file_path.startswith(METADATA_DIR):
            parts = file_path.split('/')
            metadata_type = parts[1]  # Folder indicates the type (e.g., ApexClass, CustomObject)
            metadata_name = parts[2]  # The name of the component
            
            # Handle created/modified components
            if status in ['M', 'A']:  # Modified or Added
                if metadata_type not in created_or_modified:
                    created_or_modified[metadata_type] = []
                created_or_modified[metadata_type].append(metadata_name)
            
            # Handle deleted components
            elif status == 'D':  # Deleted
                if metadata_type not in deleted:
                    deleted[metadata_type] = []
                deleted[metadata_type].append(metadata_name)

    return created_or_modified, deleted

if __name__ == "__main__":
    base_branch = "main"  # Replace with the base branch of the PR
    target_branch = "feature-branch"  # Replace with the feature branch

    # Get the changed components
    created_or_modified, deleted = get_changed_components(base_branch, target_branch)

    if created_or_modified:
        generate_package_xml(created_or_modified)
    else:
        print("No created or modified components.")

    if deleted:
        generate_destructive_xml(deleted)
    else:
        print("No deleted components.")
