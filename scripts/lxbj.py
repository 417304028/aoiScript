import time

import pyautogui

import utils


# 可以加装饰器，报错则自动导出log
# 复制元件（离线 写不了）
# def lxbj_001_01():
#     utils.check_and_launch_aoi()
# 新建程式元件 选择保存目录 指定导入文件 输入程式名称，是

# 整版涌向界面，扫描整版（弹窗提示是否导入默认元件库）

# 否 不导入默认元件库

# 不同类型元件手动添加检测窗口，须添加所有算法窗口

# 元件复制，黏贴在同一类型的元件

# 导出所有元件OK图

# 运行 程式

# 查看RV，SRC上元件窗口，结果值 正常显示

# # @utils.screenshot_error_to_excel
# 添加待料
def lxbj_001_02():
    utils.check_and_launch_aoi()
    # 检测是否在元器件编辑界面
    # editing_program = utils.ensure_in_specific_window("调色板","dpnlColorFilter")
    # if not editing_program:
    #     print("不在元器件编辑界面")
    #     raise Exception
    time.sleep(1)
    # 添加检测窗口 选择含有代料的窗口
    # utils.add_check_window()
    dlg = utils.connect_aoi_window().child_window(control_type="TabItem", title=" 高级 ")
    dlg.click_input()
    # utils.click_button("高级","TabItem")
    # "高级","颜色匹配"
    # # 添加标准影像 添加五种随机不同光源的代料（需添加成功）
    # for _ in range(5):
    #     utils.click_button("添加标准影像")
    #     utils.random_choose_light()
    #     utils.click_button("是")
    #     time.sleep(1)
    # # 修改窗口的算法参数值
    # utils.random_change_param()
    # # 分别点击测试当前窗口/元件/分组/面板
    # utils.click_button("测试当前窗口")
    # time.sleep(2)
    # utils.click_button("测试当前元件")
    # time.sleep(2)
    # utils.click_button("测试当前分组")
    # time.sleep(2)
    # utils.click_button("测试当前面板")


# @utils.screenshot_error_to_excel
# 不良窗口/元件
def lxbj_001_03():
    utils.check_and_launch_aoi()
    # 检查是否在元器件编辑界面(算法参数或者调色板存在)
    editing = utils.ensure_in_specific_window(name="调色板",control_type="Pane")
    if not editing:
        raise Exception
    # 选择某一窗口 点击测试当前窗口（检测窗口：缺陷名称）
    pyautogui.press("b")
    utils.click_button("测试当前窗口")
    # 查看提示：通过？红色不通过的话看原因

    # 点击测试当前元件 有不良窗口的话查看提示（左侧窗口缺陷名称默认则取算法参数界面首个不良结果对应的缺陷名）
    utils.click_button("测试当前元件")

def lxbj_005_01():
    # 参数配置——ui配置——程序设置
    
    # 选择【导出元件ok图】，不选【导出所有元件ok图】

    # 在某一元件【元器件编辑】界面，右击--【导出元件OK图】

    # 在提示框，点击【确定】

    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现

    # 删除目录D:\EYAOI\JOB\Job\Job名.oki

    # 删除目录F:\DataExport\Job名\OKImage

    pass
def lxbj_005_02():
    # 参数配置——ui配置——程序设置：

    # 不选【导出元件ok图】，选择【导出所有元件ok图】

    # 在某一元件【元器件编辑】界面，右击--【导出元件OK图】

    # 在提示框，点击【确定】

    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现

    # 删除目录D:\EYAOI\JOB\Job\Job名.oki

    # 删除目录F:\DataExport\Job名\OKImage

    pass