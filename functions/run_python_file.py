import subprocess
import os


def run_python_file(working_directory, file_path, args=None):
    try:

        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.split(".", 1)[1] != "py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        command.extend(args)
        result = subprocess.run(
            command,
            capture_output=True,
            cwd=working_dir_abs,
            timeout=30,
            text=True,
        )
        output_str = ""
        if result.returncode != 0:
            output_str += f"Process exited with code {result.returncode} "
        if not result.stdout or not result.stderr:
            output_str += "No output produced"
        output_str += f"STDOUT: {result.stdout}" + f"STDERR: {result.stderr}"

        return output_str

    except Exception as e:
        return f"Error: executing Python file: {e}"
