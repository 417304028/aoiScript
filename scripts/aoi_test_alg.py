from .. import utils


# 测试job算法
def aoi_test_alg():
    # 打开aoi
    utils.check_and_launch_aoi()
    # 打开指定路径job
    open_job()
    # 获取程式元件列表
    get_component_list()
    print(ALL_COMPONENTS)
    # 选择元件 TODO 后面再修改
    for component in ALL_COMPONENTS:
        if not component['seen']:  # 只处理未处理的元件
            component_test(component)
