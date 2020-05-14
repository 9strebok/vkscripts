import os

def main():
    if os.name == "nt":
        os.system("pip install vk_api progress")
    else:
        os.system("pip3 install vk_api progress")

if __name__ == "__main__":
    main()
