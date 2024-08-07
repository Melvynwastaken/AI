import subprocess
import webbrowser

# you can add more here just add the refered name and then the execution path
applications = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "paint": "mspaint.exe",
    "excel":"C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
    "jupyter": "jupyter lab",
    "powerbi": "PBIDesktopStore.exe",
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
    
# same goes for websites but in this case use url
websites = {"wiki": "https://en.wikipedia.org/wiki/Main_Page",
            "youtube":"https://www.youtube.com/",
            "github":"https://github.com/Melvynwastaken",
            "wayback":"https://wayback-api.archive.org/",
            "gpt": "https://chat.openai.com/",
            "steam": "https://store.steampowered.com/",
            "discord":"https://discord.com/channels/@me",
            "spotify":"https://open.spotify.com",
            
}

def open_web(web_name):
    web_name = web_name.lower()
    
    if web_name in websites:
        try:
            webbrowser.open(websites[web_name])
            return f"Opening {web_name}..."
        except Exception as e:
            return f"Failed to open {web_name}: {str(e)}"
    else:
        return f"{web_name} not found."

if __name__ == "__main__":
    user_input = input("Enter the name of the application or website to open: ")
    if user_input in applications:
        print(open_application(user_input))
    else:
        print(open_web(user_input))
