from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 收集 paddleocr 包的所有数据文件（例如配置文件、非 Python 文件等）
datas = collect_data_files('paddleocr.tools')


# 收集 paddleocr 包下所有的子模块，包括 tools 等
hiddenimports = collect_submodules('paddleocr.tools')