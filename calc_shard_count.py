import pymysql
import json
import argparse
import sys

def main():
    # ==========================================
    # 1. 设置命令行参数解析
    # ==========================================
    parser = argparse.ArgumentParser(description="获取 SHARD_ID 对应的 property.count 总和并按降序输出。")
    
    # 数据库连接参数
    parser.add_argument('-H', '--host', type=str, default='127.0.0.1', help='MySQL 主机地址 (默认: 127.0.0.1)')
    parser.add_argument('-P', '--port', type=int, default=3306, help='MySQL 端口 (默认: 3306)')
    parser.add_argument('-u', '--user', type=str, required=True, help='MySQL 用户名 (必填)')
    parser.add_argument('-p', '--password', type=str, required=True, help='MySQL 密码 (必填)')
    
    # 新增：SQL 查询参数
    parser.add_argument('-q', '--query', type=str, help='用于获取 shard_id 列表的 SQL 语句 (例如: "SELECT shard_id FROM tici.tici_shard_meta LIMIT 10")')
    
    # SHARD_ID 列表 (改为可选，nargs='*')
    parser.add_argument('shard_ids', metavar='SHARD_ID', type=int, nargs='*', help='一个或多个手动指定的 SHARD_ID (空格分隔，可选)')

    # 解析参数
    args = parser.parse_args()

    # 校验：必须提供 SQL 或者 手动输入 ID
    if not args.query and not args.shard_ids:
        parser.error("必须提供至少一个 SHARD_ID，或者使用 -q/--query 提供获取 ID 的 SQL 语句。")

    # ==========================================
    # 2. 组装 MySQL 连接配置
    # ==========================================
    db_config = {
        'host': args.host,
        'port': args.port,
        'user': args.user,
        'password': args.password,
        'database': 'tici',  # 固定库名
        'cursorclass': pymysql.cursors.DictCursor
    }

    print("-" * 50)
    print("=> MySQL 连接参数:")
    print(f"   Host:  {db_config['host']}")
    print(f"   Port:  {db_config['port']}")
    print(f"   User:  {db_config['user']}")
    print(f"   DB:    {db_config['database']} (固定)")
    print("-" * 50)

    try:
        # 建立数据库连接
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # ==========================================
            # 3. 收集所有的 SHARD_ID
            # ==========================================
            target_shard_ids = set(args.shard_ids) # 使用 set 去重
            
            if args.query:
                print(f"=> 执行 SQL 获取 SHARD_ID 列表:\n   [{args.query}]")
                cursor.execute(args.query)
                query_results = cursor.fetchall()
                
                for row in query_results:
                    # 如果查询结果包含 shard_id 列，直接取；否则默认取第一列的值
                    if 'shard_id' in row:
                        target_shard_ids.add(row['shard_id'])
                    elif row:
                        target_shard_ids.add(list(row.values())[0])
            
            target_shard_ids = list(target_shard_ids)
            
            if not target_shard_ids:
                print("\n[提示] 未获取到任何 SHARD_ID，程序结束。")
                return
                
            print(f"=> 共收集到 {len(target_shard_ids)} 个不重复的 SHARD_ID，开始查询并计算...\n")

            # ==========================================
            # 4. 分批查询 manifest 数据并计算
            # ==========================================
            db_data = {}
            batch_size = 1000 # 每次最多查 1000 个，防止 IN 语句过长
            
            for i in range(0, len(target_shard_ids), batch_size):
                batch_ids = target_shard_ids[i:i + batch_size]
                placeholders = ','.join(['%s'] * len(batch_ids))
                
                sql = f"SELECT shard_id, manifest FROM tici_shard_meta WHERE shard_id IN ({placeholders})"
                cursor.execute(sql, tuple(batch_ids))
                
                # 合并到总数据字典中
                for row in cursor.fetchall():
                    db_data[row['shard_id']] = row['manifest']

            # ==========================================
            # 5. 解析并计算 Count
            # ==========================================
            summary_list = []
            
            for sid in target_shard_ids:
                manifest_str = db_data.get(sid)
                
                if not manifest_str:
                    summary_list.append({'sid': sid, 'count': -1, 'msg': "未找到数据或 manifest 为空"})
                    continue
                
                try:
                    manifest_data = json.loads(manifest_str)
                    
                    # 应对未知长度的数组，安全提取并求和
                    total_count = sum(
                        frag.get('f', {}).get('property', {}).get('count', 0)
                        for frag in manifest_data.get('fragments', [])
                    )
                    
                    summary_list.append({'sid': sid, 'count': total_count, 'msg': f"Total Count: {total_count}"})
                    
                except json.JSONDecodeError:
                    summary_list.append({'sid': sid, 'count': -1, 'msg': "JSON 解析失败"})

            # ==========================================
            # 6. 结果降序排序与输出
            # ==========================================
            summary_list.sort(key=lambda x: x['count'], reverse=True)

            print("=> 计算结果 (按 count 降序排序):")
            for item in summary_list:
                if item['count'] >= 0:
                    print(f"   [SHARD_ID: {item['sid']:<8}] {item['msg']}")
                else:
                    print(f"   [SHARD_ID: {item['sid']:<8}] 结果: {item['msg']}")

    except pymysql.MySQLError as e:
        print(f"\n[错误] 数据库连接或执行失败: {e}")
    except Exception as e:
        print(f"\n[错误] 发生意外异常: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    main()
    