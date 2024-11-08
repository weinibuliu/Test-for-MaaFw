# maafw:2.2.0

import pathlib

from maa.resource import Resource
from maa.controller import AdbController
from maa.tasker import Tasker
from maa.toolkit import Toolkit

from src import custom_action

# 获取路径
main_path = pathlib.Path.cwd()


def main():
    act_names = custom_action.act_name()
    act_details = custom_action.acts()

    user_path = main_path
    Toolkit.init_option(user_path)

    # 加载资源
    resource = Resource()
    res_job = resource.post_path("res/Resource/base")
    res_job.wait()

    # 获取 adb 信息
    target_adb = "16416"  # 指定连接16416
    adbs = Toolkit.find_adb_devices()
    if not adbs:
        print("No Adb Device")
        exit()
    adb_data = None
    for adb in adbs:
        if adb.address.split(":")[-1] == target_adb:
            adb_data = adb
            break
    if not adb_data:
        print("No Target device.")
        exit()

    # Controller 初始化
    controller = AdbController(
        adb_path=adb_data.adb_path,
        address=adb_data.address,
        screencap_methods=adb_data.screencap_methods,
        input_methods=adb_data.input_methods,
        config=adb_data.config,
    )
    controller.post_connection().wait()
    print("Adb Connect Success.")

    # Tasker 初始化
    tasker = Tasker()
    tasker.bind(resource, controller)
    if not tasker.inited:
        print("Failed to init.")
        exit()

    # 注册自定义动作
    for act_name, act_detail in zip(act_names, act_details):
        resource.register_custom_action(act_name, act_detail)

    # 会引发异常的写法: tasker.post_pipeline("CustomA")
    # 正确的写法： tasker.post_pipeline("CustomA").wait().get()
    # 非 sample 写法，但实测正常： tasker.post_pipeline("CustomA").wait()
    # 以下写法均正常运行
    # tasker.post_pipeline("NoCustom")
    # tasker.post_pipeline("NoCustom").wait().get()
    # tasker.post_pipeline("NoCustom").wait()

    tasker.post_pipeline("CustomA").wait().get()
    print("Done")


if __name__ == "__main__":
    main()
