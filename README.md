# [PigeonKVM](https://github.com/Pigeon-Server/PigeonKVM)
PigeonKVM是一个由Python+django编写的IPKVM程序，用于实现服务器主机管理，拥有更强大的审计与权限管理功能 

**该项目当前处于alpha阶段，功能尚未完善，可能会有严重的性能问题**

## 编译与部署

**拉取源码**

```shell
    # 克隆源码到本地
    git clone https://github.com/Pigeon-Server/PigeonKVM.git
    cd PigeonKVM
```

**编译用户界面**

```shell
    # 进入UI项目文件夹
    cd web_develop
    # 安装NodeJs依赖
    npm i
    # 将静态文件编译到指定文件夹
    npm run buildToStatic
    # 返回主目录
    cd ../
```

**准备Python环境**

```shell
    # 新建虚拟环境
    python -m venv venv
    # 进入虚拟环境
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate  # Linux
    # 安装依赖
    pip3 install -r requirements.txt
```

**注：如需使用OrangePi GPIO需单独编译wiringOP-Python**
```shell
     sudo apt-get update  # 更新软件源
     sudo apt-get -y install git swig python3-dev python3-setuptools  # 安装依赖包
     # 注意，下面的 git clone--recursive 命令会自动下载wiringOP 的源码，因为wiringOP-Python 是依赖 wiringOP 的。请确保下载过程没有因为网络问题而报错。如 果 从 GitHub 下 载 代 码 有 问 题 ， 可 以 直 接 使用Linux 镜像中自带的wiringOP-Python 源码，存放位置为：/usr/src/wiringOP-Python。
     git clone --recursive https://github.com/orangepi-xunlong/wiringOP-Python -b next  # 拉取代码
     cd wiringOP-Python  # 进入目录
     git submodule update --init --remote  # 更新子模块
     ../venv/bin/python3 generate-bindings.py > bindings.i
     ../venv/bin/python3 setup.py install
     # 输入下面的命令，如果有帮助信息输出，说明 wiringOP-Python 安装成功，按下 q 键可以退出帮助信息的界面
     ../venv/bin/python3 -c "import wiringpi; help(wiringpi)"
```

**迁移数据库与导入数据**
```shell
    # 创建迁移数据
    python manage.py makemigrations
    # 迁移数据库 
    python manage.py migrate
```

### 以Debug模式启动项目
```shell
    python manage.py runserver 0.0.0.0:8080 --noreload
```

### 生产环境下运行
#### 在Docker中运行
```shell
```
#### 直接安装
```shell
```
待完善...

## API文档
[link](docs/apis.md)

Copyright © [Pigeon Server Team](https://github.com/Pigeon-Server)