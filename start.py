import subprocess
from os.path import exists

print("\nWelcome!\n")

workspaces = []

print("Available Workspaces: ")
f = open("data\workspaces.txt", "r")
for x in f:
  workspaces.append(x.replace('\n', ''))
  print(x)
f.close


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