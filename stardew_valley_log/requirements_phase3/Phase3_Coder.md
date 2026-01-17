<!--第三阶段重点：1、深入学习Git/GitHub 2、深入学习爬虫 3、高级图像可视化（三维图表、阶梯图、局部放大图、桑基图等）-->

# 美赛第三阶段训练 - 代码手实操指南

**核心职责：** 掌握Git/GitHub协作 + 熟练使用爬虫 + 高级可视化技能  
**时间安排：** 4天，每天4-5小时，共16-20小时  
**前置条件：** 已完成第二阶段任务，掌握基础可视化和爬虫入门

---

## 第二阶段问题回顾与改进

### 已达成目标 ✅
- [x] 可视化质量提升（关键信息标注、统计信息）
- [x] 图表类型扩展（热力图、箱线图、堆叠图等）
- [x] 爬虫基础入门（requests + BeautifulSoup）
- [x] Git/GitHub基本操作

### 需要改进的问题 ⚠️

**问题1：Git/GitHub使用不够深入**
- 表现：只掌握基本操作，协作流程不熟练
- 改进：深入学习分支管理、冲突解决、Pull Request等高级功能

**问题2：爬虫能力有限**
- 表现：只能爬取静态网页，无法处理动态内容
- 改进：学习Selenium、API调用、反爬虫应对

**问题3：可视化图表类型不够高级**
- 表现：缺少三维图表、复杂图表类型
- 改进：学习三维可视化、阶梯图、局部放大图、桑基图等高级图表

---

## Day 1：Git/GitHub深入学习（4-5小时）

### 任务1.1：Git分支管理进阶（1.5小时）

#### 做什么
深入学习Git分支管理，掌握分支创建、合并、删除等操作，理解分支策略。

#### 用什么做
- **工具：** Git命令行、GitHub Desktop（可选）
- **关键命令：** `git branch`, `git checkout`, `git merge`, `git rebase`, `git cherry-pick`

#### 怎么做

**1. 分支策略理解**
- **主分支（main/master）：** 稳定版本，用于发布
- **开发分支（develop）：** 开发主分支
- **功能分支（feature）：** 新功能开发
- **修复分支（hotfix）：** 紧急bug修复
- **发布分支（release）：** 版本发布准备

**2. 分支操作实践**

```bash
# 查看所有分支
git branch -a                    # 查看本地和远程分支
git branch -r                    # 只查看远程分支

# 创建和切换分支
git branch feature/new-viz       # 创建分支
git checkout feature/new-viz     # 切换分支
git checkout -b feature/new-viz  # 创建并切换（常用）

# 合并分支
git checkout main                # 切换到主分支
git merge feature/new-viz        # 合并功能分支
git merge --no-ff feature/new-viz  # 保留分支历史

# 删除分支
git branch -d feature/new-viz    # 删除本地分支（已合并）
git branch -D feature/new-viz    # 强制删除本地分支
git push origin --delete feature/new-viz  # 删除远程分支

# 查看分支历史
git log --oneline --graph --all  # 图形化查看分支历史
```

**3. 分支合并策略**

**Fast-forward合并：**
```bash
git checkout main
git merge feature/new-viz        # 如果main没有新提交，会fast-forward
```

**No-fast-forward合并（推荐）：**
```bash
git merge --no-ff feature/new-viz  # 保留分支历史，创建合并提交
```

**4. 解决合并冲突**

```bash
# 当合并出现冲突时
git merge feature/new-viz

# 查看冲突文件
git status

# 手动编辑冲突文件（标记<<<<<<< ======= >>>>>>>）
# 解决冲突后
git add .
git commit -m "[Merge] 解决合并冲突"
```

**5. 分支重命名**
```bash
git branch -m old-name new-name  # 重命名本地分支
git push origin -u new-name      # 推送新分支
git push origin --delete old-name  # 删除远程旧分支
```

#### 实操任务
- [ ] 创建功能分支`feature/advanced-viz`
- [ ] 在分支上开发新功能
- [ ] 合并到主分支
- [ ] 练习解决合并冲突
- [ ] 删除不需要的分支

---

### 任务1.2：Git高级操作（1.5小时）

#### 做什么
学习Git的高级操作，包括暂存、撤销、回退、标签等。

#### 用什么做
- **关键命令：** `git stash`, `git reset`, `git revert`, `git tag`, `git rebase`

#### 怎么做

**1. 暂存更改（Stash）**

