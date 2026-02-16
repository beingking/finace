#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例 - 演示如何使用股票监控系统

本文件展示了股票监控系统的各种使用方式和配置选项
"""

import sys
import os

# 确保可以导入stock_monitor模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from stock_monitor import StockMonitor, StockAnalyzer, TongHuaShunAPI
import json


def example_basic_monitoring():
    """示例1: 基本监控"""
    print("\n" + "="*70)
    print("示例1: 基本股票监控")
    print("="*70)
    
    # 创建监控器
    monitor = StockMonitor()
    
    # 执行一次扫描
    print("\n执行单次扫描...")
    monitor.scan_stocks()


def example_custom_config():
    """示例2: 自定义配置"""
    print("\n" + "="*70)
    print("示例2: 使用自定义配置")
    print("="*70)
    
    # 创建自定义配置
    custom_config = {
        'watchlist': ['600000', '000001'],  # 只监控两只股票
        'scan_interval': 30,  # 30秒扫描一次
        'alert_conditions': {
            'price_change_threshold': 2.0,  # 2%变动就提醒
            'buy_signal_threshold': 3,  # 降低买入信号阈值
            'sell_signal_threshold': -3
        }
    }
    
    # 保存临时配置
    temp_config_file = 'custom_config.json'
    with open(temp_config_file, 'w', encoding='utf-8') as f:
        json.dump(custom_config, f, ensure_ascii=False, indent=2)
    
    print(f"\n使用自定义配置文件: {temp_config_file}")
    print(f"监控股票: {', '.join(custom_config['watchlist'])}")
    print(f"扫描间隔: {custom_config['scan_interval']}秒")
    
    # 使用自定义配置创建监控器
    monitor = StockMonitor(temp_config_file)
    
    # 执行扫描
    print("\n执行扫描...")
    monitor.scan_stocks()
    
    # 清理临时文件
    if os.path.exists(temp_config_file):
        os.remove(temp_config_file)


def example_technical_analysis():
    """示例3: 技术分析演示"""
    print("\n" + "="*70)
    print("示例3: 技术分析功能演示")
    print("="*70)
    
    analyzer = StockAnalyzer()
    
    # 模拟一组股价数据（上涨趋势）
    uptrend_prices = [10.0, 10.2, 10.5, 10.8, 11.0, 11.3, 11.5, 11.8, 
                      12.0, 12.3, 12.5, 12.8, 13.0, 13.2, 13.5, 13.8,
                      14.0, 14.2, 14.5, 14.7, 15.0, 15.2, 15.5, 15.7,
                      16.0, 16.2, 16.5, 16.7, 17.0, 17.2]
    
    print("\n分析上涨趋势股票:")
    print(f"价格范围: {uptrend_prices[0]:.2f} -> {uptrend_prices[-1]:.2f}")
    
    stock_data = {
        'prices': uptrend_prices,
        'highs': [p * 1.02 for p in uptrend_prices],
        'lows': [p * 0.98 for p in uptrend_prices]
    }
    
    signals = analyzer.analyze_buy_sell_signals(stock_data)
    print(f"技术分析结果:")
    print(f"  建议: {signals['recommendation']}")
    print(f"  评分: {signals['score']}")
    if signals['buy_signals']:
        print(f"  买入信号: {', '.join(signals['buy_signals'])}")
    if signals['sell_signals']:
        print(f"  卖出信号: {', '.join(signals['sell_signals'])}")
    
    # 模拟一组股价数据（下跌趋势）
    downtrend_prices = [20.0, 19.8, 19.5, 19.2, 19.0, 18.7, 18.5, 18.2,
                        18.0, 17.7, 17.5, 17.2, 17.0, 16.8, 16.5, 16.2,
                        16.0, 15.8, 15.5, 15.3, 15.0, 14.8, 14.5, 14.3,
                        14.0, 13.8, 13.5, 13.3, 13.0, 12.8]
    
    print("\n分析下跌趋势股票:")
    print(f"价格范围: {downtrend_prices[0]:.2f} -> {downtrend_prices[-1]:.2f}")
    
    stock_data = {
        'prices': downtrend_prices,
        'highs': [p * 1.02 for p in downtrend_prices],
        'lows': [p * 0.98 for p in downtrend_prices]
    }
    
    signals = analyzer.analyze_buy_sell_signals(stock_data)
    print(f"技术分析结果:")
    print(f"  建议: {signals['recommendation']}")
    print(f"  评分: {signals['score']}")
    if signals['buy_signals']:
        print(f"  买入信号: {', '.join(signals['buy_signals'])}")
    if signals['sell_signals']:
        print(f"  卖出信号: {', '.join(signals['sell_signals'])}")


def example_api_usage():
    """示例4: API使用演示"""
    print("\n" + "="*70)
    print("示例4: API接口使用演示")
    print("="*70)
    
    api = TongHuaShunAPI()
    
    stock_code = "600000"
    
    # 获取实时价格
    print(f"\n获取 {stock_code} 的实时数据:")
    price_data = api.get_realtime_price(stock_code)
    print(f"  名称: {price_data['name']}")
    print(f"  价格: {price_data['price']:.2f}")
    print(f"  涨跌: {price_data['change']:+.2f} ({price_data['change_percent']:+.2f}%)")
    
    # 获取盘面信息
    print(f"\n获取盘面信息:")
    market_info = api.get_market_info(stock_code)
    print(f"  市盈率: {market_info['pe_ratio']:.2f}")
    print(f"  市净率: {market_info['pb_ratio']:.2f}")
    
    # 获取新闻
    print(f"\n获取最新新闻 (前3条):")
    news = api.get_news(stock_code, limit=3)
    for i, item in enumerate(news, 1):
        print(f"  {i}. {item['title']}")
    
    # 获取历史价格
    print(f"\n获取历史价格 (最近5天):")
    historical = api.get_historical_prices(stock_code, days=5)
    for i, price in enumerate(historical, 1):
        print(f"  第{i}天: {price:.2f}")


def main():
    """主函数 - 运行所有示例"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║          股票监控系统 - 使用示例                          ║
    ╚══════════════════════════════════════════════════════════╝
    
    本示例程序展示了股票监控系统的各种使用方式
    """)
    
    try:
        # 运行各个示例
        example_basic_monitoring()
        example_custom_config()
        example_technical_analysis()
        example_api_usage()
        
        print("\n" + "="*70)
        print("所有示例运行完成!")
        print("="*70)
        print("\n提示:")
        print("  - 使用 'python stock_monitor.py' 启动GUI监控")
        print("  - 使用 'python stock_monitor.py --cli' 启动命令行监控")
        print("  - 使用 'python demo.py' 快速测试")
        print("  - 编辑 'config.json' 自定义监控参数")
        
    except Exception as e:
        print(f"\n运行示例时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
