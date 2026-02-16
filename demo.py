#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单演示程序 - 运行一次扫描
"""

import sys
sys.path.insert(0, '/home/runner/work/finace/finace')

from stock_monitor import StockMonitor

def main():
    print("=" * 70)
    print("股票监控系统 - 单次扫描演示")
    print("=" * 70)
    
    # 创建监控对象
    monitor = StockMonitor()
    
    print(f"\n配置信息:")
    print(f"  监控股票: {', '.join(monitor.config['watchlist'])}")
    print(f"  扫描间隔: {monitor.config['scan_interval']} 秒")
    print(f"  价格异动阈值: {monitor.config['alert_conditions']['price_change_threshold']}%")
    
    # 执行单次扫描
    monitor.scan_stocks()
    
    print("\n演示完成!")

if __name__ == "__main__":
    main()
