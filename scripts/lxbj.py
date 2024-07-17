import time
import pyautogui
import config
import utils
import shutil
import os


@utils.screenshot_error_to_excel
# 复制元件
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
    utils.ensure_in_edit_mode()
    utils.add_check_window()
    # TODO 选择含有待料的窗口 如图像匹配
    # TODO 确认在待料窗口
    utils.click_by_png(config.ADD_STANDARD_IMAGE)
    # TODO 加五种随机不同光源的待料 需确认添加成功
    utils.random_change_param()
    utils.click_by_png(config.TEST_CURRENT_WINDOW)
    time.sleep(5)
    utils.click_by_png(config.TEST_CURRENT_ELEMENT)
    time.sleep(5)
    utils.click_by_png(config.TEST_CURRENT_GROUP)
    time.sleep(5)
    utils.click_by_png(config.TEST_CURRENT_BOARD)
    time.sleep(5)
    utils.caton_or_flashback()

# 不良窗口/元件
def lxbj_003_01():
    utils.ensure_in_edit_mode()
    pyautogui.press('b')
    utils.click_by_png(config.TEST_WINDOW)
    # TODO 检测是否为不良窗口（红色 之后查看提示） 不良窗口：检测窗口 缺陷名称
    utils.click_by_png(config.TEST_CURRENT_ELEMENT)




    # TODO 如果有不良窗口。查看提示 ：元件 首个不良窗口的缺陷名称
    utils.click_by_png(config.TEST_COMPONENT)

# 返回不修改
def lxbj_004_01():
    utils.ensure_no_package(False,False)
    utils.ensure_in_edit_mode()
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK_BUTTON)
    
2、在提示框，不选【同步到相同的封装类型】，点击【否】
    pass
# 不同步封装
def lxbj_004_02():
    utils.ensure_no_package(False,False)
    utils.ensure_in_edit_mode()
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK_BUTTON)
2、在提示框，不选【同步到相同的封装类型】，点击【是】
    pass
# 同步封装
def lxbj_004_03():
    utils.ensure_no_package(False,False)
    utils.ensure_in_edit_mode()
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK_BUTTON)
2、在提示框，选择【同步到相同的封装类型】，点击【是】
# 不同步封装
def lxbj_004_04():
    utils.ensure_no_package(False,False)
    utils.ensure_in_edit_mode()
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK_BUTTON)
2、在提示框，点击【是】
# 不同步封装
def lxbj_004_05():
    utils.ensure_no_package(False,True)
    utils.ensure_in_edit_mode()
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK_BUTTON)
2、在提示框，点击【是】
    pass
# 同步封装
def lxbj_004_06():
    utils.ensure_no_package(False,True)
    utils.ensure_in_edit_mode()
    utils.random_change_param()
    utils.click_by_png(config.EDIT_BACK_BUTTON)
2、在提示框，点击【是】
3、弹框提示不勾默认选择【同步到相同的封装类型】
    pass
# 导出元件ok图
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

1、UI：参数配置--UI配置-程序设置：不选【导出元件OK图】、选择【导出所有元件OK图】
2、删除目录D:\EYAOI\JOB\Job名\Job名.oki
3、删除目录F:\DataExport\Job名\OKImage
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
1、UI：参数配置--UI配置-程序设置：选择【导出元件OK图】、不选【导出所有元件OK图】
2、删除目录D:\EYAOI\JOB\Job名\Job名.oki
3、删除目录F:\DataExport\Job名\OKImage
def lxbj_005_03():
    1、在某一元件【元器件编辑】界面，右击--【导出料号OK图】
2、点击【是】
3、在提示框，点击【确定】
    pass
1、UI：参数配置--UI配置-程序设置：不选【导出元件OK图】、选择【导出所有元件OK图】
2、删除目录D:\EYAOI\JOB\Job名\Job名.oki
3、删除目录F:\DataExport\Job名\OKImage
def lxbj_005_04():
    1、在某一元件【元器件编辑】界面，右击--【导出料号OK图】
