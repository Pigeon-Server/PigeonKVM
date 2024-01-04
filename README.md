# IPKVM Core
IPKVM Core是一个由Python+django编写的KVM程序，拥有更强大的审计与权限管理功能 

**该项目当前处于alpha阶段，功能尚未完善，可能会有严重的性能问题**

## 编译与部署

### 编译用户界面

```shell
    # 进入UI项目文件夹
    cd web_develop
    # 安装NodeJs依赖
    npm i
    # 将静态文件编译到指定文件夹
    npm run buildToStatic
```

### 准备Python环境
```shell
    # 新建虚拟环境
    python -m venv venv
    # 进入虚拟环境
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate  # Linux
    # 安装依赖
    pip3 install -r requirements.txt
```

### 迁移数据库与导入数据
```shell
    # 创建迁移数据
    python manage.py makemigrations
    # 迁移数据库 
    python manage.py migrate
```

### 启动Debug模式

```shell
    python manage.py runserver 0.0.0.0:8080 --noreload
```

Copyright © Pigeon Server Team