```bash
# 保存当前工作区更改
git stash                        # 暂存更改
git stash save "描述信息"        # 带描述的暂存

# 查看暂存列表
git stash list

# 恢复暂存
git stash pop                   # 恢复并删除最新的暂存
git stash apply stash@{0}       # 恢复指定暂存，不删除
git stash drop stash@{0}        # 删除指定暂存

# 清空所有暂存
git stash clear
```

**2. 撤销和回退**

```bash
# 撤销工作区更改（未add）
git checkout -- filename        # 撤销单个文件
git checkout -- .               # 撤销所有文件

# 撤销暂存区更改（已add但未commit）
git reset HEAD filename         # 取消暂存单个文件
git reset HEAD .                # 取消暂存所有文件

# 回退提交
git reset --soft HEAD~1         # 回退提交，保留更改在暂存区
git reset --mixed HEAD~1        # 回退提交，保留更改在工作区（默认）
git reset --hard HEAD~1         # 回退提交，丢弃所有更改（危险！）

# 回退到指定提交
git reset --hard commit-hash    # 回退到指定commit

# 撤销提交但保留更改（推荐）
git revert HEAD                 # 创建新提交撤销上一次提交
git revert commit-hash          # 撤销指定提交
```

**3. 查看历史**

```bash
# 查看提交历史
git log                          # 详细历史
git log --oneline               # 单行显示
git log --graph --oneline --all # 图形化显示所有分支
git log -p                      # 显示每次提交的差异

# 查看文件历史
git log filename                 # 查看文件提交历史
git blame filename               # 查看文件每行的作者和提交

# 查看差异
git diff                        # 工作区与暂存区差异
git diff --staged               # 暂存区与HEAD差异
git diff HEAD                   # 工作区与HEAD差异
git diff commit1 commit2        # 两个提交之间的差异
```

**4. 标签管理**

```bash
# 创建标签
git tag v1.0.0                  # 创建轻量标签
git tag -a v1.0.0 -m "版本1.0.0"  # 创建附注标签（推荐）

# 查看标签
git tag                         # 列出所有标签
git show v1.0.0                 # 查看标签详情

# 推送标签
git push origin v1.0.0         # 推送单个标签
git push origin --tags          # 推送所有标签

# 删除标签
git tag -d v1.0.0              # 删除本地标签
git push origin --delete v1.0.0 # 删除远程标签
```

**5. 交互式Rebase（高级）**

```bash
# 交互式rebase（修改提交历史）
git rebase -i HEAD~3            # 修改最近3个提交

# 在编辑器中可以：
# pick - 保留提交
# reword - 修改提交信息
# edit - 修改提交内容
# squash - 合并到上一个提交
# drop - 删除提交
```

#### 实操任务
- [ ] 练习使用stash暂存和恢复更改
- [ ] 练习撤销和回退操作
- [ ] 创建版本标签
- [ ] 查看提交历史和差异

---

### 任务1.3：GitHub协作流程（1.5小时）

#### 做什么
学习GitHub的协作功能，包括Fork、Pull Request、Issue、Wiki等。

#### 用什么做
- **平台：** GitHub网站
- **功能：** Pull Request, Issue, Wiki, Projects, Actions

#### 怎么做

**1. Fork和Clone**

```bash
# Fork仓库（在GitHub网站操作）
# 1. 点击Fork按钮
# 2. 选择目标账户

# Clone自己的Fork
git clone https://github.com/your-username/repo-name.git
cd repo-name

# 添加上游仓库
git remote add upstream https://github.com/original-owner/repo-name.git
git remote -v                   # 查看远程仓库

# 同步上游更改
git fetch upstream
git merge upstream/main
git push origin main
```

**2. Pull Request流程**

**步骤1：创建功能分支**
```bash
git checkout -b feature/new-feature
```

**步骤2：开发并提交**
```bash
git add .
git commit -m "[Feature] 添加新功能"
git push origin feature/new-feature
```

**步骤3：在GitHub创建PR**
- 在GitHub网站点击"New Pull Request"
- 选择源分支和目标分支
- 填写PR标题和描述
- 添加标签（如`enhancement`, `bug`等）
- 请求代码审查（Request Review）

**步骤4：PR审查和合并**
- 审查者评论和提出建议
- 根据反馈修改代码
- 审查通过后合并PR
- 删除功能分支

**3. Issue管理**

**创建Issue：**
- 标题：清晰描述问题
- 描述：详细说明问题、复现步骤、期望行为
- 标签：bug, enhancement, question等
- 里程碑：关联到项目里程碑
- 分配：分配给负责人

