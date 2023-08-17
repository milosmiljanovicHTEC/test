import re
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-pr', '--path_to_readme', type=str, required=True, default="workflows/README.md", help="Location where is stored README.md")
parser.add_argument('-py', '--path_to_yaml', type=str, required=True, default="workflows", help="Folder which contains YAML files")
args = parser.parse_args()

def update_readme_for_missing_files(workflows_folder, readme_path):
    def remove_yaml_section(readme_content, yaml_filename):
        start_pattern = f"## `{yaml_filename}`"
        end_pattern = "\n\n---"

        start_index = readme_content.find(start_pattern)
        if start_index == -1:
            return readme_content

        end_index = readme_content.find(end_pattern, start_index)
        if end_index == -1:
            return readme_content

        section = readme_content[start_index:end_index+len(end_pattern)]
        updated_readme_content = readme_content.replace(section, "")
        return updated_readme_content

    # Read the README.md content
    with open(readme_path, "r") as readme_file:
        readme_content = readme_file.read()

    # Extract names from README.md
    headings = []
    lines = readme_content.split('\n')
    for line in lines:
        if line.startswith("## `") and line.endswith("`"):
            headings.append(line[4:-1])

    # List yaml files in workflows folder
    workflow_files = [file for file in os.listdir(workflows_folder) if file.endswith('.yml')]

    # Find missing files
    missing_files = set(headings) - set(workflow_files)
    # Update the README.md content
    updated_readme_content = readme_content
    for missing_file in missing_files:
        updated_readme_content = remove_yaml_section(updated_readme_content, missing_file)

    # Write the updated content back to README.md
    with open(readme_path, "w") as readme_file:
        readme_file.write(updated_readme_content)

    print("Sections removed from README.md for missing files:", missing_files)

def extract_variable_names_with_comments(yaml_file_content):
    pattern = r'(?s)env:(.*?)\n\s*jobs:'
    match = re.search(pattern, yaml_file_content)
    if match:
        env_block = match.group(1)
        env_variables = re.findall(r'^\s*(\w+)\s*:(?:.*?#(.*))?(?:\n|$)', env_block, re.MULTILINE)
        return env_variables
    return None


def params(readme_path, yaml_file):
    # Read the content of README.md file
    with open(readme_path, 'r') as readme_file:
        readme_content = readme_file.read()

    # Extract only the filename from the path
    yaml_filename = os.path.basename(yaml_file)

    # Search for '## `yaml.file`' in README.md
    match = re.search(r"## `{}`".format(re.escape(yaml_filename)), readme_content)
    if match:
        start_index = match.start()
        input_params_start = re.search(r"- ## Input Parameters", readme_content[start_index:], re.DOTALL)
        if input_params_start:
            input_params_start = start_index + input_params_start.start()
            input_params_end = re.search(r"\n\n[-*] ##", readme_content[input_params_start:]).start()
            input_params_section = readme_content[input_params_start:input_params_start + input_params_end]

            # Extract the input parameters from the YAML file
            with open(yaml_file, 'r') as yaml_file:
                yaml_content = yaml_file.read()
            input_params = re.findall(r"(\w+):\s*\n\s+type:\s+string\s*\n\s+description:\s+([^\n]*)", yaml_content, re.DOTALL)

            # Generate the new input parameters section
            new_input_params_section = "- ## Input Parameters\n\n"
            for param_name, param_desc in input_params:
                new_input_params_section += f"> - `{param_name}`: {param_desc}\n\n"

            # Add an empty line after each new row in the new input parameters section
            new_input_params_section = re.sub(r"\n", "\n", new_input_params_section)

            # Replace the old input parameters section with the new one
            new_readme_content = (
                readme_content[:input_params_start] +
                new_input_params_section +
                readme_content[input_params_start + input_params_end:]
            )
            new_readme_content = re.sub(r"\n\n+", "\n\n", new_readme_content)
            # Write the updated content to README.md
            with open(readme_path, 'w') as readme_file:
                readme_file.write(new_readme_content)
        else:
            print("Input Parameters section not found under '{}' in README.md.".format(yaml_filename))
    else:
        print("Block '{}' not found in README.md.".format(yaml_filename))

def insert_environment_variables(readme_path, yaml_file):
    with open(yaml_file, 'r') as file:
        yaml_content = file.read()

    variable_names_with_comments = extract_variable_names_with_comments(yaml_content)
    if variable_names_with_comments is not None:
        with open(readme_path, 'r') as readme_file:
            readme_content = readme_file.read()

        yaml_filename = os.path.basename(yaml_file)
        match = re.search(r"## `{}`".format(re.escape(yaml_filename)), readme_content)
        if match:
            start_index = match.start()
            env_variables_start = readme_content.find("- ## Environment Variables", start_index)
            env_variables_end = readme_content.find("- ##", env_variables_start + 1)

            # Extract the existing content before and after the environment variables block
            before_env_variables = readme_content[:env_variables_start]
            after_env_variables = readme_content[env_variables_end:]

            new_variables = [f">- `{name}`: {comment}" for name, comment in variable_names_with_comments]

            # Construct the new environment variables block
            new_env_variables_block = "- ## Environment Variables\n\n" + "\n\n".join(new_variables)

            # Construct the new content
            new_content = (
                before_env_variables +
                new_env_variables_block +
                "\n\n" +
                after_env_variables
            )

            with open(readme_path, 'w') as readme_file:
                readme_file.write(new_content)
        else:
            print("Block '{}' not found in README.md.".format(yaml_filename))
    else:
        print("No environment variables found in YAML file: {}".format(yaml_file))
def main():
    yaml_folder = args.path_to_yaml
    update_readme_for_missing_files(yaml_folder, args.path_to_readme)
    if not os.path.isdir(yaml_folder):
        print(f"Error: '{yaml_folder}' is not a valid directory.")
        return

    yaml_files = [file for file in os.listdir(yaml_folder) if file.endswith('.yml')]

    for yaml_file in yaml_files:
        yaml_file_path = os.path.join(yaml_folder, yaml_file)
        insert_environment_variables(args.path_to_readme, yaml_file_path)
        params(args.path_to_readme, yaml_file_path)

if __name__ == "__main__":
    main()