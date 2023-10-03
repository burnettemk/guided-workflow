import subprocess
from os.path import exists

# subprocess.call('test.bat')
# subprocess.call('start.bat')

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
# folder_name = createDirectory
if exists(workspace + '.bat'):
  print("")
  # run associated .bat program to open all files
  #f = open(workspace + '.bat')
  #f.close
else:
  print("\nNo workspace named '" + workspace + "' is available")
  # prompt user again

# subprocess.call(["src\createDir.bat", workspace])