**Issue模板：**
```markdown
## 问题描述
[描述问题]

## 复现步骤
1. 
2. 
3. 

## 期望行为
[描述期望的行为]

## 实际行为
[描述实际的行为]

## 环境信息
- Python版本：
- 操作系统：
```

**4. GitHub Actions（CI/CD）**

创建`.github/workflows/ci.yml`：
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python -m pytest
```

**5. 代码审查要点**

**审查清单：**
- [ ] 代码功能正确
- [ ] 代码风格一致
- [ ] 有适当的注释
- [ ] 没有明显的bug
- [ ] 性能合理
- [ ] 安全性考虑

#### 实操任务
- [ ] Fork一个仓库并同步上游更改
- [ ] 创建功能分支并提交PR
- [ ] 创建Issue并管理
- [ ] 练习代码审查流程

---

## Day 2：爬虫深入学习（4-5小时）

### 任务2.1：动态网页爬取 - Selenium（2小时）

#### 做什么
学习使用Selenium爬取动态网页，处理JavaScript渲染的内容。

#### 用什么做
- **工具库：** 
  - `selenium` - 浏览器自动化
  - `webdriver-manager` - 自动管理驱动
- **安装命令：** `pip install selenium webdriver-manager`

#### 怎么做

**1. Selenium基础**

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 初始化浏览器
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 无头模式（不显示浏览器窗口）
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 访问网页
driver.get('https://example.com')

# 等待元素加载
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "element-id")))

# 查找元素
element = driver.find_element(By.ID, "id")
elements = driver.find_elements(By.CLASS_NAME, "class")
element = driver.find_element(By.XPATH, "//div[@class='example']")

# 操作元素
element.click()                  # 点击
element.send_keys("text")        # 输入文本
text = element.text              # 获取文本
attribute = element.get_attribute("href")  # 获取属性

# 执行JavaScript
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 关闭浏览器
driver.quit()
```

**2. 等待策略**

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 显式等待（推荐）
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "id")))
element = wait.until(EC.element_to_be_clickable((By.ID, "id")))
element = wait.until(EC.visibility_of_element_located((By.ID, "id")))

# 隐式等待
driver.implicitly_wait(10)  # 全局等待10秒

# 固定等待（不推荐，但有时需要）
time.sleep(2)
```

**3. 处理下拉框和弹窗**

```python
from selenium.webdriver.support.ui import Select

# 下拉框
select = Select(driver.find_element(By.ID, "dropdown"))
select.select_by_visible_text("选项文本")
select.select_by_value("value")
select.select_by_index(0)

# 弹窗处理
alert = driver.switch_to.alert
alert.accept()                  # 接受
alert.dismiss()                 # 取消
text = alert.text               # 获取文本
```

**4. 滚动和截图**

```python
# 滚动到元素
element = driver.find_element(By.ID, "id")
driver.execute_script("arguments[0].scrollIntoView();", element)

# 滚动到底部
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 截图
driver.save_screenshot("screenshot.png")
element.screenshot("element.png")
```

**5. 实战案例：爬取动态加载的数据**

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_dynamic_table(url):
    """爬取动态加载的表格数据"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    
    # 等待表格加载
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    
    # 如果数据需要滚动加载，循环滚动
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # 提取数据
    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if cols:
            data.append([col.text for col in cols])
    
    driver.quit()
    return pd.DataFrame(data)
```

#### 实操任务
- [ ] 安装Selenium和webdriver-manager
- [ ] 爬取一个动态网页（如新闻网站、电商网站）
- [ ] 处理下拉框和弹窗
- [ ] 实现滚动加载数据
- [ ] 保存数据为CSV

---

### 任务2.2：API数据获取（1.5小时）

#### 做什么
学习通过API获取数据，包括RESTful API、JSON数据处理等。

#### 用什么做
- **工具库：** `requests`, `json`, `pandas`
- **API示例：** 公开API（如天气API、新闻API等）

#### 怎么做

**1. RESTful API基础**

```python
import requests
import json
import pandas as pd

# GET请求
response = requests.get('https://api.example.com/data')
data = response.json()

# 带参数的GET请求
params = {'key': 'value', 'page': 1}
response = requests.get('https://api.example.com/data', params=params)

# POST请求
data = {'key': 'value'}
response = requests.post('https://api.example.com/data', json=data)

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Authorization': 'Bearer token',
    'Content-Type': 'application/json'
}
response = requests.get('https://api.example.com/data', headers=headers)

# 处理响应
print(response.status_code)      # 状态码
print(response.headers)          # 响应头
print(response.text)             # 文本内容
print(response.json())            # JSON内容
```