2、点击【是】
3、在提示框，点击【确定】
    pass
1、UI：参数配置--UI配置-程序设置：选择【导出元件OK图】、不选【导出所有元件OK图】
2、删除目录D:\EYAOI\JOB\Job名\Job名.oki
3、删除目录F:\DataExport\Job名\OKImage
def lxbj_006_01():
    1、在某一元件【元器件编辑】界面，右击--【导出所有元件OK图】
2、点击【是】
3、在提示框，点击【确定】
    pass
1、UI：参数配置--UI配置-程序设置：不选【导出元件OK图】、选择【导出所有元件OK图】
2、删除目录D:\EYAOI\JOB\Job名\Job名.oki
3、删除目录F:\DataExport\Job名\OKImage
def lxbj_006_02():
    1、在某一元件【元器件编辑】界面，右击--【导出所有元件OK图】
2、点击【是】
3、在提示框，点击【确定】
    pass
参数配置--演算法配置--关联子框检测模式：选择【父框检测NG不计算】
def lxbj_007_01():
    1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
2、父、子框同时选中后，点击上方【关联】
3、选中父框，如向上移动，使之测试结果变成NG
4、选择子框后，点击【测试当前窗口】
5、点击【测试当前元件】
6、点击【测试当前分组】
    pass
1、参数配置--演算法配置--关联子框检测模式：选择【父框检测NG不计算】
2、父框检测结果是良好
def lxbj_007_02():
    1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
2、父、子框同时选中后，点击上方【关联】
3、选择子框后，点击【测试当前窗口】
4、点击【测试当前元件】
5、点击【测试当前分组】
    pass
参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续计算】
def lxbj_008_01():
    1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
2、父、子框同时选中后，点击上方【关联】
3、选中父框，如向上移动，使之测试结果变成NG
4、选择子框后，点击【测试当前窗口】
5、点击【测试当前元件】
6、点击【测试当前分组】
    pass
1、参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续计算】
2、父框检测结果是良好
def lxbj_008_02():
    1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
2、父、子框同时选中后，点击上方【关联】
3、选择子框后，点击【测试当前窗口】
4、点击【测试当前元件】
5、点击【测试当前分组】
    pass
参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续关联】
def lxbj_009_01():
1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
2、父、子框同时选中后，点击上方【关联】
3、选中父框，如向上移动，使之测试结果变成NG
4、选择子框后，点击【测试当前窗口】
5、点击【测试当前元件】
6、点击【测试当前分组】
    pass
1、参数配置--演算法配置--关联子框检测模式：选择【父框检测NG继续关联】
2、父框检测结果是良好
def lxbj_009_02():
    1、在某一元件的【元器件编辑】界面，点击上方【检测窗口】添加父、子框，如父框：方形定位、子框：颜色面积
2、父、子框同时选中后，点击上方【关联】
3、选择子框后，点击【测试当前窗口】
4、点击【测试当前元件】
5、点击【测试当前分组】
    pass
def lxbj_010_01():
    1、点击【工具】--【封装类型管理】
2、在弹窗左侧选择1个封装类型，点击【编辑封装类型】，输入新的封装类型名称，点击【是】

    pass
def lxbj_010_02():
    1、点击【工具】--【封装类型管理】
2、在弹窗左侧选择多个封装类型，点击【编辑封装类型】，输入新的封装类型名称，点击【是】

    pass

def lxbj_010_03():
    1、点击【工具】--【封装类型管理】
2、在弹窗左侧选择1个封装类型，点击【清除封装类型】
    pass
def lxbj_010_04():
    1、点击【工具】--【封装类型管理】
2、在弹窗左侧选择多个封装类型，点击【清除封装类型】
    pass

def lxbj_011_01():
    1、在整板视图，点击左上方【板】-【FOV】
