

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





```
cat /proc/sys/vm/max_map_count

wc -l /proc/48/maps



# 1) 看 max_map_count
  cat /proc/sys/vm/max_map_count

  # 2) 看 tici 进程 map 数量（是否接近上限）
  PID=$(pgrep -f TiFlashMain | head -n1)
  echo "PID=$PID"
  wc -l /proc/$PID/maps

  # 3) 看内存是否顶满
  grep -E 'MemAvailable|SwapTotal|SwapFree' /proc/meminfo

  # 4) cgroup 限制（容器场景）
  cat /sys/fs/cgroup/memory.max 2>/dev/null
  cat /sys/fs/cgroup/memory.current 2>/dev/null
  cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null
  cat /sys/fs/cgroup/memory/memory.usage_in_bytes 2>/dev/null

  如果要临时调高（需有权限）：

  echo 262144 > /proc/sys/vm/max_map_count

```



# Segment 数量

```sql
SELECT SUM(JSON_LENGTH(JSON_EXTRACT(manifest, '$.fragments[*].f.segs[*]'))) AS segs_count FROM tici_shard_meta;
```

# Frag 数量

```sql
SELECT SUM(JSON_LENGTH(JSON_EXTRACT(manifest, '$.fragments[*]'))) AS frag_count FROM tici_shard_meta;
```

# Key 数量

```sql
SELECT JSON_EXTRACT(manifest, '$.fragments[*].f.property.count') AS segs_count FROM tici_shard_meta;
```



```python
python calc_shard_count.py --host test-infra-tunnel.pingcap.net --user root --port 42512 --password "" --query "select shard_id from tici.tici_shard_meta"
```









```
kubectl get pods -l app=nginx -o name | xargs -I{} 


kubectl exec tici-tiflash-0 -- "grep -E 'WARN|ERRIR' data0/tici_searchlib.log"
```













```
python calc_count.py --host test-infra-tunnel.pingcap.net --user root --port 41343 --password "" 31548 31555 1360 1364 31573


python calc_count.py --host test-infra-tunnel.pingcap.net --user root --port 41343 --password "" --query "select shard_id from tici.tici_shard_meta"


python calc_count.py --host test-infra-tunnel.pingcap.net --user root --port 42512 --password "" --query "select shard_id from tici.tici_shard_meta"

```



```
awk -F'[][]' '$2 >= "2026/02/26 04:24:01" && $2 <= "2026/02/26 04:39:00"' tici_searchlib.log
```

