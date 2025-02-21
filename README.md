

###  部署项目
1. **克隆本仓库**  
   ```bash
   git clone <仓库地址>
2. **安装依赖**  
   ```bash
   pip install -r requirements.txt
3. **配置<code>config.py</code>**  
修改<code>LISTEN_LIST</code>、<code>DEEPSEEK_BASE_URL</code>和<code>DEEPSEEK_API_KEY</code>。
按需调整<code>MAX_TOKEN</code>、<code>TEMPERATURE</code>和<code>MODEL</code>等
4. **运行<code>deepseek to wechat.py</code>，如果报错请尝试使用Python 3.11版本。**
   ```bash
   python deepseek to wechat.py

### 如何使用
- **项目运行后，控制台提示**
     ```bash
   开始运行
即可开始监听并调用模型自动回复消息。
## 如果您想修改prompt
- 项目根目录下的 <code>prompt.md</code> 可以编辑，修改后重启项目生效。
- 注意：请不要修改与反斜线 <code> \ </code>相关的 prompt，因为它们被用于分段回复消息。

