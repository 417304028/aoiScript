import time
import pyautogui
import config
import utils
import shutil
import os


# 可以加装饰器，报错则自动导出log
# 复制元件（离线 写不了）
def lxbj_001_01():
#     utils.check_and_launch_aoi()
# 新建程式元件 选择保存目录 指定导入文件 输入程式名称，是

# 整版涌向界面，扫描整版（弹窗提示是否导入默认元件库）

# 否 不导入默认元件库

# 不同类型元件手动添加检测窗口，须添加所有算法窗口

# 元件复制，黏贴在同一类型的元件

# 导出所有元件OK图

# 运行 程式

# 查看RV，SRC上元件窗口，结果值 正常显示
    pass
@utils.screenshot_error_to_excel

# 添加待料
def lxbj_002_01():
    pass

# 不良窗口/元件
def lxbj_003_01():
    pass

def lxbj_004_01():
    pass

def lxbj_004_02():
    pass

def lxbj_004_03():
    pass

def lxbj_004_04():
    pass

def lxbj_004_05():
    pass

def lxbj_004_06():
    pass

@utils.screenshot_error_to_excel
def lxbj_005_01():
    utils.check_and_launch_aoi()
    # 参数配置——ui配置——程序设置
    utils.click_by_png(config.SETTING)
    utils.click_by_png(config.HARDWARE_SETTING)
    # 确认加载完毕
    utils.search_symbol(config.PARAM_SETTING_TOPIC, 5)
    utils.click_by_png(config.PARAM_UI_TOPIC)
    time.sleep(1.5)
    # 选择【导出元件ok图】，不选【导出所有元件ok图】
    export_one_checked = utils.is_checked((659,726),(671,738))
    export_all_checked = utils.is_checked((659,751),(671,763))
    if not export_one_checked:
        pyautogui.click(utils.get_center_coordinates((659,726),(671,738)))  # 点击【导出元件ok图】的中心坐标
    if export_all_checked:
        pyautogui.click(utils.get_center_coordinates((659,751),(671,763)))  # 点击【导出所有元件ok图】的中心坐标
    utils.click_by_png(config.PARAM_SETTING_YES)
    utils.click_by_png(config.PARAM_SETTING_CLOSE)
    # 在某一元件【元器件编辑】界面，右击--【导出元件OK图】
    point = (935,445)
    pyautogui.rightClick(point)
    utils.click_by_png(config.EXPORT_COMPONENT_OK)
    # 在提示框，点击【确定】
    a = utils.search_symbol(config.EXPORT_COMPONENT_SUCCESS, 5)
    if not a:
        raise Exception
    utils.click_by_png(config.EXPORT_COMPONENT_SUCCESS)
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    utils.click_by_png(config.RUN)
    program_name = utils.read_text(110,70)
    # 删除目录D:\EYAOI\JOB\Job\Job名.oki
    shutil.rmtree(f"D:\\EYAOI\\JOB\\{program_name}\\{program_name}.oki")
    # 删除目录F:\DataExport\Job名\OKImage
    shutil.rmtree(f"F:\\DataExport\\{program_name}\\OKImage")


@utils.screenshot_error_to_excel
def lxbj_005_02():
    utils.check_and_launch_aoi()
    # 参数配置——ui配置——程序设置
    utils.click_by_png(config.SETTING)
    utils.click_by_png(config.HARDWARE_SETTING)
    # 确认加载完毕
    utils.search_symbol(config.PARAM_SETTING_TOPIC, 5)
    utils.click_by_png(config.PARAM_UI_TOPIC)
    time.sleep(1.5)
    # 不选【导出元件ok图】，选择【导出所有元件ok图】
    export_one_checked = utils.is_checked((659,726),(671,738))
    export_all_checked = utils.is_checked((659,751),(671,763))
    if export_one_checked:
        pyautogui.click(utils.get_center_coordinates((659,726),(671,738)))  # 点击【导出元件ok图】的中心坐标
    if not export_all_checked:
        pyautogui.click(utils.get_center_coordinates((659,751),(671,763)))  # 点击【导出所有元件ok图】的中心坐标
    utils.click_by_png(config.PARAM_SETTING_YES)
    utils.click_by_png(config.PARAM_SETTING_CLOSE)
    # 在某一元件【元器件编辑】界面，右击--【导出元件OK图】
    point = (935, 445)
    pyautogui.rightClick(point)
    utils.click_by_png(config.EXPORT_COMPONENT_OK)
    # 在提示框，点击【确定】
    a = utils.search_symbol(config.EXPORT_COMPONENT_SUCCESS, 5)
    if not a:
        raise Exception
    utils.click_by_png(config.EXPORT_COMPONENT_SUCCESS)
    # 弹框提示：生成ok图完成，并可以在F:\DataExport\Job名\OKImage下发现
    utils.click_by_png(config.RUN)
    program_name = utils.read_text(110,70)
    # 删除目录D:\EYAOI\JOB\Job\Job名.oki
    shutil.rmtree(f"D:\\EYAOI\\JOB\\{program_name}\\{program_name}.oki")
    # 删除目录F:\DataExport\Job名\OKImage
    shutil.rmtree(f"F:\\DataExport\\{program_name}\\OKImage")

# 导出料号ok图
def lxbj_005_03():
    pass

def lxbj_005_04():
    pass

def lxbj_006_01():
    pass

def lxbj_006_02():
    pass
def lxbj_007_01():
    pass

def lxbj_007_02():
    pass
def lxbj_008_01():
    pass

def lxbj_008_02():
    pass
def lxbj_009_01():
    pass

def lxbj_010_01():
    pass
def lxbj_010_02():
    pass

def lxbj_010_03():
    pass
def lxbj_010_04():
    pass

def lxbj_011_01():
    pass
def lxbj_012_01():
    pass

def lxbj_012_02():
    pass
def lxbj_012_03():
    pass

def lxbj_012_04():
    pass
def lxbj_013_01():
    pass

def lxbj_013_02():
    pass

def lxbj_013_03():
    pass


def lxbj_014_01():
    pass


def lxbj_014_02():
    pass


def lxbj_014_03():
    pass

def lxbj_014_04():
    pass
def lxbj_014_05():
    pass
def lxbj_014_06():
    pass
def lxbj_014_07():
    pass
def lxbj_014_08():
    pass

def lxbj_014_09():
    pass

def lxbj_014_10():
    pass

def lxbj_014_11():
    pass

def lxbj_014_12():
    pass

def lxbj_015_01():
    pass

def lxbj_016_01():
    pass

def lxbj_016_02():
    pass

def lxbj_016_03():
    pass

def lxbj_016_04():
    pass

def lxbj_016_05():
    pass

def lxbj_017_01():
    pass

def lxbj_018_01():
    pass

def lxbj_018_02():
    pass

def lxbj_018_03():
    pass

def lxbj_018_04():
    pass



