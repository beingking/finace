#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票监控程序测试脚本
"""

import sys
import os

# 确保可以导入stock_monitor模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from stock_monitor import StockAnalyzer, TongHuaShunAPI, StockMonitor


def test_technical_analysis():
    """测试技术分析功能"""
    print("=" * 60)
    print("测试技术分析模块")
    print("=" * 60)
    
    analyzer = StockAnalyzer()
    
    # 测试数据
    prices = [10.0, 10.2, 10.5, 10.3, 10.8, 11.0, 10.9, 11.2, 11.5, 11.3,
              11.6, 11.8, 11.7, 12.0, 12.2, 12.1, 12.4, 12.6, 12.5, 12.8,
              13.0, 12.9, 13.2, 13.5, 13.3, 13.6, 13.8, 13.7, 14.0, 14.2]
    
    # 测试MA
    ma5 = analyzer.calculate_ma(prices, 5)
    ma10 = analyzer.calculate_ma(prices, 10)
    ma20 = analyzer.calculate_ma(prices, 20)
    print(f"\n移动平均线:")
    print(f"  MA5:  {ma5:.2f}")
    print(f"  MA10: {ma10:.2f}")
    print(f"  MA20: {ma20:.2f}")
    
    # 测试RSI
    rsi = analyzer.calculate_rsi(prices)
    print(f"\nRSI指标: {rsi:.2f}")
    
    # 测试MACD
    macd = analyzer.calculate_macd(prices)
    print(f"\nMACD指标:")
    print(f"  MACD线:   {macd['macd']:.4f}")
    print(f"  信号线:   {macd['signal']:.4f}")
    print(f"  柱状图:   {macd['histogram']:.4f}")
    
    # 测试KDJ
    highs = [p * 1.02 for p in prices]
    lows = [p * 0.98 for p in prices]
    kdj = analyzer.calculate_kdj(highs, lows, prices)
    print(f"\nKDJ指标:")
    print(f"  K值: {kdj['k']:.2f}")
    print(f"  D值: {kdj['d']:.2f}")
    print(f"  J值: {kdj['j']:.2f}")
    
    # 测试综合分析
    stock_data = {
        'prices': prices,
        'highs': highs,
        'lows': lows
    }
    signals = analyzer.analyze_buy_sell_signals(stock_data)
    
    print(f"\n综合分析结果:")
    print(f"  建议: {signals['recommendation']}")
    print(f"  评分: {signals['score']}")
    if signals['buy_signals']:
        print(f"  买入信号: {', '.join(signals['buy_signals'])}")
    if signals['sell_signals']:
        print(f"  卖出信号: {', '.join(signals['sell_signals'])}")
    
    print("\n✓ 技术分析测试通过")


def test_api():
    """测试API接口"""
    print("\n" + "=" * 60)
    print("测试API接口")
    print("=" * 60)
    
    api = TongHuaShunAPI()
    
    # 测试获取实时价格
    stock_code = "600000"
    price_data = api.get_realtime_price(stock_code)
    print(f"\n实时价格数据 ({stock_code}):")
    print(f"  股票名称: {price_data['name']}")
    print(f"  当前价格: {price_data['price']:.2f}")
    print(f"  涨跌额:   {price_data['change']:+.2f}")
    print(f"  涨跌幅:   {price_data['change_percent']:+.2f}%")
    
    # 测试获取盘面信息
    market_info = api.get_market_info(stock_code)
    print(f"\n盘面信息:")
    print(f"  市盈率:   {market_info['pe_ratio']:.2f}")
    print(f"  市净率:   {market_info['pb_ratio']:.2f}")
    print(f"  总市值:   {market_info['market_cap']:,}")
    
    # 测试获取新闻
    news = api.get_news(stock_code, limit=3)
    print(f"\n最新新闻:")
    for i, item in enumerate(news, 1):
        print(f"  {i}. {item['title']}")
    
    # 测试获取历史价格
    historical_prices = api.get_historical_prices(stock_code, days=10)
    print(f"\n历史价格 (最近10天):")
    for i, price in enumerate(historical_prices[-5:], 1):
        print(f"  第{i}天: {price:.2f}")
    
    print("\n✓ API接口测试通过")


def test_monitor():
    """测试监控功能（不启动GUI）"""
    print("\n" + "=" * 60)
    print("测试监控功能")
    print("=" * 60)
    
    # 创建监控对象
    monitor = StockMonitor()
    
    print(f"\n配置信息:")
    print(f"  自选股列表: {', '.join(monitor.config['watchlist'])}")
    print(f"  扫描间隔: {monitor.config['scan_interval']} 秒")
    print(f"  价格异动阈值: {monitor.config['alert_conditions']['price_change_threshold']}%")
    
    # 执行一次扫描测试
    print(f"\n执行单次扫描测试:")
    monitor.scan_stocks()
    
    print("\n✓ 监控功能测试通过")


def main():
    """主测试函数"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║          股票监控系统 - 功能测试                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        # 运行各项测试
        test_technical_analysis()
        test_api()
        test_monitor()
        
        print("\n" + "=" * 60)
        print("所有测试通过! ✓")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