**2. 错误处理**

```python
import requests
from requests.exceptions import RequestException

try:
    response = requests.get('https://api.example.com/data', timeout=10)
    response.raise_for_status()  # 如果状态码不是200，抛出异常
    data = response.json()
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.ConnectionError:
    print("连接错误")
except requests.exceptions.HTTPError as e:
    print(f"HTTP错误: {e}")
except RequestException as e:
    print(f"请求错误: {e}")
```

**3. 分页数据获取**

```python
def fetch_all_pages(base_url, params=None):
    """获取所有分页数据"""
    all_data = []
    page = 1
    
    while True:
        if params:
            params['page'] = page
        else:
            params = {'page': page}
        
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            break
        
        data = response.json()
        if not data or len(data) == 0:
            break
        
        all_data.extend(data)
        page += 1
        time.sleep(1)  # 避免请求过快
    
    return all_data
```

**4. 实战案例：获取天气数据**

```python
import requests
import pandas as pd

def get_weather_data(city, api_key):
    """获取天气数据"""
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    weather_info = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'description': data['weather'][0]['description']
    }
    
    return pd.DataFrame([weather_info])
```

**5. 数据存储**

```python
# 保存JSON
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 保存CSV
df = pd.DataFrame(data)
df.to_csv('data.csv', index=False, encoding='utf-8-sig')

# 保存Excel
df.to_excel('data.xlsx', index=False)
```

#### 实操任务
- [ ] 调用一个公开API获取数据
- [ ] 实现分页数据获取
- [ ] 处理API错误和异常
- [ ] 将API数据转换为DataFrame并保存

---

### 任务2.3：反爬虫应对（1小时）

#### 做什么
学习应对常见的反爬虫机制，包括User-Agent、代理、验证码等。

#### 用什么做
- **工具库：** `fake-useragent`, `requests`, `selenium`

#### 怎么做

**1. User-Agent轮换**

```python
from fake_useragent import UserAgent
import requests

ua = UserAgent()

# 随机User-Agent
headers = {
    'User-Agent': ua.random
}
response = requests.get(url, headers=headers)

# 或手动设置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
```

**2. 请求头设置**

```python
headers = {
    'User-Agent': 'Mozilla/5.0...',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Referer': 'https://www.example.com',
    'Cookie': 'session_id=xxx'
}
```

**3. 请求频率控制**

```python
import time
import random

def controlled_request(url, delay_range=(1, 3)):
    """控制请求频率"""
    time.sleep(random.uniform(*delay_range))
    response = requests.get(url)
    return response

# 使用示例
for url in urls:
    response = controlled_request(url)
    # 处理响应
```

**4. 代理使用**

```python
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}

response = requests.get(url, proxies=proxies, timeout=10)

# 代理池
proxy_list = [
    'http://proxy1.com:8080',
    'http://proxy2.com:8080',
]

import random
proxy = random.choice(proxy_list)
response = requests.get(url, proxies={'http': proxy, 'https': proxy})
```

**5. Cookie和Session**

```python
import requests

# 使用Session保持会话
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0...'})

# 登录获取Cookie
login_data = {'username': 'user', 'password': 'pass'}
session.post('https://example.com/login', data=login_data)

# 使用Session访问需要登录的页面
response = session.get('https://example.com/protected')

# 手动设置Cookie
cookies = {'session_id': 'xxx', 'token': 'yyy'}
response = requests.get(url, cookies=cookies)
```

**6. 验证码处理**

```python
# 简单验证码可以使用OCR库
from pytesseract import image_to_string
from PIL import Image

# 下载验证码图片
response = requests.get('https://example.com/captcha')
with open('captcha.png', 'wb') as f:
    f.write(response.content)

# OCR识别
image = Image.open('captcha.png')
captcha_text = image_to_string(image)

# 复杂验证码可能需要：
# 1. 使用打码平台（如超级鹰、图鉴等）
# 2. 机器学习模型识别
# 3. 人工识别（不推荐）
```

#### 实操任务
- [ ] 实现User-Agent轮换
- [ ] 设置完整的请求头
- [ ] 实现请求频率控制
- [ ] 练习使用Session保持登录状态

---

## Day 3-4：高级图像可视化（8-10小时）

### 任务3.1：三维图表可视化（2.5小时）

#### 做什么
学习创建三维柱状图、三维折线图、三维散点图等三维可视化图表。

