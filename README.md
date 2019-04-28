# GetRecentArxivPapers 

## 软硬件要求

### 1.机器内存1GB及以上  2.Ubuntu  3.Python3

# 一.安装 firefox及selenium环境

## 1.安装firefox 

在Ubuntu 16.04 Linux中安装Firefox Quantum 警告：您现有的Firefox安装将升级到Firefox Quantum。在较新的版本中，许多现有的附加组件和扩展组件将不起作用。当然，你可以通过重新安装去掉Quantum，然后返回到较老的，速度较慢的Firefox 56，Mozilla有官方的PPA来安装Firefox Quantum。

打开终端并逐个输入以下命令：

sudo add-apt-repository ppa:mozillateam/firefox-next

sudo apt update && sudo apt upgrade

sudo apt install firefox

## 2.安装geckodriver及selenium

(1)安装python3需要的其他库setuptools、pip

sudo apt install python3-pip

pip3 install setuptools


(3)安装selenium

 pip3  install selenium

## 3.安装geckodriver

默认安装完是支持firefox，但是更新得太慢了，需要安装geckodriver，地址 https://github.com/mozilla/geckodriver/releases/, 找到最新的release地址，x64的，然后用wget下载，然后解压

wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz

tar zxvf geckodriver-v0.24.0-linux64.tar.gz

#安装geckodriver
cp geckodriver /usr/bin

## 4.安装xvfb

 sudo apt-get install xvfb

## 5.安装pyvirtualdisplay

sudo pip3 install pyvirtualdisplay

# 二.安装所需的包

## 1.安装translate

pip3 install translate

## 2.安装google trans

git clone https://github.com/BoseCorp/py-googletrans.git

cd ./py-googletrans

python3 setup.py install

## 3.安装PIL

sudo apt-get install python3-pil

# 三.修改配置

修改arxiv_with_translate.py中的收件人邮箱和发件人的qq邮箱

执行 python3 arxiv_with_translate.py即可



