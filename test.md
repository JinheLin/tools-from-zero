```
./import_amazon_review_lightning.sh --host 10.2.12.79 --port 8063 --user root --db fts --table amazon_review --pd-addr 10.2.12.79:6561


--force-restart


./import_amazon_review_lightning.sh --host 10.2.12.79 --port 8063 --user root --db fts --skip-create-table  --force-restart


  常用可选参数：

  - --db fts --table amazon_review 覆盖目标库表
  - --skip-create-table 只导入数据，不执行 create_table.sql
  - --config-out xxx.toml --log-file xxx.log 自定义配置和日志路径
  
  
  
```