#### 用什么做
- **工具库：** Matplotlib (`mpl_toolkits.mplot3d`), Plotly
- **关键函数：** `Axes3D`, `plot_surface`, `scatter3D`, `bar3d`

#### 怎么做

**1. 三维柱状图**

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 准备数据
x = np.arange(5)
y = np.arange(4)
xpos, ypos = np.meshgrid(x, y)
xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros_like(xpos)

# 柱子的高度和宽度
dx = dy = 0.8
dz = np.random.rand(20)  # 随机高度

# 创建3D图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制3D柱状图
colors = plt.cm.viridis(dz / dz.max())
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, alpha=0.8)

# 设置标签和标题
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.set_zlabel('Z轴（高度）')
ax.set_title('三维柱状图', fontsize=14, fontweight='bold')

# 设置视角
ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.savefig('3d_bar_chart.png', dpi=300, bbox_inches='tight')
plt.show()
```

**2. 三维折线图**

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 准备数据
t = np.linspace(0, 4*np.pi, 100)
x = np.sin(t)
y = np.cos(t)
z = t

# 创建3D图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制3D折线图
ax.plot(x, y, z, linewidth=2, color='blue', label='3D曲线')

# 添加散点标记关键点
key_points = [0, 25, 50, 75, 99]
ax.scatter(x[key_points], y[key_points], z[key_points], 
           c='red', s=100, marker='o', label='关键点')

# 设置标签和标题
ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_zlabel('Z轴（时间）', fontsize=12)
ax.set_title('三维折线图', fontsize=14, fontweight='bold')
ax.legend()

# 设置视角
ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.savefig('3d_line_chart.png', dpi=300, bbox_inches='tight')
plt.show()
```

**3. 三维散点图**

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 准备数据
np.random.seed(42)
n = 100
x = np.random.randn(n)
y = np.random.randn(n)
z = np.random.randn(n)
colors = np.random.rand(n)
sizes = 100 * np.random.rand(n)

# 创建3D图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制3D散点图
scatter = ax.scatter(x, y, z, c=colors, s=sizes, 
                     alpha=0.6, cmap='viridis', edgecolors='black', linewidth=0.5)

# 添加颜色条
cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label('颜色值', fontsize=12)

# 设置标签和标题
ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_zlabel('Z轴', fontsize=12)
ax.set_title('三维散点图', fontsize=14, fontweight='bold')

# 设置视角
ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.savefig('3d_scatter_chart.png', dpi=300, bbox_inches='tight')
plt.show()
```

**4. 三维曲面图**

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 准备数据
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# 创建3D图形
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# 绘制3D曲面图
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9, 
                       linewidth=0, antialiased=True)

# 添加等高线投影
contour = ax.contour(X, Y, Z, zdir='z', offset=Z.min(), cmap='viridis', alpha=0.5)

# 添加颜色条
fig.colorbar(surf, ax=ax, pad=0.1, shrink=0.8)

# 设置标签和标题
ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_zlabel('Z轴', fontsize=12)
ax.set_title('三维曲面图', fontsize=14, fontweight='bold')

# 设置视角
ax.view_init(elev=30, azim=45)

plt.tight_layout()
plt.savefig('3d_surface_chart.png', dpi=300, bbox_inches='tight')
plt.show()
```

#### 实操任务
- [ ] 创建三维柱状图（展示多维度数据）
- [ ] 创建三维折线图（展示时间序列）
- [ ] 创建三维散点图（展示多变量关系）
- [ ] 创建三维曲面图（展示函数关系）

---

### 任务3.2：阶梯图和局部放大图（2小时）

#### 做什么
学习创建阶梯图（Step Plot）和带局部放大功能的图表。

#### 用什么做
- **工具库：** Matplotlib, `mpl_toolkits.axes_grid1`
- **关键函数：** `plt.step()`, `inset_axes()`

#### 怎么做

**1. 阶梯图**

