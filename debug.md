# 安装工具

```
dnf install -y procps-ng
```

- top, ps, pgrep, pkill, free, uptime, vmstat, sysctl, watch, pwdx

```
dnf install -y lsof
```

```
sudo dnf install -y sysstat 
```

- iostat, mpstat, pidstat, sar

```
sudo dnf install -y strace gdb
```

# k8s

```
kubectl get pods
```

```
kubectl exec -it <pod> -- /bin/bash
```

```
kubectl logs <pod-name> [-c <container-name>] --tail=100 -f
```

```
kubectl logs <pod-name> --previous
```

```
kubectl describe pod <pod>
```

```
kubectl cp <pod-name>:/path/to/log.txt ./local-log.txt
```

```
kubectl exec <pod>  -- grep WARN server.log
```

```
kubectl get pods -l app=nginx -o name | xargs -I{} kubectl exec {} -- uptime
```

# 系统配置

## 内存

```
cat /proc/sys/vm/max_map_count
```

```
wc -l /proc/48/maps
```

```
echo 262144 > /proc/sys/vm/max_map_count
```

```
 grep -E 'MemAvailable|SwapTotal|SwapFree' /proc/meminfo
```

```
  cat /sys/fs/cgroup/memory.max 2>/dev/null
  cat /sys/fs/cgroup/memory.current 2>/dev/null
  cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null
  cat /sys/fs/cgroup/memory/memory.usage_in_bytes 2>/dev/null
```

# 数据量

## Segment 数量

```sql
SELECT SUM(JSON_LENGTH(JSON_EXTRACT(manifest, '$.fragments[*].f.segs[*]'))) AS segs_count FROM tici_shard_meta;
```

## Frag 数量

```sql
SELECT SUM(JSON_LENGTH(JSON_EXTRACT(manifest, '$.fragments[*]'))) AS frag_count FROM tici_shard_meta;
```

## Key 数量

```sql
SELECT JSON_EXTRACT(manifest, '$.fragments[*].f.property.count') AS segs_count FROM tici_shard_meta;
```

```python
python calc_shard_count.py --host test-infra-tunnel.pingcap.net --user root --port 42512 --password "" --query "select shard_id from tici.tici_shard_meta"
```

# 日志

```
awk -F'[][]' '$2 >= "2026/02/26 04:24:01" && $2 <= "2026/02/26 04:39:00"' tici_searchlib.log
```





| **你的需求**            | **应该用什么**              | **示例**                    |
| ----------------------- | --------------------------- | --------------------------- |
| 定位特定的服务或机器    | **标签选择器** (`=`, `=~`)  | `{app="payment"}`           |
| 随便搜个关键字          | **文本包含** (`|=`)         | `|= "NullPointerException"` |
| 搜关键字 A **或者** B   | **文本正则** (`|~`)         | `|~ "ERROR|FATAL"`          |
| 排除干扰信息            | **文本不包含** (`!=`)       | `!= "health_check"`         |
| 查找耗时大于 1 秒的请求 | **解析器 + 数值比较** (`>`) | `| json | latency > 1`      |

