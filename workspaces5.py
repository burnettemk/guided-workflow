import os
import json
import subprocess
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox, filedialog, simpledialog


class WorkspaceManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workspace Manager")
        self.root.geometry("1200x800")

        # Initialize workspace storage
        self.workspaces_file = "workspaces.json"
        self.workspaces = self.load_workspaces()

        # Define data path where workspaces and related files are stored
        self.data_path = "data"
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        
        # Layout
        self.create_layout()

        # Define class variables for the workspace formats
        self.paths_var = "paths"
        self.dir_var = "working_dir"

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
            self.sidebar, text="Edit Workspace", command=self.edit_workspace
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
            json.dump(self.workspaces, file, indent=4) # No data is being dumped because we're not using a json object

    def populate_workspaces(self):
        """Populate the listbox with workspace names."""
        self.workspace_listbox.delete(0, tk.END)
        for name in self.workspaces:
            self.workspace_listbox.insert(tk.END, name)

    def create_workspace(self):
        """Create a new workspace."""
        workspace_name = filedialog.asksaveasfilename(
            title="Enter a name for the workspace:",
            defaultextension=".workspace",
            filetypes=[("Workspace Files", "*.workspace")]
        )

        if not workspace_name:
            return

        # Check the last part of the pathname. Use as workspace name if it doesn't exist
        workspace_name = os.path.basename(workspace_name)
        if workspace_name in self.workspaces:
            messagebox.showerror("Error", "Workspace name already exists.")
            return

        self.workspaces[workspace_name] = {"applications": []}

        working_dir = filedialog.askdirectory(
                title="Select a working directory (or create one):"
            )
        if not working_dir:
            # Offer the option to create a directory
            if messagebox.askyesno("No Directory", "Would you like to create a new directory?"):
                new_dir = filedialog.asksaveasfilename(
                    title="Enter name for new directory:"
                )
                os.makedirs(new_dir, exist_ok=True)
                working_dir = new_dir
        
        self.workspaces[workspace_name][self.dir_var] = working_dir or None
        self.workspaces[workspace_name]["applications"] = {self.paths_var: []}
        
        while True:
            app_path = filedialog.askopenfilename(
                title="Select an application to add to the workspace:"
            )
            if not app_path:
                break

            self.workspaces[workspace_name]["applications"][self.paths_var].append(app_path)

            if not messagebox.askyesno("Add More?", "Would you like to add another application?"):
                break

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
        self.current_workspace = workspace_name

        # Check for an empty application list
        apps = self.workspaces[workspace_name]["applications"][self.paths_var]
        if not apps:
            messagebox.showinfo("Empty Workspace", "This workspace has no applications.")
            return

        working_dir = self.workspaces[workspace_name][self.dir_var]
        os.chdir(working_dir)

        # Open each app
        for app in apps:
            self.open_application(app)

        messagebox.showinfo("Workspace Started", f"Workspace '{workspace_name}' started!")

    def display_workspace_apps(self, event):
        """Display applications in the selected workspace."""
        selected_index = self.workspace_listbox.curselection()
        if not selected_index:
            return

        workspace_name = self.workspace_listbox.get(selected_index)
        # apps = self.workspaces.get(workspace_name, {}).get("applications", [])
        apps = self.workspaces[workspace_name]["applications"][self.paths_var]

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
        
        print(f"Delete {workspace_name}")

    def edit_workspace(self):
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
        
        print(f"Edit {workspace_name}")


if __name__ == "__main__":
    #root = tk.Tk()
    root = ttk.Window(themename="darkly")
    
    # Load the image
    icon = tk.PhotoImage(file="test.png")

    # Set the icon
    root.iconphoto(False, icon)

    app = WorkspaceManagerApp(root)
    root.mainloop()