```python
import matplotlib.pyplot as plt
import numpy as np

# 准备数据
x = np.linspace(0, 10, 20)
y = np.sin(x) + np.random.normal(0, 0.1, len(x))

# 创建图形
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. 默认阶梯图（post）
axes[0, 0].step(x, y, where='post', linewidth=2, label='post')
axes[0, 0].plot(x, y, 'o--', alpha=0.5, label='原始数据')
axes[0, 0].set_title('阶梯图 (where="post")', fontsize=12, fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. pre阶梯图
axes[0, 1].step(x, y, where='pre', linewidth=2, color='green', label='pre')
axes[0, 1].plot(x, y, 'o--', alpha=0.5, label='原始数据')
axes[0, 1].set_title('阶梯图 (where="pre")', fontsize=12, fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 3. mid阶梯图
axes[1, 0].step(x, y, where='mid', linewidth=2, color='red', label='mid')
axes[1, 0].plot(x, y, 'o--', alpha=0.5, label='原始数据')
axes[1, 0].set_title('阶梯图 (where="mid")', fontsize=12, fontweight='bold')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# 4. 填充阶梯图
axes[1, 1].step(x, y, where='post', linewidth=2, color='purple')
axes[1, 1].fill_between(x, 0, y, step='post', alpha=0.3, color='purple')
axes[1, 1].set_title('填充阶梯图', fontsize=12, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('step_plots.png', dpi=300, bbox_inches='tight')
plt.show()
```

**2. 局部放大图（使用inset_axes）**

```python
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
import numpy as np

# 准备数据
x = np.linspace(0, 10, 1000)
y = np.sin(x) + 0.1 * np.random.randn(len(x))

# 创建主图
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(x, y, linewidth=1.5, color='blue', label='完整数据')
ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_title('带局部放大图的折线图', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()

# 定义放大区域
x1, x2 = 2, 4  # 放大区域范围
y1, y2 = -0.5, 0.5

# 创建局部放大图
axins = inset_axes(ax, width="40%", height="30%", loc='upper right',
                   bbox_to_anchor=(0.5, 0.5, 1, 1), bbox_transform=ax.transAxes)

# 在放大图中绘制数据
axins.plot(x, y, linewidth=1.5, color='red')
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xlabel('X (放大)', fontsize=10)
axins.set_ylabel('Y (放大)', fontsize=10)
axins.grid(True, alpha=0.3)

# 标记放大区域
mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5", linestyle='--')

# 在主图上标记放大区域
ax.axvspan(x1, x2, alpha=0.2, color='yellow', label='放大区域')
ax.legend()

plt.tight_layout()
plt.savefig('inset_plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

**3. 多个局部放大图**

```python
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
import numpy as np

# 准备数据
x = np.linspace(0, 10, 1000)
y = np.sin(x) * np.exp(-x/5) + 0.1 * np.random.randn(len(x))

