import os
import json
import subprocess
#import json
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox, filedialog, simpledialog
#from processmonitor import ApplicationMonitor
import processmonitor


class WorkspaceManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workspace Manager")
        self.root.geometry("1200x800")

        # Define data path where workspaces and related files are stored
        self.data_path = "data"
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # Initialize workspace storage
        self.workspaces_file = os.path.join(self.data_path, "workspaces.json")
        self.workspaces = self.load_workspaces()
        
        # Layout
        self.create_layout()

        # Define class variables for the workspace formats
        self.apps_var = "applications"
        self.paths_var = "paths"
        self.dir_var = "working_dir"
        self.playlist_var = "playlist"

        # Set persistent variable
        self.current_workspace = ""

    def create_layout(self):
        # Sidebar for buttons
        self.sidebar = tk.Frame(self.root, width=150, bg="lightgray")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.padding_box = tk.Label(self.sidebar, text=" ")
        self.padding_box.pack(pady=15)

        # Create Button
        self.button_create = tk.Button(
            self.sidebar, text="Create Workspace", command=self.create_workspace
        )
        self.button_create.pack(fill=tk.X, padx=5, pady=5)

        # Start Button
        self.button_start = tk.Button(
            self.sidebar, text="Start Workspace", command=self.start_selected_workspace
        )
        self.button_start.pack(fill=tk.X, padx=5, pady=5)

        # Edit Button
        self.button_edit = tk.Button(
            self.sidebar, text="Edit Workspace", command=self.edit_selected_workspace
        )
        self.button_edit.pack(fill=tk.X, padx=5, pady=5)

        # Delete Button
        self.button_delete = tk.Button(
            self.sidebar, text="Delete Workspace", command=self.delete_workspace
        )
        self.button_delete.pack(fill=tk.X, padx=5, pady=5)

        # Quit Button
        self.button_quit = tk.Button(
            self.sidebar, text="Quit", command=self.root.quit
        )
        self.button_quit.pack(fill=tk.X, padx=5, pady=5)

        # Main display for workspace list
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.label_workspaces = tk.Label(self.main_frame, text="Available Workspaces")
        self.label_workspaces.pack(pady=10)

        self.workspace_listbox = tk.Listbox(self.main_frame)
        self.workspace_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.workspace_listbox.bind("<<ListboxSelect>>", self.display_workspace_apps)
        self.populate_workspaces()

        # Display for currently opened workspace
        self.current_label = tk.Label(self.main_frame, text="")
        self.current_label.pack(fill=tk.BOTH)

        # Side panel for workspace applications
        self.apps_panel = tk.Frame(self.root, width=250, bg="white")
        self.apps_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.label_apps = tk.Label(self.apps_panel, text="Applications in Workspace")
        self.label_apps.pack(pady=10)

        self.apps_listbox = tk.Listbox(self.apps_panel)
        self.apps_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_workspaces(self):
        """Load workspace data from JSON."""
        if os.path.exists(self.workspaces_file):
            with open(self.workspaces_file, "r") as file:
                return json.load(file)
        return {}

    def save_workspaces(self):
        """Save workspace data to JSON."""
        with open(self.workspaces_file, "w") as file:
            json.dump(self.workspaces, file, indent=4)

    def populate_workspaces(self):
        """Populate the listbox with workspace names."""
        self.workspace_listbox.delete(0, tk.END)
        for name in self.workspaces:
            self.workspace_listbox.insert(tk.END, name)

    def create_workspace(self):
        """Create a new workspace."""
        workspace_name = simpledialog.askstring(title="Enter name for the workspace",
                                                 prompt="Enter a name for the workspace:")

        if not workspace_name:
            return

        # Check the last part of the pathname. Use as workspace name if it doesn't exist
        workspace_name = os.path.basename(workspace_name)
        if workspace_name in self.workspaces:
            messagebox.showerror("Error", "Workspace name already exists.")
            return

        self.workspaces[workspace_name] = {self.apps_var: []}

        working_dir = filedialog.askdirectory(
                title="Select a working directory (or create one):"
            )
        if not working_dir:
            # Offer the option to create a directory
            if messagebox.askyesno("No Directory", "Would you like to create a new directory?"):
                new_dir = filedialog.asksaveasfilename(
                    title="Enter name for new directory:"
                )
                if new_dir:
                    os.makedirs(new_dir, exist_ok=True)
                    working_dir = new_dir
        
        self.workspaces[workspace_name][self.dir_var] = working_dir or None
        self.workspaces[workspace_name][self.apps_var] = {self.paths_var: []}
        self.workspaces[workspace_name][self.playlist_var] = ""
        
        while True:
            app_path = filedialog.askopenfilename(
                title="Select an application to add to the workspace:"
            )
            if not app_path:
                break

            self.workspaces[workspace_name][self.apps_var][self.paths_var].append(app_path)

            if not messagebox.askyesno("Add More?", "Would you like to add another application?"):
                break
        
        if messagebox.askyesno("Add music playlist?", "Would you like to set a music playlist?"):
            pl_file = filedialog.askopenfilename(
                title="Select a playlist file to add to the workspace:"
            )
            self.workspaces[workspace_name][self.playlist_var] = pl_file

        self.save_workspaces()
        self.populate_workspaces()
        messagebox.showinfo("Workspace Created", f"Workspace '{workspace_name}' created!")

    def start_selected_workspace(self):
        """Start the selected workspace."""

        # Check to see if a workspace is selected
        selected_index = self.workspace_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a workspace.")
            return

        # Look for workspace in JSON dictionary
        workspace_name = self.workspace_listbox.get(selected_index)
        if workspace_name not in self.workspaces:
            messagebox.showerror("Error", f"Workspace '{workspace_name}' not found.")
            return

        # Set current workspace
        self.current_label["text"] = workspace_name
            # Create the process monitor
        app_monitor = processmonitor.ApplicationMonitor(self.workspaces[workspace_name][self.apps_var])
        self.start_monitoring(app_monitor)
            # Get allowed apps
        print(app_monitor.get_allowed_apps())

        # Check for an empty application list
        apps = self.workspaces[workspace_name][self.apps_var][self.paths_var]
        if not apps:
            messagebox.showinfo("Empty Workspace", "This workspace has no applications.")
            return

        working_dir = self.workspaces[workspace_name][self.dir_var]
        if working_dir:
            os.chdir(working_dir)

        # Open each app
        for app in apps:
            self.open_application(app)
        
        playlist = self.workspaces[workspace_name][self.playlist_var]
        if playlist:
            self.start_playlist(playlist)

        messagebox.showinfo("Workspace Started", f"Workspace '{workspace_name}' started!")

    def display_workspace_apps(self, event):
        """Display applications in the selected workspace."""
        selected_index = self.workspace_listbox.curselection()
        if not selected_index:
            return

        workspace_name = self.workspace_listbox.get(selected_index)
        # apps = self.workspaces.get(workspace_name, {}).get(self.apps_var, [])
        apps = self.workspaces[workspace_name][self.apps_var][self.paths_var]

        self.apps_listbox.delete(0, tk.END)
        for app in apps:
            path_list = app.split("/")
            self.apps_listbox.insert(tk.END, path_list[-1][0:-4])

    def open_application(self, app_path, working_dir=None):
        """Launch an application."""
        try:
            if os.path.exists(app_path):
                #subprocess.Popen([app_path], cwd=working_dir or None, shell=True)
                subprocess.Popen([app_path], shell=True)
                print(f"Started: {app_path}")
            else:
                print(f"Application not found: {app_path}")
        except Exception as e:
            print(f"Failed to start application: {e}")

    def start_playlist(self, playlist):
        """Launch an application."""
        try:
            # Command to start VLC with the playlist file
            command = ["start", "vlc", playlist]

            # Execute the command using Popen
            process = subprocess.Popen(command, shell=True)
        except Exception as e:
            print(f"Failed to start application: {e}")

    def delete_workspace(self):
        # Check to see if a workspace is selected
        selected_index = self.workspace_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a workspace.")
            return
        
        # Look for workspace in JSON dictionary
        workspace_name = self.workspace_listbox.get(selected_index)
        if workspace_name not in self.workspaces:
            messagebox.showerror("Error", f"Workspace '{workspace_name}' not found.")
            return
        
        if messagebox.askyesnocancel("Confirm deletion", f"Are you sure you want to delete '{workspace_name}'?"):
            self.workspaces.pop(workspace_name)
            self.save_workspaces()
            self.populate_workspaces()
            messagebox.showinfo("Workspace Deleted", f"Workspace '{workspace_name}' was deleted!")
        else:
            return
    
    def edit_selected_workspace(self):
        # Check to see if a workspace is selected
        selected_index = self.workspace_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a workspace to edit.")
            return

        workspace_name = self.workspace_listbox.get(selected_index[0])
        workspace_data = self.workspaces[workspace_name]
        old_workspace_name = workspace_name

        if not workspace_data:
            messagebox.showerror("Error", f"No data found for {workspace_name}.")
            return

        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Workspace: {workspace_name}")
        edit_window.grab_set()  # Focus on this window

        # Change name
        tk.Label(edit_window, text="Workspace Name:").pack(anchor="w")
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, old_workspace_name[:-10])  # Remove .workspace for display
        name_entry.pack(expand=True, fill=tk.X, padx=5, pady=(5, 10))

        # Edit working directory
        tk.Label(edit_window, text="Working Directory:").pack(anchor="w")
        working_dir_var = tk.StringVar(value=workspace_data[self.dir_var])
        working_dir_entry = tk.Entry(edit_window, textvariable=working_dir_var, width=50)
        working_dir_entry.pack(expand=True, fill=tk.X, padx=5, pady=5)

        def select_working_dir():
            selected_dir = filedialog.askdirectory(title="Select New Working Directory")
            if selected_dir:
                working_dir_var.set(selected_dir)
            
            # Bring the pop-up window back to focus
            edit_window.deiconify()
            edit_window.lift()

        tk.Button(edit_window, text="Change Directory", command=select_working_dir).pack(anchor="w", padx=5, pady=(0, 15))

        # Add/Change playlist
        tk.Label(edit_window, text="Playlist:").pack(anchor="w")
        playlist_var = tk.StringVar(value=workspace_data[self.playlist_var])
        if not playlist_var.get(): playlist_var.set("No playlist")
        playlist_entry = tk.Label(edit_window, textvariable=playlist_var)
        playlist_entry.pack(expand=True, padx=5, pady=(0, 5), anchor="w")

        def select_playlist():
            selected_playlist = filedialog.askopenfilename(title="Select the playlist that you'd like to add to the workspace")
            if selected_playlist:
                playlist_var.set(selected_playlist)
            
            edit_window.deiconify()
            edit_window.lift()
        
        tk.Button(edit_window, text="Select Playlist", command=select_playlist).pack(anchor="w", padx=5, pady=(0, 15))

        # Edit application paths
        tk.Label(edit_window, text="Applications:").pack(anchor="w", pady=(0, 5))
        apps_listbox = tk.Listbox(edit_window, height=10)
        apps_listbox.pack(fill=tk.BOTH, padx=5, pady=(0, 5))

        for path in workspace_data["applications"]["paths"]:
            apps_listbox.insert(tk.END, path)

        def add_application():
            file_path = filedialog.askopenfilename(title="Select Application")
            if file_path:
                apps_listbox.insert(tk.END, file_path)
            
            # Bring the pop-up window back to focus
            edit_window.deiconify()
            edit_window.lift()

        def remove_selected_application():
            selected = apps_listbox.curselection()
            for index in selected[::-1]:
                apps_listbox.delete(index)
            
            self.display_workspace_apps(None)
        
        def change_workspace_name(data, old_name, new_name):
            """
            Change a key in the dictionary while preserving the order of keys.

            Parameters:
            - d (dict): The original dictionary.
            - old_key: The key to be replaced.
            - new_key: The new key to replace the old one.

            Returns:
            - dict: A new dictionary with the updated key.
            """
            if old_name not in data:
                raise KeyError(f"The key '{old_name}' does not exist in the dictionary.")
            if new_name in data:
                raise KeyError(f"The key '{new_name}' already exists in the dictionary.")
            
            return {new_name if key == old_name else key: value for key, value in data.items()}

        app_buttons_frame = tk.Frame(edit_window)
        app_buttons_frame.pack(fill=tk.X)

        tk.Button(app_buttons_frame, text="Add Application", command=add_application).pack(side=tk.LEFT, padx=5)
        tk.Button(app_buttons_frame, text="Remove Selected", command=remove_selected_application).pack(side=tk.LEFT)

        def save_changes():
            # REMINDER: The local variable workspace_name from edit_workspace() is not the same variable that is used here somehow 

            new_workspace_name = name_entry.get().strip()
            if not new_workspace_name:
                # keep old name if new one is not defined
                workspace_name = old_workspace_name
            else:
                # Rename property and update dictionary key
                self.workspaces = change_workspace_name(self.workspaces, old_workspace_name, new_workspace_name)
                workspace_name = new_workspace_name

            new_working_dir = working_dir_var.get()
            new_apps = [apps_listbox.get(i) for i in range(apps_listbox.size())]

            self.workspaces[workspace_name] = {
                "applications": {"paths": new_apps},
                "working_dir": new_working_dir,
                self.playlist_var: playlist_var.get()
            }
            self.save_workspaces()
            self.populate_workspaces()

            # Set the selection programmatically
            index = self.workspace_listbox.get(0, tk.END).index(workspace_name)
            self.workspace_listbox.selection_clear(0, tk.END)
            self.workspace_listbox.selection_set(index)
            self.workspace_listbox.activate(index)

            self.display_workspace_apps(None)
            edit_window.destroy()

        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)

        # Focus the pop-up window
        edit_window.lift()

    def start_monitoring(self, app_monitor):
        def monitor():
            monitor = processmonitor.ApplicationMonitor(app_monitor.get_allowed_apps())
            # Get currently open apps
            outside_apps = monitor.check_for_outside_apps()
            if outside_apps:
                warn_about_outside_apps(outside_apps)
            # Call monitor again after 5000ms (5 seconds)
            self.root.after(5000, monitor)

        monitor()


def warn_about_outside_apps(outside_apps):
    if outside_apps:
        message = "The following applications are running but are not part of the current workspace:\n\n"
        message += "\n".join(outside_apps)
        messagebox.showwarning("Outside Applications Detected", message)



if __name__ == "__main__":
    #root = tk.Tk()
    root = ttk.Window(themename="cyborg")
    
    # Load the image
    icon = tk.PhotoImage(file="test.png")

    # Set the icon
    root.iconphoto(False, icon)

    # Create Workspace Manager from tkinter window
    app = WorkspaceManagerApp(root)
    
    root.mainloop()
