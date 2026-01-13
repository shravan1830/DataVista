from subprocess import run
from os import remove

js_file = "command.js"


def write_mongo_file(query) -> None:

    query += ".toArray()"

    with open(js_file, "w+") as cmd_file:
        cmd_file.write(f"console.log(JSON.stringify({query}));")


def clean_mongo_file() -> None:
    remove(js_file)


def run_mongo_query(user, db, password, query) -> str:

    # Add support for login credentials

    write_mongo_file(query)

    if user == '' or password == '':
        command = f"mongosh {db} {js_file}"
    else:
        command = f"mongosh {db} --username {user} --password {password} {js_file}"

    output = run(["cmd", "/c", command], capture_output=True)

    if output.returncode:
        raise Exception(output.stderr.decode())

    clean_mongo_file()
    
    return output.stdout.decode()