# 创建主图
fig, ax = plt.subplots(figsize=(14, 8))
ax.plot(x, y, linewidth=2, color='blue', label='完整数据')
ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_title('多个局部放大图', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()

# 创建第一个局部放大图（左上角）
axins1 = inset_axes(ax, width="30%", height="25%", loc='upper left')
axins1.plot(x, y, linewidth=1.5, color='red')
axins1.set_xlim(0, 2)
axins1.set_ylim(-0.5, 1.5)
axins1.set_title('区域1', fontsize=9)
axins1.grid(True, alpha=0.3)
mark_inset(ax, axins1, loc1=2, loc2=4, fc="none", ec="0.5")

# 创建第二个局部放大图（右上角）
axins2 = inset_axes(ax, width="30%", height="25%", loc='upper right')
axins2.plot(x, y, linewidth=1.5, color='green')
axins2.set_xlim(4, 6)
axins2.set_ylim(-0.3, 0.3)
axins2.set_title('区域2', fontsize=9)
axins2.grid(True, alpha=0.3)
mark_inset(ax, axins2, loc1=1, loc2=3, fc="none", ec="0.5")

plt.tight_layout()
plt.savefig('multiple_inset_plots.png', dpi=300, bbox_inches='tight')
plt.show()
```

#### 实操任务
- [ ] 创建阶梯图（展示离散数据变化）
- [ ] 创建带局部放大的折线图
- [ ] 创建多个局部放大图
- [ ] 结合阶梯图和局部放大功能

---

### 任务3.3：多色填充和桑基图（3.5小时）

#### 做什么
学习创建多色填充图表和桑基图（Sankey Diagram），用于展示数据流动和关系。

#### 用什么做
- **工具库：** Matplotlib, Plotly (用于桑基图), `matplotlib.patches`
- **关键函数：** `fill_between()`, `plotly.graph_objects.Sankey`

#### 怎么做

**1. 多色填充图**

```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# 准备数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.cos(x)

# 创建图形
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. 基础多色填充
ax = axes[0, 0]
ax.fill_between(x, 0, y1, alpha=0.5, color='blue', label='sin(x)')
ax.fill_between(x, 0, y2, alpha=0.5, color='red', label='cos(x)')
ax.plot(x, y1, 'b-', linewidth=2)
ax.plot(x, y2, 'r-', linewidth=2)
ax.set_title('基础多色填充', fontsize=12, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# 2. 条件填充
ax = axes[0, 1]
ax.fill_between(x, y1, y2, where=(y1 > y2), alpha=0.5, color='green', label='y1 > y2')
ax.fill_between(x, y1, y2, where=(y1 <= y2), alpha=0.5, color='orange', label='y1 <= y2')
ax.plot(x, y1, 'b-', linewidth=2, label='y1')
ax.plot(x, y2, 'r-', linewidth=2, label='y2')
ax.set_title('条件多色填充', fontsize=12, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# 3. 渐变填充
ax = axes[1, 0]
for i in range(len(x)-1):
    ax.fill_between([x[i], x[i+1]], 0, y1[i:i+2], 
                     color=plt.cm.viridis(i/len(x)), alpha=0.7)
ax.plot(x, y1, 'k-', linewidth=2)
ax.set_title('渐变填充', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)

# 4. 堆叠多色填充
ax = axes[1, 1]
ax.fill_between(x, 0, y1, alpha=0.6, color='blue', label='sin(x)')
ax.fill_between(x, y1, y1+y2, alpha=0.6, color='red', label='cos(x)')
ax.fill_between(x, y1+y2, y1+y2+y3, alpha=0.6, color='green', label='sin(x)*cos(x)')
ax.plot(x, y1, 'b-', linewidth=1)
ax.plot(x, y1+y2, 'r-', linewidth=1)
ax.plot(x, y1+y2+y3, 'g-', linewidth=1)
ax.set_title('堆叠多色填充', fontsize=12, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('multicolor_fill.png', dpi=300, bbox_inches='tight')
plt.show()
```

**2. 桑基图（使用Plotly）**

```python
import plotly.graph_objects as go

# 准备数据：定义节点和连接
# 节点标签
labels = ['源1', '源2', '源3', '中间1', '中间2', '目标1', '目标2', '目标3']

# 源节点索引
source = [0, 0, 1, 1, 2, 3, 3, 4, 4]
# 目标节点索引
target = [3, 4, 3, 4, 4, 5, 6, 6, 7]
# 流量值
value = [8, 4, 2, 2, 6, 4, 6, 2, 8]

# 节点颜色
node_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
               '#F7DC6F', '#BB8FCE', '#85C1E2']

# 创建桑基图
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=node_colors
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=['rgba(255,0,0,0.4)' if i < 3 else 'rgba(0,255,0,0.4)' 
               for i in range(len(source))]
    )
)])

fig.update_layout(
    title_text="桑基图示例：数据流动可视化",
    font_size=14,
    width=1000,
    height=600
)

fig.write_image("sankey_diagram.png", width=1000, height=600, scale=3)
fig.show()
```

**3. 复杂桑基图（多层级）**

```python
import plotly.graph_objects as go

# 定义更复杂的节点和连接
labels = [
    # 第一层：能源来源
    '煤炭', '石油', '天然气', '核能', '可再生能源',
    # 第二层：转换过程
    '发电', '工业', '交通', '建筑',
    # 第三层：最终用途
    '电力', '热力', '动力'
]

# 定义连接
source = [
    # 能源来源 -> 转换过程
    0, 0, 0,  # 煤炭 -> 发电、工业、建筑
    1, 1,     # 石油 -> 工业、交通
    2, 2, 2,  # 天然气 -> 发电、工业、建筑
    3,        # 核能 -> 发电
    4, 4,     # 可再生能源 -> 发电、建筑
    # 转换过程 -> 最终用途
    5, 5,     # 发电 -> 电力、热力
    6, 6,     # 工业 -> 电力、热力
    7,        # 交通 -> 动力
    8, 8      # 建筑 -> 电力、热力
]

target = [
    # 能源来源 -> 转换过程
    5, 6, 8,
    6, 7,
    5, 6, 8,
    5,
    5, 8,
    # 转换过程 -> 最终用途
    9, 10,
    9, 10,
    11,
    9, 10
]

value = [
    # 能源来源 -> 转换过程
    30, 20, 10,
    15, 25,
    20, 15, 10,
    15,
    10, 5,
    # 转换过程 -> 最终用途
    50, 20,
    30, 20,
    25,
    15, 10
]

# 节点颜色（按层级）
node_colors = [
    '#FF6B6B', '#FF8E53', '#FFA07A', '#FFB347', '#FFD700',  # 能源来源
    '#4ECDC4', '#45B7D1', '#87CEEB', '#98D8C8',              # 转换过程
    '#90EE90', '#98FB98', '#ADFF2F'                          # 最终用途
]

