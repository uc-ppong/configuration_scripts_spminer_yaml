import os
import sys
import re
import yaml


def replace_placeholders(spingest_section_name, total_ingest):
    # Read the YAML file
    with open('00_SYSTEM_SPDATA.yaml', 'r') as yaml_file:
        config_data = yaml.safe_load(yaml_file)

    # Initialize an empty string to store the configuration data
    system_content = ""

    # Write the SYSTEM section to the string
    system_content += "[SYSTEM]\n"
    for key, value in config_data['SYSTEM'].items():
        system_content += f"SYSTEM.{key}={value}\n"

    # Write the SPDATA section to the string
    system_content += "\n[SPDATA]\n"
    for key, value in config_data['SPDATA'].items():
        system_content += f"SPDATA.{key}={value}\n"

    # Read the contents of 01_SPINGEST_HEADER.txt
    with open('01_INGEST_HEADER.yaml', 'r') as yaml_file:
        ingest_data = yaml.safe_load(yaml_file)

    yaml_ingest_key = "SPINGEST"
    # Replace the value of TOTAL_MINE
    ingest_data[yaml_ingest_key]['TOTAL_MINE'] = total_ingest

    # Initialize an empty string to store the configuration data
    template_content = ""

    # Write the section to the string
    template_content += f"[{spingest_section_name}]\n"
    for key, value in ingest_data[yaml_ingest_key].items():
        template_content += f"{spingest_section_name}.{key}={value}\n"

    # Combine the contents
    output_content = system_content + '\n' + template_content

    # Sort the filenames that start with '2' followed by two digits and then any characters
    pattern = re.compile(r'^2\d{2}.*')
    sorted_files = sorted([f for f in os.listdir('.') if pattern.match(f)])

    # Debug: Print the sorted files for verification
    print("Files matching pattern '2xx':", sorted_files)

    # Append the content of the sorted files
    for idx, filename in enumerate(sorted_files):
        print(f"Processing file: {filename}")  # Debug: Print the filename being processed
        with open(filename, 'r') as file:
            # Read the YAML content
            file_content = yaml.safe_load(file)
            print(f"File content: {file_content}")  # Debug: Print the content of the file

            # Replace placeholders in each file's content and convert to required format
            for key, value in file_content.items():
                output_content += "\n\n"
                # New MINE
                if isinstance(value, dict):
                    output_content += f"##{key} - {value.get('name', '')}\n"
                    for sub_key, sub_value in value.items():
                        #output_content += "\n"
                        if isinstance(sub_value, dict):
                            for sub_sub_key, sub_sub_value in sub_value.items():
                                print(
                                    f"Processing key-value pair: {sub_sub_key} - {sub_sub_value}")  # Debug: Print key-value pairs
                                if sub_sub_key is False:
                                    output_content += f"{spingest_section_name}.{key}_{sub_key}_OFF={sub_sub_value}\n"
                                elif isinstance(sub_sub_value, str) or isinstance(sub_sub_value, int):
                                    # DEST
                                    output_content += f"{spingest_section_name}.{key}_{sub_key}_{sub_sub_key}={sub_sub_value}\n"
                                elif isinstance(sub_sub_value, list):
                                    # MINELOG
                                    for i, minelog in enumerate(sub_sub_value):
                                        output_content += "\n"
                                        for log_key, log_value in minelog.items():
                                            output_content += f"{spingest_section_name}.{key}_{sub_key}_MINELOG{i}_{log_key}={log_value}\n"
                        elif isinstance(sub_value, str) or isinstance(sub_value, int):
                            output_content += f"{spingest_section_name}.{key}_{sub_key}={sub_value}\n"

    # Write to the output file
    with open('simplified_output.txt', 'w') as output_file:
        output_file.write(output_content)


