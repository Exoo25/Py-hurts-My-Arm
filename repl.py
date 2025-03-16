import os
print("Pyhton REPL", "type python code to execute")
print("Type 'exit' to exit the REPL")
code = input(">>> ")
while code != "exit":
    try:
        if code == "clear":
            os.system("cls")
            print("Pyhton REPL", "type python code to evalute")
            print("Type 'exit' to exit the REPL")
            code = input(">>> ")
        else:
            exec(code)
            code = input(">>> ")
    except Exception as e:
        print(e)
        code = input(">>> ")




