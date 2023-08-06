from os_android_launcher_creator.bp import _launcher_creator as bp
from typing import Callable, Any, Iterable
from os_android_launcher_creator import AppObj

from typing import List
##################################################################################
#
# This module aim is to create a launcher icon for a given app using
# Android Studio automation
#
##################################################################################

screen_width = False
screen_height = False


def create_launcher_icons(custom_android_project_path,
                          app_list: List[AppObj],
                          shortcut_keys_to_open_image_asset= ['shift', 'b'],
                          launcher_resize_percent=50,
                          launcher_background_color_hex='#ffffff'):
    """
    Will create a launcher icons from a given icon
    NOTICE: the automation need to run in an open project in Android Studio so make sure you open one to work on!

    Args:
        custom_android_project_path: the current open Android Studio project
        app_list: a list containing the AppObj. Every AppObj contains the path to the launcher and and a path to the destination files to be copied
        shortcut_keys_to_open_image_asset: the list of buttons to hold together in order to open the Image Asset in Android Studio
        launcher_resize_percent: the resize percents of the icon to fit the frame in the editor
        launcher_background_color_hex: the color of the background of the icons
    """
    inst = bp.LauncherCreatorBP(custom_android_project_path, app_list, shortcut_keys_to_open_image_asset,  launcher_resize_percent, launcher_background_color_hex)
    inst.create_launcher_icons()