def replace_miner_placeholders(spminer_section_name, total_miner):
    # Read the existing contents of the output file
    with open('simplified_output.txt', 'r') as system_file:
        system_content = system_file.read()

    # # Read the contents of 03_SPMINER_HEADER.txt
    # with open('03_SPMINER_HEADER.txt', 'r') as template_file:
    #     template_content = template_file.read()
    #
    # # Replace placeholders in the template content
    # template_content = template_content.replace('{spminer_section_name}', spminer_section_name)
    # template_content = template_content.replace('{total_miner}', str(total_miner))

    # Read the contents of 01_SPINGEST_HEADER.txt
    with open('02_MINER_HEADER.yaml', 'r') as yaml_file:
        ingest_data = yaml.safe_load(yaml_file)

    yaml_miner_key = "SPMINER"
    # Replace the value of TOTAL_MINE
    ingest_data[yaml_miner_key]['TOTAL_MINE'] = total_miner

    # Initialize an empty string to store the configuration data
    template_content = ""

    # Write the section to the string
    template_content += f"[{spminer_section_name}]\n"
    for key, value in ingest_data[yaml_miner_key].items():
        template_content += f"{spminer_section_name}.{key}={value}\n"

    # Combine the contents
    output_content = system_content + '\n' + template_content

    # Sort the filenames that start with '3' followed by two digits and then any characters
    pattern = re.compile(r'^3\d{2}.*')
    sorted_files = sorted([f for f in os.listdir('.') if pattern.match(f)])

    # Debug: Print the sorted files for verification
    print("Files matching pattern '3xx':", sorted_files)

    # Append the content of the sorted files
    for idx, filename in enumerate(sorted_files):
        print(f"Processing file: {filename}")  # Debug: Print the filename being processed
        with open(filename, 'r') as file:
            # Read the YAML content
            file_content = yaml.safe_load(file)
            print(f"File content: {file_content}")  # Debug: Print the content of the file

            # Replace placeholders in each file's content and convert to required format
            for key, value in file_content.items():
                output_content += "\n\n"
                if isinstance(value, dict):
                    # MINE level
                    output_content += f"##{key} - {value.get('name', '')}\n"
                    output_content += "\n"
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, dict):
                            #Each DEST
                            output_content += "\n"
                            for sub_sub_key, sub_sub_value in sub_value.items():
                                print(
                                    f"Processing key-value pair: {sub_sub_key} - {sub_sub_value}")  # Debug: Print key-value pairs
                                if sub_sub_key is False:
                                    output_content += f"{spminer_section_name}.{key}_{sub_key}_OFF={sub_sub_value}\n"
                                elif isinstance(sub_sub_value, str) or isinstance(sub_sub_value, int):
                                    output_content += f"{spminer_section_name}.{key}_{sub_key}_{sub_sub_key}={sub_sub_value}\n"
                                elif isinstance(sub_sub_value, list):
                                    output_content += "\n"
                                    for i, minelog in enumerate(sub_sub_value):
                                        for log_key, log_value in minelog.items():
                                            output_content += f"{spminer_section_name}.{key}_{sub_key}_MINELOG{i}_{log_key}={log_value}\n"
                        elif isinstance(sub_value, str) or isinstance(sub_value, int):
                            output_content += f"{spminer_section_name}.{key}_{sub_key}={sub_value}\n"

    # Read the contents of 400_SPMERGE.txt
    # with open('400_SPMERGE.txt', 'r') as spmerge_file:
    #   merge_content = spmerge_file.read()
    #   output_content += '\n' + merge_content

    with open('400_SPMERGE.yaml', 'r') as spmerge_file:
        merge_content = yaml.safe_load(spmerge_file)

    # Write the SYSTEM section to the string
    output_content += "\n[SPMERGE]\n"
    for key, value in merge_content['SPMERGE'].items():
        output_content += f"SPMERGE.{key}={value}\n"

    # Write to the output file
    with open('mocn_gx_report.properties', 'w') as output_file:
        output_file.write(output_content)


def count_files_with_prefix(directory, prefix):
    pattern = re.compile(r'^{}\d{{2}}.*'.format(prefix))
    count = 0
    for filename in os.listdir(directory):
        if pattern.match(filename):
            count += 1
    return count


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <spingest_section_name> <spminer_section_name>")
        sys.exit(1)

    spingest_section_name = sys.argv[1]
    spminer_section_name = sys.argv[2]
    directory = '.'  # Current directory, you can change this to any directory you want to scan

    prefix = '2'
    total_ingest = count_files_with_prefix(directory, prefix)
    replace_placeholders(spingest_section_name, total_ingest)

    prefix = '3'
    total_miner = count_files_with_prefix(directory, prefix)
    replace_miner_placeholders(spminer_section_name, total_miner)

    print(
        f"Output written to mocn_gx_report.properties with section name '{spingest_section_name}' and total ingest '{total_ingest}'")
    print(
        f"Output written to mocn_gx_report.properties with section name '{spminer_section_name}' and total miner '{total_miner}'")
