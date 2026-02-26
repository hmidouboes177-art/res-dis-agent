# init_login.py
from playwright.sync_api import sync_playwright
import os

from browser_config import USER_DATA_DIR, get_proxy_config

def setup_initial_login():
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    
    with sync_playwright() as p:
        print(" 正在启动带远程调试端口的浏览器...")
        # 在 launch_persistent_context 中添加 proxy 和 ignore_https_errors 参数
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            # 1. 解决自签名证书拦截问题
            ignore_https_errors=True,

            # 2. 可选代理配置（通过环境变量控制）
            proxy=get_proxy_config(),

            args=[
                "--remote-debugging-port=9222",
                "--remote-debugging-address=127.0.0.1",
                # 双重保险：在底层 Chromium 参数中强制忽略证书错误
                "--ignore-certificate-errors",
            ],
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
       
        page = context.new_page()
        page.goto("https://www.reddit.com/login")
        
        print("\n" + "="*60)
        print(" 浏览器已启动并在后台挂起！")
        print("1. 请在你的【本地电脑】终端执行 SSH 端口转发命令")
        print("2. 在本地浏览器中访问 http://127.0.0.1:9222")
        print("3. 点击页面进入 Reddit，手动完成 Google SSO 登录")
        print("4. 登录成功看到首页后，回到此服务器终端按下【回车键】")
        print("="*60 + "\n")
        
        # 阻塞程序，直到你在本地完成登录并敲击回车
        input("等待手动操作... 完成登录后请按【回车键】关闭浏览器并保存状态：")
        
        print(" 正在保存 Cookie 和登录状态...")
        context.close()
        print("✅ 环境初始化完成！")

if __name__ == "__main__":
    setup_initial_login()
