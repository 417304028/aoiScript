import config
import utils


def jbgn_001_01():
    for i in range(3):
        # 确保aoi打开
        utils.check_and_launch_aoi()
        # 打开程式 （需识别打开程式的弹窗，无则截图并保存）
        # utils.click_button(config.OPEN_PROGRAM_PATH, 1)
        # 输入程式主目录（显示全目录的所有程式）

        # 程式列表-主目录程式下任选一个并双击（出现在右侧列表中）

        # 看是否能实现下移

        if i < 2:
            # 点击取消（弹窗消失并返回之前的整版视图）
            utils.click_button(config.OPEN_PROGRAM_NO, 1)
        else:
            # 重复步骤 打开——至——取消 三次后 点击确定按钮
            utils.click_button(config.OPEN_PROGRAM_YES, 1)
    # 有进度条提示，加载后无闪退


def jbgn_001_02():
    pass

def jbgn_001_03():
    pass

def jbgn_001_04():
    pass