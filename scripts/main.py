from triage import trier
from dashboad import show_dashboard
import os

def ask(command:str):
    command = command.split(" ")
    if command[0] == "help":
        print("sort [InputPath] ([OutputPath]): sorts tickets using an ollama LLM. OutputPath optional")
        print("exit : exists program")
        print("help : shows list of commands and arguments")
        print("dashboard [Path] : makes a dashboard out of a generated json file")
        return False
    if command[0] == "sort":
        if len(command)>=2 and os.path.exists(command[1]):
            if len(command)==3:
                trier(command[1], command[2])
                print("Your file has been generated at " + command[2])
            else:
                trier(command[1], "outputs/results.json")
                print("Your file has been generated at outputs/results.json")    
        return False    
    if command[0] == "dashboard":
        print(command)
        if len(command)== 2 and os.path.exists(command[1]):
            show_dashboard(command[1])
        return False
    if command[0] == "exit":
        return True
    print("Invalid Command")

if __name__ == "__main__":
    print("-- Welcome to SortingBot\n")
    exit = False
    while not exit:
       exit = ask(str(input("> use help for a list of commands : ")))


