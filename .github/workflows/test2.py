import re
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('-pr', '--path_to_readme', type=str, required=True, default="README.md", help="Location where is stored readme.md")
# parser.add_argument('-py', '--path_to_yaml', type=str, required=True, default="test.yml", help="location where are stored yaml files")
# args = parser.parse_args()

def extract_variable_names_with_comments(yaml_file):
    with open(yaml_file, 'r') as file:
        content = file.read()
    pattern = r'(?s)env:(.*?)\n\s*jobs:'
    match = re.search(pattern, content)
    if match:
        env_block = match.group(1)
        env_variables = re.findall(r'(\w+)\s*:(?:.*?#(.*))?(?:\n|$)', env_block)
        return env_variables

    return None


def replace_variable_values(readme_path, variable_names_with_comments):
    with open(readme_path, 'r') as file:
        content = file.read()

    for variable in variable_names_with_comments:
        pattern = fr'- `{variable[0]}`:.*'
        replacement = f'- `{variable[0]}`: {variable[1]}'
        content = re.sub(pattern, replacement, content)

    with open(readme_path, 'w') as file:
        file.write(content)

def find_start_of_yaml_block(content, yaml_file):
    pattern = fr'^## `{yaml_file}`'
    match = re.search(pattern, content, re.MULTILINE)
    if match:
        return match.start()
    else:
        return -1

    
def next_line(content, start_index, target_line):
    lines = content.splitlines()
    for i in range(start_index, len(lines)):
        if lines[i].strip() == target_line.strip():
            return len('\n'.join(lines[:i])) + len(lines[i])
    return len(content)

def find_end_of_env_variables(content, start_index):
    end_index = content.find("- ##", start_index)
    if end_index == -1:
        end_index = len(content)
    return end_index



def insert_environment_variables(readme_path, yaml_file, variable_names_with_comments):
    with open(readme_path, 'r') as file:
        content = file.read()

    start_index = find_start_of_yaml_block(content, yaml_file)
    if start_index == -1:
        print(f"YAML file block for {yaml_file} not found in README.md")
        return

    env_variables_start = content.index("- ## Environment Variables", start_index)
    env_variables_end = content.index("- ##", env_variables_start + 1)

    existing_variables = re.findall(r'>- `([^`]+)`:', content[env_variables_start:env_variables_end])
    variables_to_insert = [(variable, comment) for variable, comment in variable_names_with_comments if variable not in existing_variables]

    # Remove variables from the 'Environment Variables' section
    variables_to_delete = [variable for variable in existing_variables if variable not in [v[0] for v in variable_names_with_comments]]
    updated_lines = []

    for line in content[env_variables_start:env_variables_end].splitlines():
        match = re.match(r'>- `([^`]+)`:(.*)', line)
        if match:
            variable = match.group(1).strip()
            comment = match.group(2).strip()

            if variable in variables_to_delete:
                continue

            updated_lines.append(line)

    if variables_to_insert:
        # Add new variables at the end
        for new_variable, new_comment in variables_to_insert:
            updated_lines.append(f">- `{new_variable}`: {new_comment}")

    new_content = content[:env_variables_start] + "- ## Environment Variables\n\n" + "\n".join(updated_lines) + "\n"
    new_content += content[env_variables_end:]

    with open(readme_path, 'w') as file:
        file.write(new_content)

    print("Environment variables inserted successfully in README.md")

    

def params(yaml_path):
    # Read the content of README.md file
    with open('README.md', 'r') as readme_file:
        readme_content = readme_file.read()
    
    # Read the content of the YAML file
    with open(yaml_path, 'r') as yaml_file:
        yaml_content = yaml_file.read()
    
    # Search for '## `yaml.file`' in README.md
    match = re.search(r"## `{}`".format(yaml_path), readme_content)
    if match:
        start_index = match.start()
        input_params_start = re.search(r"- ## Input Parameters", readme_content[start_index:], re.DOTALL)
        if input_params_start:
            input_params_start = start_index + input_params_start.start()
            input_params_end = re.search(r"\n\n[-*] ##", readme_content[input_params_start:]).start()
            input_params_section = readme_content[input_params_start:input_params_start + input_params_end]

            # Extract the input parameters from the YAML file
            with open(yaml_path, 'r') as yaml_file:
                yaml_content = yaml_file.read()
            input_params = re.findall(r"(\w+):\n\s+type:\s+string\n\s+description:\s+(.+)\n\s+required:", yaml_content)

            # Generate the new input parameters section
            new_input_params_section = "- ## Input Parameters\n"
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

            # Write the updated content to README.md
            with open('README.md', 'w') as readme_file:
                readme_file.write(new_readme_content)
        else:
            print("Input Parameters section not found under '{}' in README.md.".format(yaml_path))
    else:
        print("Block '{}' not found in README.md.".format(yaml_path))
yaml_file = "miopen-db.yml"
readme_path = "README.md"

hi = params(yaml_file)
variable_names_with_comments = extract_variable_names_with_comments(yaml_file)
replace_variable_values(readme_path, variable_names_with_comments)
insert_environment_variables(readme_path, yaml_file, variable_names_with_comments)

