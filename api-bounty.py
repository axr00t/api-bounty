import subprocess
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    banner = """
==================================================================================
               .--.
              /.-. '----------.
              \'-' .--"--""-"-'
               '--'  By axroot
  ____  ____ ____      ____    ___   __ __  ____   ______  __ __ 
 /    ||    \    |    |    \  /   \ |  |  ||    \ |      ||  |  |
|  o  ||  o  )  |     |  o  )|     ||  |  ||  _  ||      ||  |  |
|     ||   _/|  |     |     ||  O  ||  |  ||  |  ||_|  |_||  ~  |
|  _  ||  |  |  |     |  O  ||     ||  :  ||  |  |  |  |  |___, |
|  |  ||  |  |  |     |     ||     ||     ||  |  |  |  |  |     |
|__|__||__| |____|    |_____| \___/  \__,_||__|__|  |__|  |____/ 
                                                                
Use the Keyhack repository to validate the keys found \n(https://github.com/streaak/keyhacks)
==================================================================================    
    """
    print(banner)

def show_menu():
    print("Please choose an option:")
    print("[1] - Check Requirements")
    print("[2] - Start Search")
    print("[3] - About The Tool")
    print("[0] - Exit")

def check_requirements():
    print("\nChecking Requirements...\n")
    requirements = ["subfinder", "httpx-toolkit", "katana"]
    for req in requirements:
        try:
            result = subprocess.run(f"which {req}", shell=True, check=True, text=True, capture_output=True)
            print(f"{req} is installed: {result.stdout.strip()} ✅")
        except subprocess.CalledProcessError:
            print(f"{req} is not installed. ❌")
    print("\nImportant: You need the secretfinder tool (https://github.com/m4ll0k/SecretFinder), clone the repository and insert the installation path in the api-bounty tool code.")

def start_search():
    print("\nStarting the Search...\n")
    domain = input("Please enter the domain to search (example.com): ")
    
    commands = [
        f"subfinder -d {domain} -all -recursive > subdomains.txt",
        "cat subdomains.txt | httpx-toolkit -ports 8080,80,8000,8888 -mc 200,403,400,500 -o subdomains-alive.txt",
        "katana -list subdomains-alive.txt -jc -d 4 -o crawl.txt",
        "cat crawl.txt Z grep -E '\\.js$|\\.json' | sort -u > jsfiles.txt",
        "cat jsfiles.txt | while read url; do python3 /your-path/secretfinder/SecretFinder.py -i $url -o cli; done | tee -a secrets.txt",
        "cat secrets.txt | grep 'Heroku' | sort -u > HerokuAPI.txt",
        "cat secrets.txt | grep 'Twilio' | sort -u > TwilioAPI.txt",
        "cat secrets.txt | grep 'google' | sort -u > GoogleAPI.txt",
        "cat secrets.txt | grep 'aws' | sort -u > awsAPI.txt",
        "cat secrets.txt | grep -E 'Stripe|Paypal|auth' | sort -u > OtherAPI.txt"
    ]

    for command in commands:
        clear_screen()
        display_banner()
        print(f"\n[***] Executing command: {command}\n")
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            if result.stdout:
                print(f"Output:\n{result.stdout}")
            if result.stderr:
                print(f"[X] Errors:\n{result.stderr}")
            print(f"[✅]Command completed successfully: {command}\n")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the command ❌:\n{e.stderr}")
            break

def about():
    print("The API Bounty tool automates the process of searching for API Keys in Bug Bounty programs, \nperforming a wide variety of search tasks.")

def main():
    while True:
        clear_screen()
        display_banner()
        show_menu()
        choice = input("\nEnter your choice -> ")
        
        clear_screen()
        display_banner()

        if choice == '1':
            check_requirements()
        elif choice == '2':
            start_search()
        elif choice == '3':
            about()
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
