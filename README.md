# TagSysAdmin


使用 logger 说明 (未实现)

1。 新建py文件
2。 导入 from flask import current_app
3。 current_app.logger.info("this is info")

注意：
1。新建文件 第一行需要 # -*- coding: utf-8 -*-

使用settings.py说明

1。在app.py 中 app.config.from_object(conf["pro"])  来控制 test 和 pro环境

线下：请使用 test环境


