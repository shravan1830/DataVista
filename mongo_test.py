import subprocess

# Start a shell process

try:
    process = subprocess.Popen(
        'mongosh',  # 'bash' for Linux/macOS, 'cmd' for Windows
        stdin= subprocess.PIPE,  # Allow us to send commands to the process
        stdout= subprocess.PIPE,  # Capture output
        stderr= subprocess.PIPE,  # Capture errors
        universal_newlines=True  # Text mode (strings rather than bytes)
    )
except FileNotFoundError:
    raise FileNotFoundError("Please install mongosh and set environment path for the same.")

# Commands to execute
commands = [
    "use employee_db;",
    "db.salary_data.find({})",
]

# Execute each command one by one
# output, errors = '', ''
# for cmd in commands:
#     process.stdin.write(cmd + '\n')  
#     process.stdin.flush()    
  
# output, errors = process.communicate() 

# # # Print the result
# print(output)
# # print(re.split("^> | ^bye",output))
# # print("Output:\n", output.split(">"))

# if len(errors):
#     print("Errors (if any):\n", errors)


try:
    ans = process.check_output(["cmd.exe"], text=True)
    print(ans)

except subprocess.CalledProcessError as e:
    print(f"Command failed with return code {e.returncode}")