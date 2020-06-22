import argparse
import getpass
import os

import vk_api

PARSER = argparse.ArgumentParser(description="Check if a person has a current account in bookmarks")
PARSER.add_argument("-u", "--user", action="store", type=int, dest="user", help="python3 checkfave.py -u [user_id]")
args = PARSER.parse_args()

BANNER = """
         ___| |__   ___  ___| | __ / __\_ ___   _____
        / __| '_ \ / _ \/ __| |/ // _\/ _` \ \ / / _ \\
       | (__| | | |  __/ (__|   </ / | (_| |\ V /  __/
        \___|_| |_|\___|\___|_|\_\/   \__,_| \_/ \___|
"""

def authorize():
    try:
        login = input("[?] LOGIN: ")
        passwd = getpass.getpass("[?] PASSWORD: ")
        api = vk_api.VkApi(login=login, password=passwd, session=None)
        api.auth()
        api = api.get_api()
        return api


def delete_vk_config():
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")
    os.walk("..")
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")
    

def main():
    print(BANNER)
    account = authorize()
    info = account.users.get(user_ids=args.user, fields="is_favorite")
    if info[0].get("is_favorite") == 1:
        print("""====================\n""", "True")
    else:
        print("""====================\n""", "False")


if __name__ == "__main__":
    main()
    delete_vk_config()
