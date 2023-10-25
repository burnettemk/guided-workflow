import subprocess
import os
from os.path import exists

def create_workspace():
  # Prompt User for details
  print("Give this workspace a name: \n")
  workspace_name = input()
  f = open("data\workspaces.txt", 'w')
  f.write(workspace_name)
  f.close()

  # Create Directory
  os.mkdir("C:/Users/waffl/Workspaces/" + workspace_name)

  # Prompt user for application path


def run_subprocess(process):
  if process == "explorer":
    return_code = subprocess.call(['start', 'C:\Windows\explorer', workspace], shell=True)
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


def generate_bat():
  print()


if __name__ == "__main__":
  cwd = os.getcwd()
  print("\nWelcome!\n")

  workspaces = []

  if exists("data") == False:
    os.mkdir("data")

  if exists("data\workspaces.txt"):
    print("Available Workspaces: ")
    f = open("data\workspaces.txt", "r")
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

  for n in workspaces:
    if workspace == n:
      print("You've chosen to work with: " + n)

  # Check for folder existence. If it exists, open file explorer in that folder and run created .bat file

  # Create Workspace folder
  file_path = 'data/' + workspace + '.bat'

  if exists(file_path):

    # Call start.bat to run the workspace
    print("Starting workspace...")

    run_subprocess("cmd")

    # Find directory
    f = open('data/directoryList.txt')
    os.chdir('C:/Users/waffl/Workspaces')

    if exists(workspace):
      print("Opening workspace folder...")
      run_subprocess("explorer")
    else:
      print("Creating workspace folder...")
      os.mkdir(workspace)
      run_subprocess("explorer")
    
    f.close

    os.chdir(cwd)

  else:
    print("Associated .bat or .cmd file not found.\nGenerating new .bat file...")
    # prompt user again

  # subprocess.call(["src\createDir.bat", workspace])