import threading


# 全局变量和锁
class Global:
    Software_Version = "AiNiee-chatgpt4.61-优化版"  # 软件版本号
    cache_list = []  # 全局缓存数据
    Running_status = 0  # 存储程序工作的状态，0是空闲状态,1是接口测试状态
    # 6是翻译任务进行状态，7是错行检查状态

    # 定义线程锁
    lock1 = threading.Lock()  # 这个用来锁缓存文件
    lock2 = threading.Lock()  # 这个用来锁UI信号的
    lock3 = threading.Lock()  # 这个用来锁自动备份缓存文件

    # 从 AiNiee4.py 移动过来的全局变量
    user_interface_prompter = None
    request_limiter = None
    configurator = None
    window = None
    script_dir = None
    resource_dir = None
