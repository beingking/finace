#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票监控程序 - 基于同花顺API
实时监控自选股的价格、盘面信息、新闻，并分析买卖点
"""

import time
import json
import requests
from datetime import datetime
from typing import List, Dict, Any
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
import sys


class StockAnalyzer:
    """股票技术分析类"""
    
    def __init__(self):
        pass
    
    def calculate_ma(self, prices: List[float], period: int = 5) -> float:
        """计算移动平均线"""
        if len(prices) < period:
            return 0
        return sum(prices[-period:]) / period
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """计算相对强弱指标RSI"""
        if len(prices) < period + 1:
            return 50
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            diff = prices[i] - prices[i-1]
            if diff > 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(diff))
        
        if len(gains) < period:
            return 50
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices: List[float]) -> Dict[str, float]:
        """计算MACD指标"""
        if len(prices) < 26:
            return {'macd': 0, 'signal': 0, 'histogram': 0}
        
        ema_12 = self._calculate_ema(prices, 12)
        ema_26 = self._calculate_ema(prices, 26)
        macd_line = ema_12 - ema_26
        
        # 简化版本，实际应计算MACD的EMA
        signal_line = macd_line * 0.9
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def _calculate_ema(self, prices: List[float], period: int) -> float:
        """计算指数移动平均"""
        if len(prices) < period:
            return prices[-1] if prices else 0
        
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        
        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema
        
        return ema
    
    def calculate_kdj(self, highs: List[float], lows: List[float], closes: List[float], period: int = 9) -> Dict[str, float]:
        """计算KDJ指标"""
        if len(closes) < period:
            return {'k': 50, 'd': 50, 'j': 50}
        
        lowest_low = min(lows[-period:])
        highest_high = max(highs[-period:])
        
        if highest_high == lowest_low:
            rsv = 50
        else:
            rsv = (closes[-1] - lowest_low) / (highest_high - lowest_low) * 100
        
        # 简化计算
        k = rsv * 0.67 + 33
        d = k * 0.67 + 33
        j = 3 * k - 2 * d
        
        return {'k': k, 'd': d, 'j': j}
    
    def analyze_buy_sell_signals(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """综合分析买卖信号"""
        signals = {
            'buy_signals': [],
            'sell_signals': [],
            'score': 0,
            'recommendation': 'HOLD'
        }
        
        prices = stock_data.get('prices', [])
        if len(prices) < 30:
            return signals
        
        # MA分析
        ma5 = self.calculate_ma(prices, 5)
        ma10 = self.calculate_ma(prices, 10)
        ma20 = self.calculate_ma(prices, 20)
        current_price = prices[-1]
        
        if ma5 > ma10 > ma20 and current_price > ma5:
            signals['buy_signals'].append('均线多头排列')
            signals['score'] += 2
        elif ma5 < ma10 < ma20 and current_price < ma5:
            signals['sell_signals'].append('均线空头排列')
            signals['score'] -= 2
        
        # RSI分析
        rsi = self.calculate_rsi(prices)
        if rsi < 30:
            signals['buy_signals'].append(f'RSI超卖({rsi:.2f})')
            signals['score'] += 3
        elif rsi > 70:
            signals['sell_signals'].append(f'RSI超买({rsi:.2f})')
            signals['score'] -= 3
        
        # MACD分析
        macd = self.calculate_macd(prices)
        if macd['histogram'] > 0 and macd['macd'] > macd['signal']:
            signals['buy_signals'].append('MACD金叉')
            signals['score'] += 2
        elif macd['histogram'] < 0 and macd['macd'] < macd['signal']:
            signals['sell_signals'].append('MACD死叉')
            signals['score'] -= 2
        
        # KDJ分析（需要高低价数据）
        highs = stock_data.get('highs', prices)
        lows = stock_data.get('lows', prices)
        kdj = self.calculate_kdj(highs, lows, prices)
        
        if kdj['j'] < 20:
            signals['buy_signals'].append(f'KDJ超卖(J={kdj["j"]:.2f})')
            signals['score'] += 2
        elif kdj['j'] > 80:
            signals['sell_signals'].append(f'KDJ超买(J={kdj["j"]:.2f})')
            signals['score'] -= 2
        
        # 综合建议
        if signals['score'] >= 5:
            signals['recommendation'] = 'STRONG BUY'
        elif signals['score'] >= 2:
            signals['recommendation'] = 'BUY'
        elif signals['score'] <= -5:
            signals['recommendation'] = 'STRONG SELL'
        elif signals['score'] <= -2:
            signals['recommendation'] = 'SELL'
        else:
            signals['recommendation'] = 'HOLD'
        
        return signals


class TongHuaShunAPI:
    """同花顺API接口类"""
    
    def __init__(self):
        # 注意：这里使用模拟数据，实际使用需要真实的同花顺API密钥
        self.base_url = "http://api.mock.com"  # 模拟API地址
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_realtime_price(self, stock_code: str) -> Dict[str, Any]:
        """获取实时股价"""
        # 模拟数据
        import random
        base_price = 10.0 + random.random() * 90
        
        return {
            'code': stock_code,
            'name': f'股票{stock_code}',
            'price': base_price,
            'change': random.uniform(-5, 5),
            'change_percent': random.uniform(-10, 10),
            'volume': random.randint(1000000, 100000000),
            'turnover': base_price * random.randint(1000000, 100000000),
            'high': base_price * 1.05,
            'low': base_price * 0.95,
            'open': base_price * 0.98,
            'prev_close': base_price * 0.97,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_market_info(self, stock_code: str) -> Dict[str, Any]:
        """获取盘面信息"""
        return {
            'code': stock_code,
            'pe_ratio': 15.5,
            'pb_ratio': 2.3,
            'market_cap': 1000000000,
            'circulation_market_cap': 800000000,
            'total_shares': 100000000,
            'circulation_shares': 80000000,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_news(self, stock_code: str, limit: int = 5) -> List[Dict[str, str]]:
        """获取股票新闻"""
        # 模拟新闻数据
        news_list = []
        for i in range(limit):
            news_list.append({
                'title': f'股票{stock_code}相关新闻标题{i+1}',
                'content': '这是新闻内容摘要...',
                'source': '财经网',
                'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'url': f'http://news.example.com/{stock_code}/{i}'
            })
        return news_list
    
    def get_historical_prices(self, stock_code: str, days: int = 30) -> List[float]:
        """获取历史价格数据"""
        import random
        base_price = 10.0 + random.random() * 90
        prices = []
        for i in range(days):
            price = base_price * (1 + random.uniform(-0.05, 0.05))
            prices.append(price)
            base_price = price
        return prices


class StockMonitor:
    """股票监控主类"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config = self.load_config(config_file)
        self.api = TongHuaShunAPI()
        self.analyzer = StockAnalyzer()
        self.running = False
        self.monitor_thread = None
        self.alert_window = None
        
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            'watchlist': ['600000', '000001', '000002'],  # 自选股列表
            'scan_interval': 60,  # 扫描间隔（秒）
            'alert_conditions': {
                'price_change_threshold': 3.0,  # 价格变动阈值(%)
                'volume_threshold': 200,  # 成交量阈值（%）
                'buy_signal_threshold': 5,  # 买入信号阈值
                'sell_signal_threshold': -5  # 卖出信号阈值
            },
            'technical_analysis': {
                'enable_ma': True,
                'enable_rsi': True,
                'enable_macd': True,
                'enable_kdj': True
            }
        }
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合并默认配置
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except FileNotFoundError:
            print(f"配置文件 {config_file} 不存在，使用默认配置")
            # 创建默认配置文件
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            return default_config
    
    def scan_stocks(self):
        """扫描股票"""
        print(f"\n{'='*60}")
        print(f"开始扫描 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        for stock_code in self.config['watchlist']:
            try:
                # 获取实时数据
                price_data = self.api.get_realtime_price(stock_code)
                market_info = self.api.get_market_info(stock_code)
                news = self.api.get_news(stock_code, limit=3)
                
                # 获取历史数据用于技术分析
                historical_prices = self.api.get_historical_prices(stock_code, days=30)
                
                # 构建分析数据
                stock_data = {
                    'prices': historical_prices,
                    'highs': [p * 1.02 for p in historical_prices],
                    'lows': [p * 0.98 for p in historical_prices]
                }
                
                # 技术分析
                signals = self.analyzer.analyze_buy_sell_signals(stock_data)
                
                # 显示信息
                self.display_stock_info(price_data, market_info, signals, news)
                
                # 检查是否需要弹窗提醒
                self.check_alert_conditions(price_data, signals, news)
                
            except Exception as e:
                print(f"扫描股票 {stock_code} 时出错: {str(e)}")
        
        print(f"{'='*60}\n")
    
    def display_stock_info(self, price_data: Dict, market_info: Dict, signals: Dict, news: List[Dict]):
        """显示股票信息"""
        print(f"\n【{price_data['name']} ({price_data['code']})】")
        print(f"当前价: {price_data['price']:.2f}  "
              f"涨跌: {price_data['change']:+.2f} ({price_data['change_percent']:+.2f}%)")
        print(f"成交量: {price_data['volume']:,}  "
              f"成交额: {price_data['turnover']:,.2f}")
        print(f"今开: {price_data['open']:.2f}  "
              f"最高: {price_data['high']:.2f}  "
              f"最低: {price_data['low']:.2f}")
        
        print(f"\n技术分析:")
        print(f"  建议: {signals['recommendation']} (评分: {signals['score']})")
        if signals['buy_signals']:
            print(f"  买入信号: {', '.join(signals['buy_signals'])}")
        if signals['sell_signals']:
            print(f"  卖出信号: {', '.join(signals['sell_signals'])}")
        
        print(f"\n最新新闻:")
        for i, item in enumerate(news[:3], 1):
            print(f"  {i}. {item['title']} ({item['source']})")
    
    def check_alert_conditions(self, price_data: Dict, signals: Dict, news: List[Dict]):
        """检查是否满足弹窗提醒条件"""
        alerts = []
        
        # 检查价格变动
        threshold = self.config['alert_conditions']['price_change_threshold']
        if abs(price_data['change_percent']) >= threshold:
            alerts.append(f"价格异动: {price_data['change_percent']:+.2f}%")
        
        # 检查买卖信号
        buy_threshold = self.config['alert_conditions']['buy_signal_threshold']
        sell_threshold = self.config['alert_conditions']['sell_signal_threshold']
        
        if signals['score'] >= buy_threshold:
            alerts.append(f"强烈买入信号! 评分: {signals['score']}")
            alerts.extend([f"  - {sig}" for sig in signals['buy_signals']])
        elif signals['score'] <= sell_threshold:
            alerts.append(f"强烈卖出信号! 评分: {signals['score']}")
            alerts.extend([f"  - {sig}" for sig in signals['sell_signals']])
        
        # 如果有重要新闻（这里简化处理，实际应分析新闻重要性）
        if any('重大' in item['title'] or '公告' in item['title'] for item in news):
            alerts.append("发现重要新闻!")
        
        # 如果有提醒，显示弹窗
        if alerts:
            self.show_alert(price_data['name'], price_data['code'], alerts)
    
    def show_alert(self, stock_name: str, stock_code: str, alerts: List[str]):
        """显示弹窗提醒"""
        alert_msg = f"【{stock_name} ({stock_code})】\n\n" + "\n".join(alerts)
        print(f"\n!!! 提醒 !!!\n{alert_msg}\n")
        
        # 在主线程中显示弹窗
        try:
            if self.alert_window and self.alert_window.winfo_exists():
                self.alert_window.lift()
            else:
                self.create_alert_window(stock_name, stock_code, alerts)
        except:
            pass
    
    def create_alert_window(self, stock_name: str, stock_code: str, alerts: List[str]):
        """创建提醒窗口"""
        try:
            window = tk.Toplevel()
            window.title(f"股票提醒 - {stock_name}")
            window.geometry("500x300")
            
            # 标题
            title_label = tk.Label(window, 
                                  text=f"{stock_name} ({stock_code})",
                                  font=('Arial', 14, 'bold'),
                                  fg='red')
            title_label.pack(pady=10)
            
            # 提醒内容
            text_area = scrolledtext.ScrolledText(window, 
                                                  width=60, 
                                                  height=12,
                                                  font=('Arial', 10))
            text_area.pack(padx=10, pady=5)
            text_area.insert('1.0', '\n'.join(alerts))
            text_area.config(state='disabled')
            
            # 关闭按钮
            close_btn = tk.Button(window, 
                                 text="知道了",
                                 command=window.destroy,
                                 width=20)
            close_btn.pack(pady=10)
            
            # 置顶显示
            window.lift()
            window.attributes('-topmost', True)
            
            self.alert_window = window
        except Exception as e:
            print(f"创建提醒窗口失败: {str(e)}")
    
    def monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                self.scan_stocks()
                time.sleep(self.config['scan_interval'])
            except Exception as e:
                print(f"监控循环出错: {str(e)}")
                time.sleep(10)
    
    def start(self):
        """启动监控"""
        if self.running:
            print("监控已在运行中")
            return
        
        print("启动股票监控程序...")
        print(f"监控股票: {', '.join(self.config['watchlist'])}")
        print(f"扫描间隔: {self.config['scan_interval']} 秒")
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        print("监控已启动!")
    
    def stop(self):
        """停止监控"""
        print("停止监控...")
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("监控已停止")


class StockMonitorGUI:
    """股票监控图形界面"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("股票监控系统")
        self.root.geometry("800x600")
        
        self.monitor = StockMonitor()
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        # 控制面板
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.start_btn = tk.Button(control_frame, 
                                   text="启动监控",
                                   command=self.start_monitoring,
                                   width=15,
                                   bg='green',
                                   fg='white')
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(control_frame,
                                  text="停止监控",
                                  command=self.stop_monitoring,
                                  width=15,
                                  bg='red',
                                  fg='white',
                                  state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态标签
        self.status_label = tk.Label(self.root, 
                                     text="状态: 未启动",
                                     font=('Arial', 12))
        self.status_label.pack(pady=5)
        
        # 自选股列表
        watchlist_frame = tk.LabelFrame(self.root, text="自选股列表", padx=10, pady=10)
        watchlist_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.watchlist_text = scrolledtext.ScrolledText(watchlist_frame,
                                                        width=70,
                                                        height=10,
                                                        font=('Courier', 10))
        self.watchlist_text.pack(fill=tk.BOTH, expand=True)
        
        # 显示当前自选股
        watchlist = '\n'.join(self.monitor.config['watchlist'])
        self.watchlist_text.insert('1.0', f"当前监控股票:\n{watchlist}")
        
        # 日志区域
        log_frame = tk.LabelFrame(self.root, text="监控日志", padx=10, pady=10)
        log_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                  width=70,
                                                  height=15,
                                                  font=('Courier', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 重定向标准输出到日志区域
        sys.stdout = TextRedirector(self.log_text)
    
    def start_monitoring(self):
        """启动监控"""
        self.monitor.start()
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_label.config(text="状态: 监控中...", fg='green')
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitor.stop()
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="状态: 已停止", fg='red')
    
    def run(self):
        """运行界面"""
        self.root.mainloop()


class TextRedirector:
    """文本重定向器，用于将print输出重定向到GUI"""
    
    def __init__(self, widget):
        self.widget = widget
    
    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
    
    def flush(self):
        pass


def main():
    """主函数"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║          股票监控系统 - Stock Monitor System             ║
    ║              基于同花顺API实时监控分析                    ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # 启动GUI
    try:
        gui = StockMonitorGUI()
        gui.run()
    except KeyboardInterrupt:
        print("\n程序已退出")
    except Exception as e:
        print(f"程序运行出错: {str(e)}")


if __name__ == "__main__":
    main()