# 创建桑基图
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=25,
        line=dict(color="black", width=1),
        label=labels,
        color=node_colors
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color='rgba(0,0,255,0.3)'
    )
)])

fig.update_layout(
    title_text="能源流动桑基图（多层级）",
    font_size=12,
    width=1200,
    height=700
)

fig.write_image("complex_sankey.png", width=1200, height=700, scale=3)
fig.show()
```

**4. 使用matplotlib创建简单桑基图**

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def draw_simple_sankey(flows, labels, colors=None):
    """绘制简单的桑基图"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    if colors is None:
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    
    # 计算节点位置
    n_nodes = len(labels)
    node_y = np.linspace(0.1, 0.9, n_nodes)
    
    # 绘制节点
    for i, (label, y, color) in enumerate(zip(labels, node_y, colors)):
        # 左侧节点
        rect_left = mpatches.Rectangle((0.1, y-0.03), 0.1, 0.06, 
                                       facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(rect_left)
        ax.text(0.05, y, label, ha='right', va='center', fontsize=10, fontweight='bold')
        
        # 右侧节点
        rect_right = mpatches.Rectangle((0.8, y-0.03), 0.1, 0.06, 
                                        facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(rect_right)
    
    # 绘制连接（简化版）
    # 这里只是示例，实际桑基图需要更复杂的计算
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('简化桑基图', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('simple_sankey.png', dpi=300, bbox_inches='tight')
    plt.show()

# 使用示例
flows = [10, 20, 15]
labels = ['源1', '源2', '源3']
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
draw_simple_sankey(flows, labels, colors)
```

#### 实操任务
- [ ] 创建多色填充图（条件填充、渐变填充、堆叠填充）
- [ ] 使用Plotly创建桑基图
- [ ] 创建多层级桑基图
- [ ] 将桑基图应用到实际数据（如能源流动、资金流动等）

---

## ✅ 第三阶段完成标准

完成以下所有任务即可进入下一阶段：

### Git/GitHub能力
- [ ] 熟练掌握分支管理（创建、合并、删除）
- [ ] 能够解决合并冲突
- [ ] 掌握Git高级操作（stash、reset、revert、tag）
- [ ] 能够使用Pull Request进行协作
- [ ] 能够管理Issue和代码审查

### 爬虫能力
- [ ] 能够使用Selenium爬取动态网页
- [ ] 能够通过API获取数据
- [ ] 能够处理反爬虫机制（User-Agent、代理、频率控制）
- [ ] 能够处理登录和Session
- [ ] 完成至少2个爬虫项目

### 高级可视化能力
- [ ] 能够创建三维柱状图
- [ ] 能够创建三维折线图
- [ ] 能够创建三维散点图
- [ ] 能够创建三维曲面图
- [ ] 能够创建阶梯图
- [ ] 能够创建局部放大图
- [ ] 能够创建多色填充图
- [ ] 能够创建桑基图

### 项目完成度
- [ ] 完成Git/GitHub协作项目
- [ ] 完成至少2个爬虫项目
- [ ] 完成高级可视化项目（包含所有要求的图表类型）
- [ ] 所有代码规范，有注释
- [ ] 所有项目有说明文档

---

## 📚 学习资源

### Git/GitHub
1. **Pro Git Book** - https://git-scm.com/book
2. **GitHub官方指南** - https://guides.github.com
3. **Learn Git Branching** - https://learngitbranching.js.org
4. **B站：Git/GitHub教程**

### 爬虫
1. **Selenium官方文档** - https://www.selenium.dev/documentation
2. **BeautifulSoup文档** - https://www.crummy.com/software/BeautifulSoup/bs4/doc/
3. **Requests文档** - https://requests.readthedocs.io
4. **B站：Python爬虫教程**

### 高级可视化
1. **Matplotlib 3D教程** - https://matplotlib.org/stable/tutorials/toolkits/mplot3d.html
2. **Plotly文档** - https://plotly.com/python/
3. **Seaborn文档** - https://seaborn.pydata.org
4. **B站：Python数据可视化高级教程**

---

## 💡 学习建议

1. **循序渐进**：先掌握基础，再学习高级功能
2. **实践为主**：多写代码，多练习
3. **查阅文档**：遇到问题先查官方文档
4. **代码规范**：保持代码整洁，添加注释
5. **版本控制**：使用Git管理代码，养成提交习惯
6. **协作交流**：通过GitHub与他人协作，学习最佳实践

