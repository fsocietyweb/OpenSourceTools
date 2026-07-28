import platform
import os
import uuid
import shutil

class Tool:
    def __init__(self, name):
        self.name = name
    
    def run(self):
        pass


class SystemInfo(Tool):
    def __init__(self):
        super().__init__("SystemInfo")


    def run(self):
        print("=== System Info ===")

        print("CPU:", self.get_cpu())
        self.get_os()


    def get_cpu(self):
        with open("/proc/cpuinfo") as file:
            for line in file:
                if "model name" in line:
                    return line.split(":")[1].strip()

        return "Unknown"

    def get_os(self):
        info = platform.freedesktop_os_release()
        kernel = platform.release()
        architechture = platform.machine()
        hostname = platform.node()

        print("Linux Distro:", info["NAME"])
        print("Kernel:", kernel)
        print("Architechture:", architechture)
        print("Hostname:", hostname)


class shutdown(Tool):
    def __init__(self):
        super().__init__("Shutdown")
    
    def run(self):
        choice = input("Are you sure you want to shutdown? y/n: ")

        if choice == "y":
            os.system("shutdown now")
        else:
            return

class restart(Tool):
    def __init__(self):
        super().__init__("Restart")
    
    def run(self):
        choice = input("Are you sure you want to restart? y/n: ")

        if choice == "y":
            os.system("reboot now")
        else:
            return

class Run_Discord(Tool):
    def __init__(self):
        super().__init__("Run Discord")
    
    def run(self):
        os.system("discord")
        print("Discord executed")


class Generate_UUID(Tool):
    def __init__(self):
        super().__init__("Generate UUID")
    
    def run(self):
        genuuid = uuid.uuid4()

        print("Your generated UUID: ", genuuid)


class Install_Programm(Tool):
    def __init__(self):
        super().__init__("Install Programm")
    
    def run(self):
        programm = input("Programm you want to install: ")

        if shutil.which("pacman"):
            os.system(f"sudo pacman -S {programm}")
            print(f"{programm} succesfully installed")
        
        elif shutil.which("apt"):
            os.system(f"sudo apt install {programm}")
            print(f"{programm} succesfully installed")
        
        elif shutil.which("dnf"):
            os.system(f"sudo dnf install {programm}")
            print(f"{programm} succesfully installed")
        
        elif shutil.which("zypper"):
            os.system(f"sudo zypper install {programm}")
            print(f"{programm} succesfully installed")
        
        elif shutil.which("apk"):
            os.system(f"sudo apk add {programm}")
            print(f"{programm} succesfully installed")
        
        else:
            print("Your package manager is not supported")


class Update_System(Tool):
    def __init__(self):
        super().__init__("Update System")
    
    def run(self):
        distro = platform.freedesktop_os_release()

        if shutil.which("apt"):
            os.system("sudo apt update && sudo apt upgrade")
            print(f"Dein System:{distro["ID"]} wurde geupdatet")
        
        elif shutil.which("dnf"):
            os.system("sudo dnf upgrade --refresh")
            print(f"Dein System:{distro["ID"]} wurde geupdatet")
        
        elif shutil.which("pacman"):
            os.system("sudo pacman -Syu")
            print(f"Dein System:{distro["ID"]} wurde geupdatet")

        elif shutil.which("zypper"):
            os.system("sudo zypper update")
            print(f"Dein System:{distro["ID"]} wurde geupdatet")

        elif shutil.which("apk"):
            os.system("sudo apk update && sudo apk upgrade")
            print(f"Dein System:{distro["ID"]} wurde geupdatet")

        else:
            print("Dein Package manager wird nicht unterstützt")    


while True:
    print("=== Lennys Multitool ===")
    print("1. System Info")
    print("2. Shutdown")
    print("3. Restart")
    print("4. Discord")
    print("5. Genrate UUID")
    print("6. Install a Programm")
    print("7. Update your System")
    print("8. Exit")

    try:
        choice = int(input("> "))
    except ValueError:
        print("Please enter a number")
        continue

    if choice == 1:
        tool = SystemInfo()
        tool.run()
    
    elif choice == 2:
        tool = shutdown()
        tool.run()
    
    elif choice == 3:
        tool = restart()
        tool.run()
    
    elif choice == 4:
        tool = Run_Discord()
        tool.run()
    
    elif choice == 5:
        tool = Generate_UUID()
        tool.run()
    
    elif choice == 6:
        tool = Install_Programm()
        tool.run()
    
    elif choice == 7:
        tool = Update_System()
        tool.run()
    
    else:
        exit()
