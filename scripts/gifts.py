#!/bin/python3
"""VK script for parsing user gifts"""
import argparse
import getpass
import os
import time

from progress.bar import IncrementalBar
import vk_api


# Parser
PARSER = argparse.ArgumentParser(description="Parse user gifts")


# add python3 gifts.py [user_id_1] [user_id_2]
PARSER.add_argument("users",
                    nargs="*",
                    type=int,
                    help="python3 gifts.py [user_id_1] [user_id_2] [...]")


# add python3 gifts.py -m [min]
PARSER.add_argument("-m",
                    "--min",
                    type=int,
                    dest="min",
                    default=0,
                    help="python3 gifts.py -x [max]")


args = PARSER.parse_args()


class Colors():
    """Store colors and have functions for coloring"""
    HEADER = '\033[95m'
    MAINCOLOR = '\033[33m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


    def color_string(string: str):
        """

        color_string(string: str) -> str

        Return colored string
        """
        new_string = f"{Colors.MAINCOLOR}{Colors.BOLD}{string}{Colors.ENDC}"
        return new_string


    def nice_output(output: str):
        """
        nice_output(output: str) -> None
            print(output) with coloring
        """
        new_output = f"{Colors.MAINCOLOR}{Colors.BOLD}{output}{Colors.ENDC}"
        print(new_output)


    def nice_output_with_content(output: str, content):
        """
        nice_output_with_content(output: str, content) -> None
            print(output, content) with colored output
        """
        new_output = f"{Colors.MAINCOLOR}{Colors.BOLD}\t{output}\t{Colors.ENDC}"
        print(new_output, content)


def authorize():
    """
    authorize() -> vk_api.vk_api.VkApiMethod

    Get login and password.
    Authorize to vk.com.
    Return api.
    """
    try:
        login = input(Colors.color_string("[?] LOGIN: ")).strip()
        passwd = getpass.getpass(Colors.color_string("[?] PASSWORD: "))

        api = vk_api.VkApi(login=login,
                           password=passwd,
                           session=None)
        api.auth()
        api = api.get_api()
        return api

    except vk_api.BadPassword:
        print("[!] Bad password")


def delete_vk_config():
    """
    delete_vk_config() -> None

    Check if vk_config.v2.json exists
                            True:
        Delete it
                            False:
        Pass
    """
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")
    os.walk("..")
    if os.path.exists("vk_config.v2.json"):
        os.system("rm vk_config.v2.json")


def get_gifts(account: vk_api.vk_api.VkApiMethod, user: int):
    """
    get_gifts(account: vk_api.vk_api.VkApiMethod, user: int) -> None

    Get and parse args:user gifts. Print statistic.
    """
    print()
    gifts_list = account.gifts.get(user_id=user)
    account_info = account.users.get(user_ids=user)

    count = len(gifts_list.get("items"))

    # Create status bar
    bar_name = str(
        account_info[0].get("first_name") + " " + \
                        account_info[0].get("last_name")
    )

    statusbar = IncrementalBar(
        Colors.color_string(bar_name),
        max = count
    )

    usrs = []
    for i in gifts_list.get("items"):
        if not i.get("from_id") in usrs:
            usrs.append(i.get("from_id"))
        statusbar.next()
        time.sleep(0.005)
    statusbar.finish()
    print()

    res = []
    for usr in usrs:
        tmp = 0
        for i in gifts_list.get("items"):
            if i.get("from_id") == usr:
                tmp += 1

        res.append([usr, tmp])

    res.sort(key=lambda k: k[1])

    needed_users = reversed([r for r in res if r[1] >= args.min])

    groups_gifts = 0
    users_gifts = 0
    unidentified = 0

    for usr in needed_users:
        public_url = "https://vk.com/public"
        user_url = "https://vk.com/id"
        if usr[0] < 0:
            usr_id = str(abs(usr[0]))
            url = f"{public_url}{usr_id}"
            Colors.nice_output_with_content(url, usr[1])
            groups_gifts += usr[1]

        elif usr[0] > 0:
            usr_id = str(abs(usr[0]))
            url = f"{user_url}{usr_id}"
            Colors.nice_output_with_content(url, usr[1])
            users_gifts += usr[1]

    unidentified = count - (groups_gifts + users_gifts)

    print()

    Colors.nice_output_with_content(
        "Count:                  ",
        count
    )

    Colors.nice_output_with_content(
        "Gifts from groups:      ",
        groups_gifts
    )

    Colors.nice_output_with_content(
        "Gifts from users:       ",
        users_gifts
    )

    Colors.nice_output_with_content(
        "Unidentified gifts:     ",
        unidentified
    )



def main():
    """ MAIN FUNCTION """
    BANNER = Colors.color_string(r"""
        .__  _____  __
   ____ |__|/ ____\/  |_  ______
  / ___\|  \   __\\   __\/  ___/
 / /_/  >  ||  |   |  |  \___ \
 \___  /|__||__|   |__| /____  >
/_____/                      \/

""")
    print(BANNER)
    account = authorize()

    for usr in args.users:
        get_gifts(account, usr)

    print()

    print("Done")

if __name__ == "__main__":
    main()
    delete_vk_config()
