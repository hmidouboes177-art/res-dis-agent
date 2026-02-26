from playwright.sync_api import sync_playwright
import time
import urllib.parse
# ⚠️ 注意替换为你实际的路径
USER_DATA_DIR = "/root/reddit-new/chrome_data" 


def auto_search(keyword):
    with sync_playwright() as p:
        print(" 加载已登录的环境...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,  
            ignore_https_errors=True, 
            proxy={
                "server": "xxx",  # 例如: "http://192.168.1.100:8080"
                "username": "xxx",             # 如果代理不需要密码，把 username 和 password 删掉
                "password": "xxx"
            },
            args=["--ignore-certificate-errors"],
            slow_mo=50,
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        encoded_keyword = urllib.parse.quote(keyword)
        search_url = f"https://www.reddit.com/search/?q={encoded_keyword}"
        
        try:
            print(f" 直接访问搜索链接: {search_url}")
            page.goto(search_url, timeout=60000, wait_until="domcontentloaded") 
            
            # 给页面动态数据(API)渲染留出 3 秒缓冲时间
            time.sleep(3) 
            
            # ==========================================
            # 数据抓取与清洗逻辑
            # ==========================================
            post_links = page.locator('a[href*="/comments/"]').all()
            
            if not post_links:
                print("⚠️ 未找到任何帖子，可能是网络加载失败或该关键词无结果。")
            else:
                # 使用字典进行去重：URL 为 key，标题为 value
                cleaned_posts = {}
                
                for element in post_links:
                    href = element.get_attribute('href')
                    text = element.inner_text().strip().replace('\n', ' ')
                    
                    # 过滤掉图片张数标记(如 1/3...)、无意义的省略号、或单纯的"评论"字眼
                    if not text or text == '...' or text.isdigit() or '评论' in text or 'comments' in text.lower():
                        continue
                    
                    # 补全相对路径为绝对路径
                    if href.startswith('/'):
                        href = "https://www.reddit.com" + href
                        
                    # 去重逻辑：如果同一个链接抓到了多个文本，保留最长的那个（通常最长的是完整标题）
                    if href in cleaned_posts:
                        if len(text) > len(cleaned_posts[href]):
                            cleaned_posts[href] = text
                    else:
                        cleaned_posts[href] = text
                
                # 打印最终清洗后的清爽数据
                print(f"\n 成功抓取并去重，共找到 {len(cleaned_posts)} 条有效帖子：\n" + "-"*50)
                
                # 遍历打印结果
                for i, (url, title) in enumerate(cleaned_posts.items(), 1):
                    print(f"[{i}] {title}")
                    print(f"    链接: {url}\n")
                    
        except Exception as e:
            print(f"❌ 发生异常: {e}")
            page.screenshot(path="final_error.png")
            print("已保存错误截图至 final_error.png")
        
        # 抓取完毕，关闭浏览器
        context.close()

if __name__ == "__main__":
    auto_search("ai")
