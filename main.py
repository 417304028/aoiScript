from utils import logger
import scripts.lxbj
import utils

if __name__ == '__main__':
    # mw.start_gui()
    utils.setup_logger()
    logger.info("程序开始运行")
    # scripts.lxbj.lxbj_001_02()
    # scripts.lxbj.lxbj_001_03()
    scripts.lxbj.lxbj_005_01()
    # scripts.lxbj.lxbj_005_02()
    logger.info("程序结束运行")
