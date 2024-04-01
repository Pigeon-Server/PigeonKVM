# API文档

## API状态标志
| 状态码 | 介绍        |
|-----|-----------|
| -1  | 参数错误或违规参数 |
| 0   | 失败或无权限    |
| 1   | 正常返回      |

## 个人信息管理
### 获取用户信息
**URL:** /userInfo/api/getInfo  
**方法:** GET | POST  
**需求权限:** auth  
**返回数据:**
```json

```
___
### 编辑用户信息
**URL:** /userInfo/api/editInfo  
**方法:** POST  
**需求权限:** auth  
**请求参数:**
```json

```
**返回数据:**
```json

```
___
### 上传头像
**URL:** /userInfo/api/uploadAvatar  
**方法:** POST  
**需求权限:** auth  
**请求参数:**

```json
{
  "data": {
    "avatarImgBase64": "", // 通过Base64编码的图片
    "avatarImgHash": ""  // 图片哈希
  }
}
```
**返回数据:**
```json
{
  "status": 1, // 状态
  "msg": ""  // 提示消息
}
```
___
### 获取头像
**URL:** /userInfo/api/getAvatar  
**方法:** GET  
**需求权限:** auth  
**返回数据:** Image

### 设置密码
**URL:** /userInfo/api/setPassword  
**方法:** POST  
**需求权限:** any  
**请求参数:**

```json
{
  "data": {
    "oldPassword": "",  // 旧密码
    "newPassword": ""  // 新密码
  }
}
```
**返回数据:**

```json
{
  "status": 1, // 状态
  "msg": ""  // 提示消息
}
```
___
## 用户管理
### 获取用户列表
**URL:** /admin/api/getUserList  
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**
___
### 新增用户
**URL:** /admin/api/addUser  
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**
___
### 删除用户
**URL:** /admin/api/delUser  
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**
___
### 获取用户权限
**URL:** /admin/api/getUserPermission  
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**
___
### 获取用户信息
**URL:** /admin/api/getUserInfo  
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**
___
### 更改用户信息
**URL:** /admin/api/setUserInfo  
**方法:** POST  
**需求权限:** manageUsers  
**请求参数:**
___
## 权限管理
### 获取权限组列表
**URL:** /admin/api/getPermissionGroups  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**
___
### 获取权限列表
**URL:** /admin/api/getPermissionList  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**
___
### 新增权限组
**URL:** /admin/api/addPermissionGroup  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**
___
### 删除权限组
**URL:** /admin/api/delPermissionGroup  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**
___
### 获取权限组信息
**URL:** /admin/api/getPermissionGroupInfo  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**
___
### 更改权限组信息
**URL:** /admin/api/setPermissionGroup  
**方法:** POST  
**需求权限:** managePermissionGroups  
**请求参数:**
___
## 审计与日志
### 获取审计记录
**URL:** /admin/api/auditAndLogger/audit  
**方法:** POST  
**需求权限:** viewAudit  
**请求参数:**
___
### 获取访问日志
**URL:** /admin/api/auditAndLogger/accessLog
**方法:** POST  
**需求权限:** viewAudit  
**请求参数:**
___
### 获取文件修改记录
**URL:** /admin/api/auditAndLogger/fileChangeLog  
**方法:** POST  
**需求权限:** viewAudit  
**请求参数:**
___
### 获取系统日志
**URL:** /admin/api/auditAndLogger/systemLog  
**方法:** POST  
**需求权限:** viewAudit  
**请求参数:**
___