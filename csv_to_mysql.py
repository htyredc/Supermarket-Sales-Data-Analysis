#!/usr/bin/env python3
"""
将supermarket_sales.csv数据转换为MySQL SQL导入脚本
"""

import csv
import os
from datetime import datetime

def convert_csv_to_mysql(csv_file_path, sql_file_path):
    """
    将CSV文件转换为MySQL SQL导入脚本
    
    Args:
        csv_file_path: CSV文件路径
        sql_file_path: 输出SQL文件路径
    """
    # 读取CSV文件
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # 获取列名
        rows = list(csv_reader)  # 获取所有数据行
    
    # 生成SQL脚本，使用纯UTF-8编码，保持通用性
    with open(sql_file_path, 'w', encoding='utf-8') as sql_file:
        # 1. 创建数据库（如果需要）
        sql_file.write('-- 创建数据库（如果不存在）\n')
        sql_file.write('CREATE DATABASE IF NOT EXISTS supermarket_sales;\n')
        sql_file.write('USE supermarket_sales;\n\n')
        
        # 2. 创建表
        sql_file.write('-- 创建销售数据表\n')
        sql_file.write('CREATE TABLE IF NOT EXISTS sales (\n')
        sql_file.write('    invoice_id VARCHAR(20) PRIMARY KEY,\n')
        sql_file.write('    branch CHAR(1),\n')
        sql_file.write('    city VARCHAR(50),\n')
        sql_file.write('    customer_type VARCHAR(20),\n')
        sql_file.write('    gender VARCHAR(10),\n')
        sql_file.write('    product_line VARCHAR(100),\n')
        sql_file.write('    unit_price DECIMAL(10, 2),\n')
        sql_file.write('    quantity INT,\n')
        sql_file.write('    tax_5_percent DECIMAL(10, 4),\n')
        sql_file.write('    total DECIMAL(10, 4),\n')
        sql_file.write('    sale_date DATE,\n')
        sql_file.write('    sale_time TIME,\n')
        sql_file.write('    payment VARCHAR(20),\n')
        sql_file.write('    cogs DECIMAL(10, 2),\n')
        sql_file.write('    gross_margin_percentage DECIMAL(10, 9),\n')
        sql_file.write('    gross_income DECIMAL(10, 4),\n')
        sql_file.write('    rating DECIMAL(3, 1)\n')
        sql_file.write(') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n')
        
        # 3. 禁用外键检查（可选，加速导入）
        sql_file.write('-- 禁用外键检查以加速导入\n')
        sql_file.write('SET FOREIGN_KEY_CHECKS = 0;\n\n')
        
        # 4. 清空表（如果需要）
        sql_file.write('-- 清空表数据（如果需要）\n')
        sql_file.write('TRUNCATE TABLE sales;\n\n')
        
        # 5. 生成INSERT语句
        sql_file.write('-- 插入数据\n')
        sql_file.write('INSERT INTO sales (\n')
        sql_file.write('    invoice_id, branch, city, customer_type, gender, product_line,\n')
        sql_file.write('    unit_price, quantity, tax_5_percent, total, sale_date, sale_time,\n')
        sql_file.write('    payment, cogs, gross_margin_percentage, gross_income, rating\n')
        sql_file.write(') VALUES\n')
        
        # 处理每一行数据
        for i, row in enumerate(rows):
            # 格式化日期（将MM/DD/YYYY转换为YYYY-MM-DD）
            sale_date = datetime.strptime(row[10], '%m/%d/%Y').strftime('%Y-%m-%d')
            
            # 格式化时间（确保是HH:MM格式）
            sale_time = row[11]
            
            # 构建INSERT语句的值部分
            values = [
                f"'{row[0]}'",  # invoice_id
                f"'{row[1]}'",  # branch
                f"'{row[2]}'",  # city
                f"'{row[3]}'",  # customer_type
                f"'{row[4]}'",  # gender
                f"'{row[5]}'",  # product_line
                f"{row[6]}",    # unit_price
                f"{row[7]}",    # quantity
                f"{row[8]}",    # tax_5_percent
                f"{row[9]}",    # total
                f"'{sale_date}'",  # sale_date
                f"'{sale_time}'",  # sale_time
                f"'{row[12]}'", # payment
                f"{row[13]}",   # cogs
                f"{row[14]}",   # gross_margin_percentage
                f"{row[15]}",   # gross_income
                f"{row[16]}"    # rating
            ]
            
            # 生成完整的INSERT语句行
            values_str = ', '.join(values)
            if i == len(rows) - 1:
                # 最后一行，使用分号结束
                sql_file.write(f'    ({values_str});\n')
            else:
                # 不是最后一行，使用逗号结束
                sql_file.write(f'    ({values_str}),\n')
        
        # 6. 启用外键检查
        sql_file.write('\n-- 启用外键检查\n')
        sql_file.write('SET FOREIGN_KEY_CHECKS = 1;\n\n')
        
        # 7. 提交事务（如果需要）
        sql_file.write('-- 提交事务\n')
        sql_file.write('COMMIT;\n')
    
    print(f"SQL脚本已生成：{sql_file_path}")

if __name__ == "__main__":
    # CSV文件路径
    csv_file = "supermarket_sales - Sheet1.csv"
    # 输出SQL文件路径
    sql_file = "supermarket_sales.sql"
    
    # 转换CSV到MySQL SQL
    convert_csv_to_mysql(csv_file, sql_file)
