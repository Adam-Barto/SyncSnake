# coding: utf-8 
# Needs Python 3, dirsync
import getpass  # used to get username
import socket
import os
import fnmatch
import shutil

import time  # used to sleep the snake

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import dirsync
from dirsync import sync

REMOTE_SERVER = "smb://server-name"
SHARE_POINT_PATH = "/SyncTest"

busy = False  # if the code is busy with syncing

share_point = None
username = None
sync_folder = None  # the share folder

# udocs = None # User documents
# upics = None # User pictures
udesk = None  # User desktop


def Sync_Refresh():  # Refreshes the Sync
    #       print(sync_folder)
    for files in os.listdir(sync_folder):
        filename = files.replace(' ', '\ ')
        #               print("Targeting:" + files)
        if os.path.isdir(sync_folder + '/' + files):
            try:
                shutil.rmtree(sync_folder + '/' + files)
            except:
                print(files + " Not Found, Carry on")
        else:
            try:
                os.remove(sync_folder + '/' + files)
            except:
                print(sync_folder + '/' + files)
                print(files + " Not Found, Carry on")


class SnakeEyes:  # used to watch for changes
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = WhatHappened()  # The Handler
        self.observer.schedule(event_handler, udesk, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(0.0001)
        except:
            self.observer.stop()
            print("Error")
        self.observer.join()


class WhatHappened(FileSystemEventHandler):  # The handler
    @staticmethod
    def on_any_event(event):
        global busy
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            print("Received created event - %s." % event.src_path)
            dirsync.sync(udesk, sync_folder, 'sync')
        elif event.event_type == 'modified':
            if busy:
                print("I'm busy!")
            else:
                busy = True
                print("Received modified event - %s." % event.src_path)
                Sync_Refresh()
                dirsync.sync(udesk, sync_folder, 'sync')
                busy = False
        elif event.event_type == 'moved':
            if busy:
                print("I'm busy!")
            else:
                busy = True
                print("Received moved event - %s." % event.src_path)
                Sync_Refresh()
                dirsync.sync(udesk, sync_folder, 'sync')
                busy = False
        elif event.event_type == 'deleted':  # same for this one, refresh the entire thing
            if busy:
                print("I'm busy!")
            else:
                busy = True
                print("Received deleted event - %s." % event.src_path)
                Sync_Refresh()
                dirsync.sync(udesk, sync_folder, 'sync')
                busy = False


def is_connected(hostname):
    try:
        # see if we can resolve the host name — tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host — tells us if the host us actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        print("True")
        return True
    except:
        pass
        print("False")
    return False


# is_connected(REMOTE_SERVER)

def setup_share():
    # sets up storage if storage does not exist... Permission error gotten around by having a share folder
    if not os.path.exists(
            SHARE_POINT_PATH):
        # Have to input this manually, set to sharing. Meaning that once it becomes connected, we it should be fine
        os.makedirs(SHARE_POINT_PATH)
        print("SyncTest not found, implementing...")
    else:
        print("SyncTest located")
    global share_point
    share_point = str(SHARE_POINT_PATH)
    if not os.path.exists(share_point + '/' + username):
        os.makedirs(share_point + '/' + username)
    else:
        print("Found " + username + "\'s storage")
    global sync_folder
    sync_folder = share_point + '/' + username
    dirsync.sync(udesk, sync_folder, 'sync')
    dirsync.sync(sync_folder, udesk, 'sync')


##        def connect_folders(to_connect): ##this connects us to the other folders
##                if not os.path.exists(sync_folder + '/' + to_connect):
##                        os.makedirs(sync_folder + '/' + to_connect)
##                        print(to_connect + " has been created")
##                return (sync_folder + '/' + to_connect)
##        global udesk
##        udesk = connect_folders("Desktop")


def start_snake():
    global username
    username = getpass.getuser()
    print(username)
    setup_share()
    if __name__ == '__main__':
        w = SnakeEyes()
        w.run()


# The start up function
dir_path = os.path.dirname(os.path.realpath(__file__))  # ensures that Syncsnake is stored in the correct spot


def in_scripts():
    if dir_path.endswith('Scripts/Syncsnake'):
        print("Snycsnake is in scripts")
        global udesk
        print(dir_path)
        udesk = os.path.expanduser("~/Desktop")  # hooks up the users desktop as the emulation point
        start_snake()
    else:
        print("Not in the right place, please move Scripts/Syncsnake")


in_scripts()
