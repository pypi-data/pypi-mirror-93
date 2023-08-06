import os
import os_tools.logger_handler as lh
import os_tools.tools as tools
import os_file_handler.file_handler as fh
import time
import pyautogui
from os_android_launcher_creator.LauncherObj import LauncherObj

##################################################################################
#
# just a bp for the launcher creator
#
##################################################################################


def paste():
    from sys import platform
    if platform == "darwin":
        hot_key(['command', 'v'])
    else:
        hot_key(['ctrl', 'v'])


def select_all():
    from sys import platform
    if platform == "darwin":
        hot_key(['command', 'a'])
    else:
        hot_key(['ctrl', 'a'])


def hot_key(btn_list):
    pyautogui.keyDown(btn_list[0])

    time.sleep(1)
    for i in range(1, len(btn_list)):
        pyautogui.keyDown(btn_list[i])

    time.sleep(1)
    for i in range(1, len(btn_list)):
        pyautogui.keyUp(btn_list[i])

    time.sleep(1)
    pyautogui.keyUp(btn_list[0])


class LauncherCreatorBP:
    STATIC_MAIN_RELATIVE_PATH = os.path.join('app', 'src')
    SECS_COOLDOWN_UNTIL_PROJECT_OPEN = 4
    LOGGER_TAG = '[Launcher Creator]'
    LAUNCHER_ICON_FILE = 'ic_launcher'

    def __init__(self, custom_android_project_path, launcher_obj_list: list[LauncherObj], shortcut_keys_to_open_image_asset,  launcher_resize_percent, launcher_background_color_hex, skip_if_output_dir_exists):
        self.logger = lh.Logger(self.LOGGER_TAG)  # build the logger
        self.custom_android_project_path = custom_android_project_path
        self.launcher_obj_list = launcher_obj_list
        self.shortcut_keys_to_open_image_asset = shortcut_keys_to_open_image_asset
        self.launcher_resize_percent = launcher_resize_percent
        self.launcher_background_color_hex = launcher_background_color_hex
        self.main_path = os.path.join(custom_android_project_path, self.STATIC_MAIN_RELATIVE_PATH)
        self.skip_if_output_dir_exists = skip_if_output_dir_exists

    def create_launcher_icons(self):
        self.print_ln()
        self.logger.info(f'Preparing to work on {str(len(self.launcher_obj_list))} icons')
        time.sleep(1)
        tools.ask_for_input('Please open your custom project in Android Studio and inform me when you are done [done]')

        self.logger.info(f'Now go back to the project and wait {str(self.SECS_COOLDOWN_UNTIL_PROJECT_OPEN)} seconds...')
        time.sleep(self.SECS_COOLDOWN_UNTIL_PROJECT_OPEN)

        for i in range(0, len(self.launcher_obj_list)):
            curr_launcher_obj = self.launcher_obj_list[i]
            self.print_ln()
            launcher_name = fh.get_dir_name(fh.get_parent_path(curr_launcher_obj.icon_path))
            self.logger.info(f'Working on: "{launcher_name}"...')

            # skip if exists
            if self.skip_if_output_dir_exists:
                if fh.is_dir_exists(curr_launcher_obj.output_path):
                    self.logger.info(f'Launcher "{launcher_name}" output path already exists. Skipping!')
                    continue

            # run current launcher
            res = self.run_cycle(self.launcher_obj_list[i])

            # do something with the response
            if res:
                self.logger.info(f'Launcher {launcher_name} done!')
            else:
                tools.ask_for_input("ERROR: It seems like the process failed for " + self.launcher_obj_list[i].icon_path + ". Let me know when you are ready to run on the same file [Enter]")
                i -= 1

        self.print_ln()

    def run_cycle(self, launcher_obj: LauncherObj):

        import random
        random_suffix = f'_{str(random.randint(0, 99999))}'
        launcher_name = f'{self.LAUNCHER_ICON_FILE}{random_suffix}'

        # open image assets
        hot_key(self.shortcut_keys_to_open_image_asset)

        time.sleep(1)

        # navigate to name
        self.logger.info('Setting temporary name...')
        pyautogui.press('tab', 2, 0.1)
        tools.copy_to_clipboard(launcher_name)
        select_all()
        paste()

        # navigate to path
        self.logger.info('Setting Path...')
        pyautogui.press('tab', 5, 0.1)
        tools.copy_to_clipboard(launcher_obj.icon_path)
        select_all()
        paste()

        self.logger.info('Disabling Trim...')
        pyautogui.press('tab', 3, 0.1)
        pyautogui.press('space')

        self.logger.info('Setting Resize...')
        pyautogui.press('tab', 2, 0.1)
        pyautogui.press('pagedown', presses=4, interval=0.1)
        time.sleep(1)
        pyautogui.press('right', presses=self.launcher_resize_percent, interval=0.1)

        time.sleep(2)
        self.logger.info('Navigating to Background tab...')
        pyautogui.press('tab', 9, 0.1)
        pyautogui.press('right')

        # time.sleep(1)

        self.logger.info('Setting Background Color...')
        pyautogui.press('tab', 3, 0.1)
        pyautogui.press('space')

        self.logger.info('Clicking and setting the color...')
        pyautogui.press('tab', 3, 0.1)
        pyautogui.press('space')
        color = self.launcher_background_color_hex.replace('#', '')
        select_all()
        pyautogui.write(color, interval=0.1)
        time.sleep(2)
        pyautogui.press('enter')

        self.logger.info('Clicking Next...')
        pyautogui.press('enter')

        time.sleep(1)
        self.logger.info('Clicking Finish...')
        pyautogui.press('enter')

        self.logger.info('Gathering files...')
        time.sleep(6)

        # launcher file continue....
        launcher_made_files = fh.search_file(self.main_path, prefix=launcher_name, recursive=True)

        self.logger.info('Copying files...')
        for launcher_file in launcher_made_files:
            rel_launcher_path = launcher_file.replace(f'{self.main_path}/', '')
            dst_launcher_file = os.path.join(launcher_obj.output_path, rel_launcher_path)
            dst_launcher_file = dst_launcher_file.replace(random_suffix, '')
            fh.copy_file(launcher_file, dst_launcher_file)

        self.logger.info('Removing temp files...')
        fh.remove_files(launcher_made_files)

        self.logger.info('waiting for next cycle...')
        time.sleep(1.5)
        return True

    def clear_old_launcher_files(self):
        self.logger.info('removing all old launcher made files...')
        launcher_made_files = fh.search_file(self.main_path, None, 'ic_launcher')
        fh.remove_files(launcher_made_files)

    def print_ln(self):
        self.logger.info('--------------------------------------------------------------------------------')