2、在弹窗【FOV检测】-【异物】：选择所有子选项，其中【类型】选择【元件遮罩】，点击【是】关闭弹窗。
3、【确定】关闭弹框
4、在整板视图界面中，右击，选择【整板抽色】，在【Frm_BoardColorFilter】弹窗中完成整板抽色操作。
5、在整板视图界面中，点击【整板异物】Tab页，【高级】--【扩展(um)】栏，修改扩展值，如将默认的150改为3000
6、在【整板异物】Tab页，点击【整板遮罩编辑】，查看元件的遮罩
    pass
1、元件包含【图像匹配】窗口
2、【图像匹配】窗口包含多个代料
def lxbj_012_01():
    1、在某一元件【元器件编辑】界面，选择元件【图像匹配】窗口2、在调色板中，修改不同代料的RGB值(红、绿、蓝、限的值)
3、查看不同代料的RGB值、
    pass
1、元件包含【颜色匹配】窗口
2、【颜色匹配】窗口包含多个代料
def lxbj_012_02():
    1、在某一元件【元器件编辑】界面，选择元件【颜色匹配】窗口2、在调色板中，修改不同代料的RGB值(红、绿、蓝、限的值)
3、查看不同代料的RGB值
    pass
1、元件包含【引脚相似度匹配】窗口
2、【引脚相似度匹配】窗口包含多个代料
def lxbj_012_03():
    1、在某一元件【元器件编辑】界面，选择元件【引脚相似度匹配】窗口2、在调色板中，修改不同代料的RGB值(红、绿、蓝、限的值)
3、查看不同代料的RGB值
    pass
1、元件包含【引脚检测】窗口
2、【引脚检测】窗口包含多个代料
def lxbj_012_04():
    1、在某一元件【元器件编辑】界面，选择元件【引脚检测】窗口2、在调色板中，修改不同代料的RGB值(红、绿、蓝、限的值)
3、查看不同代料的RGB值
    pass
# 13开头的前置条件 设置保存Debug程式快捷键，如Ctrl+Alt+F12 设置打开Debug程式快捷键，Ctrl+Alt+F2 djb文件的元件包含多个检测窗口
def lxbj_013_01():
    1、使用快捷键，打开某一包含多个检测窗口的djb文件
2、在【窗口列表】第一个窗口设置为不勾选，即第1个窗口不检测
3、点击【编辑】--【返回】
4、【是】保存修改
5、双击该元件，查看该元件窗口列表
    pass

def lxbj_013_02():
    1、使用快捷键，打开某一包含多个检测窗口的djb文件
2、在【窗口列表】将第一个窗口设置为不勾选
3、点击上方【导出当前料号】导出料号
4、在【窗口列表】将第一个窗口设置为勾选
5、点击上方【导入当前料号】导入刚导出的料号
6、查看料号的窗口列表                                                 
    pass

def lxbj_013_03():
    1、使用快捷键，打开某一包含多个检测窗口的djb文件
2、在【窗口列表】将第一个窗口设置为勾选
3、点击上方【导出当前料号】导出料号
4、在【窗口列表】将第一个窗口设置为不勾选
5、点击上方【导入当前料号】导入刚导出的料号
6、查看料号的窗口列表                                                 
    pass

# 14开头的前置条件：元件带有字符检测窗口
def lxbj_014_01():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：标准，【字体工艺】选择：默认
4、点击上方【测试当前窗口】
    pass


def lxbj_014_02():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：标准，【字体工艺】选择：丝印
4、点击上方【测试当前窗口】
    pass


def lxbj_014_03():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：标准，【字体工艺】选择：点阵
4、点击上方【测试当前窗口】
    pass

def lxbj_014_04():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：标准，【字体工艺】选择：晶体管
4、点击上方【测试当前窗口】
    pass
def lxbj_014_05():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：图例，【字体工艺】选择：默认
4、点击上方【测试当前窗口】
    pass
def lxbj_014_06():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：图例，【字体工艺】选择：丝印
4、点击上方【测试当前窗口】
    pass
def lxbj_014_07():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：图例，【字体工艺】选择：点阵
4、点击上方【测试当前窗口】
    pass
