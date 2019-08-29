# !/uer/bin/env python3
# coding=utf-8

__author__ = 'Medivh Xu'

__version__ = '1.0.8'

"""
1.0.0 version update:
* 首次提交 可以做基本的接口测试使用
"""

"""
1.0.1 version update:
* 修复requests依赖中,urllib3中的高危漏洞
"""

"""
1.0.2 version update:
* 优化字符串拼接类中，字符串排序方法名称
* 修复start脚本中的取用户token等参数错误
* 修复start脚本中请求参数写死时抛异常，缺少必要参数
"""

"""
1.0.3 version update:
* 修复数据库连接失败异常，增加update、insert方法
* 增加格式异常类
"""

"""
1.0.4 version update:
* 修复数据库update方法返回值问题
"""

"""
1.0.5 version update:
* 修改数据库select_all返回数据缺失；
* 删除log.py，集成进runner.py中；
* 优化send_email方法；
* 
"""

"""
1.0.6 version update:
* 优化数据库调用方法；
* 还原loger文件；
* 新增用例批量读取方法；
* 优化test_start,拆解请求步骤；
* 新增charles导出chlsj文件支持；
"""

"""
1.0.7 version update:
* 修复bug；
* 修改chlsj文件支持格式变动；
"""

"""
1.0.8 version update:
* 修复bug；
* 抽出主线中，数据前置处理和后置处理；
* 新增user类和生成外部orderId类；
* 优化数据后置处理方法；
"""
