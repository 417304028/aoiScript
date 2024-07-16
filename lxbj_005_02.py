from scripts import lxbj
from utils import logger
from utils import setup_logger
if __name__ == '__main__':
    setup_logger()
    logger.info("程序开始运行")
    lxbj.lxbj_005_02()
    logger.info("程序结束运行")