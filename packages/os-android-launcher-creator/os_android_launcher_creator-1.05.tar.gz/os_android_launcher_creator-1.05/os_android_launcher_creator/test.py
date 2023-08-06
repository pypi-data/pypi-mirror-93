import os
from os_file_handler import file_handler as fh
from os_xml_handler import xml_handler as xh
from os_tools import tools
from os_android_launcher_creator import launcher_creator

IS_APP_SMART = 'true'


def start():
    apps_dir = '/Users/home/Google Drive/Remotes/Android/osfunapps_updates/old_apps/work/test_batch'

    app_dirs = fh.get_dir_content(apps_dir, collect_files=False, collect_dirs=True)
    done_dir = '/Users/home/Google Drive/Remotes/Android/osfunapps_updates/old_apps/work/done'

    apps = []
    for app_dir in app_dirs:
        # launcher logo
        icon_path = os.path.join(app_dir, 'logo.png')
        output_path = os.path.join(app_dir, 'files', 'launcher')
        apps.append(launcher_creator.AppObj(icon_path, output_path))

    launcher_creator.create_launcher_icons('/Users/home/Programming/android/Remotes/Projects/GeneralRemoteAndroid', apps, ['shift', 'b'], 65)

    # # done
    # dst_app_dir = os.path.join(done_dir, fh.get_dir_name(app_dir))
    # fh.copy_dir(app_dir, dst_app_dir)
    # fh.remove_dir(app_dir)


def is_ad_node_exists(parent_node, att_name_value):
    return xh.find_all_nodes(parent_node, 'ad', 'name', att_name_value)


if __name__ == "__main__":
    start()
