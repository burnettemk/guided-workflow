import psutil
import os
import tkinter as tk
from tkinter import messagebox

allowed = "allowed.txt"

class ApplicationMonitor:
    def __init__(self, allowed_paths):
        self.allowed_paths = set(allowed_paths)

    def get_running_applications(self):
        running_apps = set()
        for proc in psutil.process_iter(['pid', 'exe']):
            try:
                exe_path = proc.info['exe']
                if exe_path:  # Exclude processes without a valid executable
                    running_apps.add(exe_path)
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
        return running_apps

    def check_for_outside_apps(self):
        running_apps = self.get_running_applications()
        #print("ALLOWED APPS" + str(self.allowed_paths))
        outside_apps = running_apps - self.allowed_paths
        #print(outside_apps)
        return outside_apps
    
    def get_allowed_apps(self):
        """Get list of system processes and add to ALLOW list"""
        if os.path.exists(allowed):
            with open(allowed, "r") as file:
                return file.read()
        return {}