def lxbj_014_08():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：图例，【字体工艺】选择：晶体管
4、点击上方【测试当前窗口】
    pass

def lxbj_014_09():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：参数，【字体工艺】选择：默认
4、点击上方【测试当前窗口】
    pass

def lxbj_014_10():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：参数，【字体工艺】选择：丝印
4、点击上方【测试当前窗口】
    pass

def lxbj_014_11():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：参数，【字体工艺】选择：点阵
4、点击上方【测试当前窗口】
    pass

def lxbj_014_12():
    1、某一元件的【元器件编辑】界面
2、在左侧【元件窗口】列表中，双击【字符检测】窗口
3、在右侧【算法参数】栏中，【检测模式】选择：参数，【字体工艺】选择：晶体管
4、点击上方【测试当前窗口】
    pass

def lxbj_015_01():
    1、某一元器件编辑界面，在上方【编辑】--【光源】选择不同光源，如中角度（不选均匀光）；
2、添加方形定位检测窗口，查看右侧【算法参数】--【2D光源】
3、返回修改该元件；
4、再次进入该元器件编辑界面，查看方形定位窗口的【算法参数】--【2D光源】
    pass
元件添加参考点关联所有检测框
def lxbj_016_01():
    1、在整板视图界面，右击某一元件--【添加参考点】
2、进入该元件的【元器件编辑】界面，全选所有检测框；
3、点击上方【编辑】--【关联】
4、点击上方【编辑】--【取消关联】
    pass
元件添加参考点关联所有检测框
def lxbj_016_02():
    1、在整板视图界面，右击某一元件--【添加参考点】
2、进入该元件的【元器件编辑】界面，全选所有检测框；
3、【右击】--【关联】
4、【右击】--【取消关联】
    pass
元件添加参考点关联所有检测框
def lxbj_016_03():
1、在整板视图界面，右击某一元件--【添加参考点】
2、进入该元件的【元器件编辑】界面，全选所有检测框；
3、使用【链接元件所有检测框】快捷键（【参数配置】--【快捷】查看该捷键），关联检测框
    pass
元件添加参考点关联所有检测框
def lxbj_016_04():
    1、在整板视图界面，右击某一元件--【添加参考点】
2、进入该元件的【元器件编辑】界面，全选所有检测框；
3、【右击】--【自动链接元件检测框】
    pass
元件添加参考点关联所有检测框
def lxbj_016_05():
    1、在整板视图界面，右击某一元件--【添加参考点】
2、进入该元件的【元器件编辑】界面，选择某一父框和子框；
3、点击上方【编辑】--【关联】
4、点击上方【编辑】--【取消关联】
    pass
# 客户JOB名称和地址：H898_E1_256G+8G_V1.2_TOP_A2（\\192.168.201.215\f\AOI-JOB\泰衡诺科技）
# 离线测试窗口
def lxbj_017_01():
    1，【程式元件】--【料/位号】：输入C2745，点击放大镜图标查找
2，双轨元件进入元件编辑界面
3，测试当前窗口
4，其他三个元件也要测试
    pass

def lxbj_018_01():
    1、打开一个编辑过的有多个拼版的job
2、左侧选择板--选择一个拼版右键--删除拼版
3、点击【是】
4、勾选保留此拼板下的元件
5、点击【是】
    pass

def lxbj_018_02():
    1、打开一个编辑过的有多个拼版的job
2、点击【拼板操作】并选中一个拼版
3、点击【删除拼板】
4、勾选保留此拼板下的元件
5、点击【是】
    pass

def lxbj_018_03():
    1、打开一个编辑过的有多个拼版的job
2、左侧选择板--选择一个拼版右键--删除拼版
3、点击【是】
4、勾选保留基准点
5、点击【是】
    pass
# 选择一个拼版删除并保留基准点
def lxbj_018_04():
    1、打开一个编辑过的有多个拼版的job
2、点击【拼板操作】并选中一个拼版
3、点击【删除拼板】
4、勾选保留基准点
5、点击【是】
    pass



