# 项目结构说明 (Project Structure)

```
finace/
├── stock_monitor.py        # 主程序文件 (核心监控系统)
├── config.json            # 配置文件 (自选股和参数设置)
├── requirements.txt       # Python依赖包列表
├── demo.py                # 快速演示脚本 (单次扫描)
├── examples.py            # 完整示例程序 (多种用法演示)
├── test_stock_monitor.py  # 测试脚本 (功能测试)
├── README.md              # 完整文档 (详细说明)
├── QUICKSTART.md          # 快速开始指南 (5分钟上手)
├── .gitignore            # Git忽略文件
└── program               # (原有文件，已保留)
```

## 核心文件说明

### 1. stock_monitor.py (主程序, ~600行)

**核心类:**
- `StockAnalyzer`: 技术分析引擎
  - 计算MA、RSI、MACD、KDJ等指标
  - 综合分析买卖信号
  - 生成交易建议

- `TongHuaShunAPI`: API接口封装
  - 获取实时股价
  - 获取盘面信息
  - 获取新闻资讯
  - 获取历史数据

- `StockMonitor`: 监控主控制器
  - 定时扫描自选股
  - 检查提醒条件
  - 触发弹窗提醒
  - 管理监控循环

- `StockMonitorGUI`: 图形界面 (可选)
  - 提供友好的GUI界面
  - 实时日志显示
  - 启动/停止控制

**特性:**
- ✅ 支持GUI和CLI两种模式
- ✅ 多线程异步监控
- ✅ 智能弹窗提醒
- ✅ 完整技术分析
- ✅ 可配置化设计

### 2. config.json (配置文件)

```json
{
  "watchlist": ["600000", "000001", ...],    // 自选股列表
  "scan_interval": 60,                       // 扫描间隔(秒)
  "alert_conditions": {
    "price_change_threshold": 3.0,           // 价格异动阈值(%)
    "volume_threshold": 200,                 // 成交量阈值(%)
    "buy_signal_threshold": 5,               // 买入信号阈值
    "sell_signal_threshold": -5              // 卖出信号阈值
  },
  "technical_analysis": {
    "enable_ma": true,                       // 启用均线分析
    "enable_rsi": true,                      // 启用RSI分析
    "enable_macd": true,                     // 启用MACD分析
    "enable_kdj": true                       // 启用KDJ分析
  }
}
```

### 3. demo.py (快速演示)

简化的演示脚本，执行一次扫描后退出。适合：
- 快速测试程序是否正常
- 查看监控输出格式
- 验证配置是否正确

**使用:**
```bash
python demo.py
```

### 4. examples.py (完整示例)

包含多个使用示例：
1. 基本监控示例
2. 自定义配置示例
3. 技术分析演示
4. API使用演示

**使用:**
```bash
python examples.py
```

### 5. test_stock_monitor.py (测试脚本)

全面的功能测试，包括：
- ✅ 技术分析模块测试
- ✅ API接口测试
- ✅ 监控功能测试
- ✅ 所有指标计算验证

**使用:**
```bash
python test_stock_monitor.py
```

## 使用流程

### 新手推荐流程

```
1. 安装依赖
   └─> pip install -r requirements.txt

2. 快速测试
   └─> python demo.py
   
3. 查看示例
   └─> python examples.py
   
4. 配置自选股
   └─> 编辑 config.json
   
5. 启动监控
   └─> python stock_monitor.py (GUI)
   └─> python stock_monitor.py --cli (CLI)
```

### 开发者流程

```
1. 阅读源码
   └─> stock_monitor.py
   
2. 运行测试
   └─> python test_stock_monitor.py
   
3. 修改API
   └─> 编辑 TongHuaShunAPI 类
   
4. 自定义分析
   └─> 编辑 StockAnalyzer 类
   
5. 测试验证
   └─> python demo.py
```

## 技术栈

- **语言**: Python 3.8+
- **核心库**: 
  - `requests` - HTTP请求
  - `tkinter` - GUI界面 (可选)
  - `threading` - 多线程支持
  - `json` - 配置管理

## 扩展性

### 添加新的技术指标

在 `StockAnalyzer` 类中添加新方法：

```python
def calculate_new_indicator(self, prices: List[float]) -> float:
    # 实现新指标
    return result
```

### 添加新的提醒渠道

在 `StockMonitor` 类中修改 `show_alert` 方法：

```python
def show_alert(self, ...):
    # 原有弹窗提醒
    ...
    # 添加其他提醒方式
    # 例如: 发送邮件、微信通知等
```

### 接入真实API

修改 `TongHuaShunAPI` 类：

```python
class TongHuaShunAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.10jqka.com.cn"
        # 替换为真实API调用
```

## 性能优化

- 使用线程池并发获取多只股票数据
- 缓存历史数据减少API调用
- 异步处理提醒通知
- 数据库存储历史记录

## 安全考虑

- ✅ 无硬编码敏感信息
- ✅ 配置文件外部化
- ✅ 异常处理完善
- ✅ CodeQL安全扫描通过

## 维护建议

1. **定期更新依赖**: `pip install --upgrade -r requirements.txt`
2. **备份配置文件**: 定期备份 `config.json`
3. **查看日志**: 监控程序运行日志
4. **测试验证**: 修改后运行测试脚本

## 故障排查

### 问题1: 无法启动GUI

**解决**: 安装tkinter或使用CLI模式
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# 或使用CLI模式
python stock_monitor.py --cli
```

### 问题2: API返回错误

**解决**: 检查网络连接和API配置
- 确认网络正常
- 检查API密钥是否有效
- 查看错误日志

### 问题3: 提醒不弹出

**解决**: 检查提醒条件设置
- 降低 `price_change_threshold`
- 调整信号阈值
- 确认监控已启动

## 贡献指南

欢迎提交PR改进项目！提交前请：
1. 运行测试确保通过
2. 遵循现有代码风格
3. 添加必要的文档
4. 说明改动原因

## 许可证

本项目仅供学习交流使用。

## 免责声明

⚠️ 本程序仅供学习研究使用，不构成任何投资建议。使用本软件进行投资决策的风险由使用者自行承担。
