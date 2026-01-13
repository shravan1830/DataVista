from subprocess import run
from json import loads
# from fix_busted_json import repair_json
db_name = "employee_db"
js_file = "command.js"
cmd_str = "db.salary_data.find({})"
cmd_str += ".toArray()"

# console.log(output)"

# with open(js_file, "w+") as cmd_file:
#     cmd_file.write(f"console.log({cmd_str});")

command = f"mongosh {db_name} {js_file}"


# run(["cmd","/c",command])

# print(output)
# import subprocess
# output = subprocess.run(["cmd","/c",command], capture_output=True)

# if output.returncode:
#     raise Exception(output.stderr.decode())


# print(output.stdout.decode())

he = {"hi":"abc","hello":"cde"}

hi, hello = he.values()
print(hi,hello)