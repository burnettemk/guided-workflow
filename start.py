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


if __name__ == "__main__":
  print("\nWelcome!\n")

  workspaces = []

  if exists("data") == False:
    subprocess.run(["mkdir", "data"], shell=True)

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

  # Check for folder existence. It it exists, open file explorer in that folder and run created .bat file

  # Create Workspace folder
  file_path = 'data/' + workspace + '/' + workspace + '.bat'

  if exists('data/' + workspace + '/' + workspace + '.bat'):

    # Call start.bat to run the workspace
    print("Starting workspace...")
    
    return_code = subprocess.call('start.bat ' + 'data/' + workspace + ' ' + workspace + '.bat')
    if return_code == 0:
      print("Command executed successfully.")
    else:
      print("Command failed with return code", return_code)

    # Find directory
    f = open('data/directoryList.txt')
    for dir in f:
      if dir.__contains__(workspace):

        # Open Workspace Directory
        print("Opening workspace folder...")

        return_code = subprocess.call(['start', 'C:\Windows\explorer', dir], shell=True)
        if return_code == 0:
          print("Command executed successfully.")
        else:
          print("Command failed with return code", return_code)
    f.close

  else:
    print("\nNo workspace named '" + workspace + "' is available")
    # prompt user again

  # subprocess.call(["src\createDir.bat", workspace])