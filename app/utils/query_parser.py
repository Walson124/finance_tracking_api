def parse_query(file_path, **kwargs):
    """
    Parses an SQL file, replaces placeholders (including brackets) with provided keyword arguments,
    and returns the SQL string.

    Args:
        file_path (str): Path to the SQL file.
        **kwargs: Keyword arguments to replace placeholders in the SQL file.

    Returns:
        str: The SQL file content with placeholders replaced.
    """
    try:
        # Read the SQL file
        with open(file_path, 'r') as file:
            sql_content = file.read()

        # Replace placeholders with corresponding values from kwargs
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"  # Placeholder format: {key}
            
            # Check if the value is a string
            if isinstance(value, str):
                # Ensure the string is inserted without quotes
                sql_content = sql_content.replace(placeholder, value)
            else:
                # For other types (e.g., numbers), just replace directly without quotes
                sql_content = sql_content.replace(placeholder, str(value))

        return sql_content
    except FileNotFoundError:
        raise FileNotFoundError(f"SQL file not found at path: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while parsing the SQL file: {e}")
