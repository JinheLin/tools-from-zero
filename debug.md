

```
dnf install -y procps-ng
```

- top, ps, pgrep, pkill, free, uptime, vmstat, sysctl, watch, pwdx

```
dnf install -y lsof
```

```
dnf install -y pcp-system-tools
```

- pcp-dstat, dstat, pop-iostat, pcp-free, pcp-uptime
- pmstat, pminfo
- pmval, pmlogger
- pmprobe

```
sudo dnf install -y sysstat 
```

- iostat, mpstat, pidstat, sar

```
sudo dnf install -y strace gdb
```



```
kubectl logs <pod-name> [-c <container-name>] --tail=100 -f
```



```
kubectl logs <pod-name> --previous
```

- 如果 Pod 已经挂了，查看上一个退出的容器日志



```
kubectl debug -it <pod-name> --image=nicolaka/netshoot --target=<container-name>
```



```
kubectl cp <pod-name>:/path/to/log.txt ./local-log.txt
```



```
kubectl exec -it <pod-name> -- ping <service-name>
```

