# VKSCRIPTS

# Anchors
[TREE](#Tree)

[INSTALL](#INSTALL)

[SCRIPTS](#Scripts)

[HELP](#Help)

## Tree
~~~
.
├── README.md
├── requirements.txt
└── scripts
   ├── checkfave.py
   ├── gifts.py
   └── mergefriends.py
~~~
[BACK](#Anchors)

## INSTALL

### Linux
~~~bash
    git clone https://github.com/9strebok/vkscripts
    pip3 install -r requirements.txt
~~~

### Windows
~~~bash
    git clone https://github.com/9strebok/vkscripts
    pip install -r requirements.txt
~~~

[BACK](#Anchors)

## SCRIPTS

* ***checkfave.py*** **status: working** - *Check if a person has a current account in bookmarks.*

## USING
~~~
    python3 checkfave.py -u/--user [id]
~~~

* ***gifts.py*** **status: working** - *User gift parsing.*

## USING
~~~
    python3 gifts.py -u/--user [id]
~~~

* ***mergefriends.py*** **status: working** - *Makes mutual friends between two people*

## USING
~~~
    python3 gifts.py -u1/--user1 [id] -u2/--user2 [id]
~~~

[BACK](#Anchors)

---

## HELP

~~~
    python3 [script] -h/--help
~~~

### Template

~~~
    python3 checkfave.py -h
~~~

~~~
    usage: checkfave.py [-h] [-u USER]

    Check if a person has a current account in bookmarks

    optional arguments:
        -h, --help            show this help message and exit
        -u USER, --user USER  python3 checkfave.py -u [user_id]
~~~

[BACK](#Anchors)

---
