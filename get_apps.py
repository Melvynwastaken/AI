import subprocess

applications = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "paint": "mspaint.exe",
    "discord": "enter ur path here bozo",
    "spotify": "enter spotify path here"
}

def open_application(app_name):
    app_name = app_name.lower()
    
    if app_name in applications:
        try:
            subprocess.Popen(applications[app_name])
            return f"Opening {app_name}..."
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"
    else:
        return f"{app_name} not found."

if __name__ == "__main__":
    user_input = input("Enter the name of the application to open: ")
    print(open_application(user_input))
