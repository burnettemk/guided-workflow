# guided-workflow

my own personal system for focus and productivity

The main purpose of the system is to increase focus while I work on various projects or other artistic endeavors.

## The program life cycle

The first step in the application's life cycle will be to open up a window or command prompt prompting me as the user to
choose which workspace I would like to setup right now or exit out the program if I simply wish to do something else.

Both the command prompt or a window would display all currently saved workspaces and prompt me to choose

Ideally, I would like for the program to run on startup and get me straight to focusing.

Additionally, I want to also have the option to setup a new workspace.

### New workspaces

Upon selecting to use a new workspace, I should be greeted with a clear screen with new prompts that ask me to put input the
programs that I'd like to be part of the new workspace

The name of the programs will be added to a file or directory for a batch script to read through later

The new workspace can be setup to start immediately upon creation or simply saved to the workspaces file or directory

### Choosing a workspace

Once a workspace is chosen, we run some batch scripts that looks through the listed applications it needs to open and starts those
programs. Once finished, I just get to work. The program should take note of the new processes that it created for when we
wish to kill the programs.

### Terminating or switching workspaces

Whenever we want to stop working or switch to a new workspace, the current workspace must be closed to make room for the
new one. We will simply kill all open tasks and wait for them to be removed from the tasklist before starting up the
new workspace.

If needed, we can wait some time for a startup background process to finish or wait some time before starting
another program. Although for non intensive programs, I doubt it will be a big deal if programs start at the same time.

Right now, I will just design this project to cater mostly to programs that don't involve long startups or are intensive
cpu intensive. So basically anything that doesn't have to do with video processing or 3d rendering or an intensive video game.

## Additional details

I would like for each workspace to have their own directory so I can work from it and further reduce distractions, but this is
an optional feature.

I would also like to change the color of the command prompt depending on the workspace and this is also the only reason why
I'm using batch scripting over powershell for right now. But I won't leave out powershell.
