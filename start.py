import subprocess
import os
from os.path import exists


def create_workspace():
  # Prompt User for details
  print("Give this workspace a name: \n")
  workspace_name = input()
  f = open("data/workspaces.txt", 'a')
  f.write('\n' + workspace_name)
  f.close()

  # Create Directory
  os.mkdir("C:/Users/waffl/Workspaces/" + workspace_name)

  # Generate batch file
  generate_bat(workspace_name)


def run_subprocess(process, cwd = "", workspace = ""):
  if process == "explorer":
    return_code = subprocess.call(['start', 'C:/Windows/explorer', workspace], shell=True)
    if return_code == 0:
      print("Command executed successfully.")
    else:
      print("Command failed with return code", return_code)
  elif process == "cmd":
    os.chdir('data')

    return_code = subprocess.call([workspace + '.bat'], shell=True)
    if return_code == 0:
      print("Command executed successfully.")
    else:
      print("Command failed with return code", return_code)
    
    os.chdir(cwd)


def generate_bat(wrkspc_name: str):
  workspace = wrkspc_name
  wrkspc_dir : str = ""
  wrkspc_file : str = ""
  cont = True

  while cont:
    wrkspc_dir = input("Paste the path of the directory of the file you wish to open: ")
    wrkspc_file = input("Paste the name of the file you wish to open: ")

    f = open("data/" + wrkspc_name + '.bat', 'x')
    f.write("@echo off\n")
    f.write("cd " + '\"' + wrkspc_dir + '\"' + '\n')
    f.write("start " + wrkspc_file + '\n')

    if input("Do you want to add another file/program? Y/N ") == 'N' or 'n':
      cont = False
  
  f.close()


def start_workspace(wrkspc_name : str):
  # Check for folder existence. If it exists, open file explorer in that folder and run created .bat file
  file_path = 'data/' + workspace + '.bat'

  if exists(file_path):

    # Call start.bat to run the workspace
    print("Starting workspace...")

    run_subprocess("cmd", cwd, workspace)

    # Find directory
    os.chdir('C:/Users/waffl/Workspaces')

    if exists(workspace):
      print("Opening workspace folder...")
      run_subprocess("explorer", workspace)
    else:
      print("Creating workspace folder...")
      os.mkdir(workspace)
      run_subprocess("explorer", workspace)

    os.chdir(cwd)
  else:
    print("Associated .bat or .cmd file not found.\nGenerating new .bat file...")
    generate_bat(workspace)

    start_workspace(workspace)



if __name__ == "__main__":
  cwd = os.getcwd()
  print("\nWelcome!\n")

  workspaces = []

  if exists("data") == False:
    os.mkdir("data")

  if exists("data/workspaces.txt"):
    print("Available Workspaces: ")
    f = open("data/workspaces.txt", "r")
    for x in f:
      workspaces.append(x.replace('\n', ''))
      print(x)
    f.close
  else:
    print("No workspaces found. Would you like to make one? Y/N")
    res = input()
    if res == 'Y' or res == 'y':
      create_workspace() 
    elif res == 'N' or res == 'n':
      print("Program closed.")
      exit()
  
  workspace = input("Choose your workspace: ")
  
  if workspace != 'n' or 'new':
    for n in workspaces:
      if workspace == n:
        print("You've chosen to work with: " + n)
        start_workspace(workspace)
  
  match workspace:
    case 'exit':
      print("Closing program...")
      exit()
    case 'new':
      create_workspace()
      start_workspace(workspace)
    case 'n':
      create_workspace()
      start_workspace(workspace)

