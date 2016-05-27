#Coding-Analysis
A way to find data behind your repo.

###About the dirs.
```
Coding-Analysis/        <-- 根目录
|
+- docs/                        <-- 文档
|
+- gitspider/                      <-- gitapi数据采集脚本根目录
|
+- local/                       <-- 本地数据采集脚本根目录
|  |
|  +- collectors/           <-- 本地数据采集器
|  |
|  +- projects              <-- 本地repo
|
+- LICENSE                  <-- 代码LICENSE
|
+- requirements.txt     <-- 附加需求文档 
|
+- run.py                       <--列示代码
```

###Example:
 Check `./run.py`.
 
###A few things you need care.
For the first time of using the script , you need change some configurations in `Coding-Analysis/config.py`.

1. The `ACCESS_TOKEN = your_access_token`, if you don't have one ,create it at your settings.
2. The `PROJECT_NAME = your_local_pro_name`, check the dir `Coding-Analysis/local/projects` to see all the local repo.

(You need to add the your local repo to `/Coding-Analysis/local/prejects` or downloading one by using the shell script `./local/downloadRepo.sh`)


 