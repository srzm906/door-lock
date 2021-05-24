#                            门禁开发文档

## 安装环境
### 1. 树莓派python安装包：
#### 更新树莓派
sudo apt-get update  

sudo apt-get dist-upgrade
  
  更新时间受网络和设备影响，时间较长。
#### 安装包
pip3 install pymysql(python2为pip)
    
sudo pip install pyfingerprint
    
    
    
    
    
    
### 2. 指纹模块和RFID资料:
   - [指纹模块](https://github.com/bastianraschke/pyfingerprint)
   - [RFID模块](https://www.basemu.com/rc522-rfid-tag-reading-with-the-raspberry-pi-1.html)


## 指纹

### 1. 指纹录入
- finger_enroll.py
### 2. 指纹搜索
- finger_search.py
### 3. 指纹删除
- finger_delete.py
### 4. 指纹数据上传

- finger_upload_data.py

### 5. 指纹数据下载

- finger_download_data.py

## RFID

### 1. 校园卡ID注册
- mfrc_register.py
### 2. 校园卡ID搜索
- mfrc_search.py


## 服务器
### 1. 服务器位置
- 门锁/server.py
# door-lock
# door-lock
