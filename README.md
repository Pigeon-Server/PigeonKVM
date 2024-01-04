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

### 以Debug模式启动项目
```shell
    python manage.py runserver 0.0.0.0:8080 --noreload
```

### 生产环境下运行
待完善...

### API文档

**待完善**
#### 个人信息管理

##### 获取用户信息
>**URL:** /userInfo/api/getInfo  
**方法:** GET | POST  
**需求权限:** any

##### 编辑用户信息
>**URL:** /userInfo/api/editInfo  
**方法:** POST  
**需求权限:** any  
**请求参数:**

##### 上传头像
>**URL:** /userInfo/api/uploadAvatar  
**方法:** POST  
**需求权限:** any  
**请求参数:**

##### 获取头像
>**URL:** /userInfo/api/getAvatar  
**方法:** GET  
**需求权限:** any

##### 设置密码
>**URL:** /userInfo/api/setPassword  
**方法:** POST  
**需求权限:** any  
**请求参数:**

#### 用户管理
##### 获取用户列表
>**URL:** /admin/api/getUserList  
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**

##### 新增用户
>**URL:** /admin/api/addUser  
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**

##### 删除用户
>**URL:** /admin/api/delUser  
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**

##### 获取用户权限
>**URL:** /admin/api/getUserPermission  
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**

##### 获取用户信息
>**URL:** /admin/api/getUserInfo
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**

##### 更改用户信息
>**URL:** /admin/api/setUserInfo  
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**

#### 权限管理

##### 获取权限组列表
>**URL:** /admin/api/getPermissionGroups  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**

##### 获取权限列表
>**URL:** /admin/api/getPermissionList  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**

##### 新增权限组
>**URL:** /admin/api/addPermissionGroup  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**

##### 删除权限组
>**URL:** /admin/api/delPermissionGroup  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**

##### 获取权限组信息
>**URL:** /admin/api/getPermissionGroupInfo  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**

##### 更改权限组信息
>**URL:** /admin/api/setPermissionGroup  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**

#### 审计与日志
##### 获取审计记录
>**URL:** /admin/api/auditAndLogger/audit  
**方法:** POST  
**需求权限:** viewAudit  
**请求参数:**

##### 获取访问日志
>**URL:** /admin/api/auditAndLogger/accessLog
**方法:** POST  
**需求权限:** viewAudit  
**请求参数:**

##### 获取文件修改记录
>**URL:** /admin/api/auditAndLogger/fileChangeLog  
**方法:** POST  
**需求权限:** viewAudit  
**请求参数:**

##### 获取系统日志
>**URL:** /admin/api/auditAndLogger/systemLog  
**方法:** POST  
**需求权限:** viewAudit  
**请求参数:**

Copyright © Pigeon Server Team