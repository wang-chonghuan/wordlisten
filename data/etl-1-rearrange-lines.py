def process_file(input_filename):
    output_filename = 'output-etl-1-' + input_filename
    with open(input_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Step 1: Remove lines containing only 'Strong', 'Example', 'Play'
    lines = [line for line in lines if line.strip() not in {'Strong', 'Example', 'Play'}]

    # Step 2: Insert empty line between every four non-empty lines and replace two consecutive empty lines with one
    processed_lines = []
    non_empty_count = 0
    previous_was_empty = False

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            non_empty_count += 1
            if non_empty_count == 3:
                processed_lines.append('\n')
            processed_lines.append(line)
            previous_was_empty = False
        else:
            if not previous_was_empty:
                processed_lines.append(line)
            previous_was_empty = True
            non_empty_count = 0

    # Handle case where last line might be empty
    if processed_lines and processed_lines[-1].strip() == '':
        processed_lines.pop()

    # Write to output file
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)

# Replace 'busuu-de-a1-480.txt' with the path to your actual file if different
process_file('words.txt')
