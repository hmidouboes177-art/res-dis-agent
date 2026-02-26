# Reddit 自动化脚本使用说明

本项目包含两个 Playwright 脚本：
- `init_login.py`：首次人工登录 Reddit，生成并保存用户指纹（浏览器持久化数据）。
- `daily_search.py`：复用已生成的用户指纹进行后续访问和搜索。

## 1) 环境信息

- 运行环境：**Linux 服务器（无桌面 UI）**。
- 因为服务器无 UI，浏览器画面需要通过 **SSH 端口转发 + 本地 Chrome 调试面板** 来操作。

## 2) 配置文件

脚本统一读取项目根目录下的 `cfg.env`：

```env
# 登录指纹目录（持久化 Chrome 用户数据）
USER_DATA_DIR=/root/reddit-new/chrome_data

# 代理配置（不需要代理时把 PROXY_SERVER 留空）
PROXY_SERVER=
PROXY_USERNAME=
PROXY_PASSWORD=
```

说明：
- `USER_DATA_DIR`：用于保存/复用 Playwright 持久化登录指纹。
- `PROXY_SERVER` 为空时，不启用代理。

## 3) 第一步：先运行 `init_login.py` 生成用户指纹

在服务器上执行：

```bash
python init_login.py
```

脚本会启动 Chromium 并监听调试端口 `9222`，然后等待你手动登录 Reddit。

### SSH 端口转发

请在你本地电脑终端执行（按你的服务器地址修改）：

```bash
ssh -L 9222:127.0.0.1:9222 <your_user>@<your_server_ip>
```

### 如果打开 `http://127.0.0.1:9222` 是白屏

这通常是经典问题：
- SSH 隧道其实已经打通；
- 但 Chromium 安全策略（例如 DNS 重新绑定防护）或 DevTools 静态资源加载失败，导致页面空白。

此时浏览器进程大概率仍正常。**建议优先使用下面最稳妥的方法**：

#### 方法一（强烈推荐）：使用本地 Chrome 的 `chrome://inspect/#devices`

1. 本地 Chrome 打开：`chrome://inspect/#devices`
2. 勾选 **Discover network targets**。
3. 点击 **Configure...**，添加：`127.0.0.1:9222`（或 `localhost:9222`）。
4. 等待几秒，在 **Remote Target** 列表中找到服务器上的页面。
5. 点击对应页面下的 **inspect**，即可打开可实时操作的调试窗口。
6. 在该窗口中手动完成 Reddit 登录。

登录成功后，回到服务器终端按回车，`init_login.py` 会保存状态到 `USER_DATA_DIR`。

## 4) 第二步：运行 `daily_search.py` 复用第 1 步指纹

在同一配置下执行：

```bash
python daily_search.py
```

脚本会使用第 1 步生成的 `USER_DATA_DIR`（app_data 指纹）启动浏览器并访问 Reddit。

---

如果后续还有更多配置项，直接在 `cfg.env` 中追加即可，无需逐个设置环境变量。
