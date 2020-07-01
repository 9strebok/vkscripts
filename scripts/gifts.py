import argparse
import getpass
import os
import time

from progress.spinner import MoonSpinner
import vk_api

PARSER = argparse.ArgumentParser(description="Check if a person has a current account in bookmarks")
PARSER.add_argument("-u", "--user", action="store", type=int, dest="user", help="python3 gifts.py -u [user_id]")
args = PARSER.parse_args()

BANNER = """
        .__  _____  __
   ____ |__|/ ____\/  |_  ______
  / ___\|  \   __\\\\   __\/  ___/
 / /_/  >  ||  |   |  |  \___ \\
 \___  /|__||__|   |__| /____  >
/_____/                      \/

"""

def authorize():
    try:
        login = input("[?] LOGIN: ")
        try:
            passwd = getpass.getpass("[?] PASSWORD: ")
        except:
            print("[!] Error")
            passwd = getpass.getpass("[?] PASSWORD: ")
        api = vk_api.VkApi(login=login, password=passwd, session=None)
        api.auth()
        api = api.get_api()
        return api
    except vk_api.BadPassword as e:
        print("[!] Bad password")


def delete_vk_config():
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")
    os.walk("..")
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")


def main():
    print(BANNER)
    account = authorize()
    print()
    try:
        gifts_list = account.gifts.get(user_id=args.user)
        with MoonSpinner("Wait..") as bar:
            usrs = []
            for i in gifts_list.get("items"):
                time.sleep(0.01)
                if not i.get("from_id") in usrs:
                    usrs.append(i.get("from_id"))
                bar.next()
        print()

        res = []
        for usr in usrs:
            tmp = 0
            for i in gifts_list.get("items"):
                if i.get("from_id") == usr:
                    tmp += 1
            if usr < 0:
                usr = str(abs(usr))

                public = "https://vk.com/public"
                s = f"echo -e '\e]8;;{public}{usr}\\a{public}{usr}\e]8;;\\a\t' {tmp}"
                os.system(s)
            elif usr > 0:
                usr = str(usr)
                vkid = "https://vk.com/id"
                s = f"echo -e '\e]8;;{vkid}{usr}\\a{vkid}{usr}\e]8;;\\a\t' {tmp}"
                os.system(s)
        print()

        groups_gifts = 0
        users_gifts = 0
        for i in gifts_list.get("items"):
            if i.get("from_id") < 0:
                groups_gifts += 1
            elif i.get("from_id") > 0:
                users_gifts += 1
        unidentified = gifts_list.get("count") - (groups_gifts + users_gifts)
        print("Count:                  \t", gifts_list.get("count"))
        print("Gifts from groups:      \t", groups_gifts)
        print("Gifts from users:       \t", users_gifts)
        print("Unidentified gifts:     \t", unidentified)
        print()
    except:
        print("Error, maybe you can't to get gifts list")
        print()


if __name__ == "__main__":
    main()
    delete_vk_config()
