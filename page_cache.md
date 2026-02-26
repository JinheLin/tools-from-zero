在 Linux 系统中，**Page Cache（页缓存）** 是内核为了提高磁盘 I/O 效率，将一部分物理内存用于缓存磁盘数据的机制。

Linux 内核通常会自动管理 Page Cache，尽量占满剩余内存以提升性能。如果你发现 Page Cache 占用过高导致系统“内存不足”的假象，或者由于大量写入导致系统卡顿，可以通过修改 `/proc/sys/vm/` 下的内核参数进行限制和调优。





# 脏数据刷盘

| **参数**                    | **说明**                                                     | 默认值      |                                                              |
| --------------------------- | ------------------------------------------------------------ | ----------- | ------------------------------------------------------------ |
| vm.dirty_ratio              | 当脏数据达到系统总内存的百分比时，系统「阻塞」新的写请求，强制将数据刷入磁盘。 | 20%         | 通常为 20%，对于高速磁盘可调低。                             |
| vm.dirty_background_ratio   | 当脏数据达到总内存的百分比时，后台线程（pdflush/kworker）开始「异步」刷盘，不阻塞应用。 | 10%         | 通常为 10%，应小于 dirty_ratio。                             |
| vm.dirty_bytes              | 与 dirty_ratio 功能相同，但以字节为单位。设置此项会自动覆盖 ratio。 | /           | 适用于内存极大的服务器，精确控制缓存大小。                   |
| vm.dirty_background_bytes   | 与 dirty_background_ratio 功能相同，以字节为单位。           | /           | 适用于内存极大的服务器，精确控制缓存大小。                   |
| vm.dirty_expire_centisecs   | 脏数据在内存中驻留多久后被视为“过期”。单位：1/100秒。        | 3000 (30秒) | 缩短此时间可以减少系统崩溃时丢失数据的风险，并降低突发大流量写入的压力。 |
| vm.dirty_writeback_centisec | 内核线程多久检查一次是否有脏数据需要刷盘。                   | 500 (5秒)   |                                                              |



## 内存回收倾向 (Swappiness)

虽然不是直接限制 Page Cache 大小，但它决定了系统在内存不足时是优先回收 Page Cache 还是 Swap 交换内存。

- vm.swappiness: 范围 0-100。
  - 较低值 (如 10): 倾向于回收 Page Cache（保持应用活跃数据在内存）。
  - 较高值 (如 60+): 倾向于将匿名内存交换到磁盘，保留更多 Page Cache 以加速文件读写。

## 强制释放 Page Cache (手动操作)

如果你想立即清除已产生的 Page Cache，可以向 `drop_caches` 写入特定数值。**注意：这仅能释放可回收的缓存，正在使用的不会被释放。**



```
# 1. 释放页缓存 (Page Cache)
echo 1 > /proc/sys/vm/drop_caches

# 2. 释放目录项和索引节点 (dentries and inodes)
echo 2 > /proc/sys/vm/drop_caches

# 3. 释放页缓存、目录项和索引节点 (最常用)
echo 3 > /proc/sys/vm/drop_caches
```



## 控制 VFS 缓存回收压力

除了文件内容，Linux 还会缓存文件的元数据（目录项 dentry 和索引节点 inode）。

- **`vm.vfs_cache_pressure`**：默认值为 **100**。
  - **设置 > 100**（如 200）：内核会更频繁地回收元数据缓存，从而腾出更多内存。
  - **设置 < 100**：内核倾向于保留元数据缓存，这能加快文件查找速度，但会占用更多内存。





过度限制 Page Cache 会导致磁盘 I/O 剧增，从而显著降低系统运行速度。通常建议通过 `dirty_bytes` 限制脏数据的“上限”，而不是强行缩减 Page Cache。



如果你是为了防止**磁盘 IO 导致系统卡顿**：

- 调低 `vm.dirty_background_ratio` 和 `vm.dirty_ratio`。

如果你是为了给**应用程序留出更多物理内存**：

- 调低 `vm.swappiness`（如设为 10）。
- 适当增加 `vm.vfs_cache_pressure`（如设为 200）。

**持久化配置**： 将配置写入 `/etc/sysctl.conf` 并运行 `sysctl -p`。





# mmap

- madvise