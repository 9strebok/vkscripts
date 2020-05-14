import argparse
import getpass
import os

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
    login = input("[?] LOGIN: ")
    passwd = getpass.getpass("[?] PASSWORD: ")
    api = vk_api.VkApi(login=login, password=passwd, session=None)
    api.auth()
    api = api.get_api()
    return api


def delete_vk_config():
    if not os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")

def main():
    print(BANNER)
    account = authorize()
    try:
        gifts_list = account.gifts.get(user_id=args.user)


        usrs = []
        for i in gifts_list["items"]:
            if not i["from_id"] in usrs:
                usrs.append(i["from_id"])

        res = []
        for usr in usrs:
            tmp = 0
            for i in gifts_list["items"]:
                if i["from_id"] == usr:
                    tmp += 1
            if usr < 0:
                usr = abs(usr)
                print("vk.com/public"+str(usr), tmp)
            elif usr == 0:
                pass
            else:
                print("vk.com/id"+str(usr), tmp)
        print()

        groups_gifts = 0
        users_gifts = 0
        for i in gifts_list["items"]:
            if i["from_id"] < 0:
                groups_gifts += 1
            elif i["from_id"] > 0:
                users_gifts += 1
        unidentified = gifts_list["count"] - (groups_gifts + users_gifts)
        print("Count:", gifts_list["count"])
        print("Gifts from groups:", groups_gifts)
        print("Gifts from users:", users_gifts)
        print("Unidentified gifts:", unidentified)
    except:
        print("Error, maybe you can't to get gifts list")


if __name__ == "__main__":
    main()
    delete_vk_config()