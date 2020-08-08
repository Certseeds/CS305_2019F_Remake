<!--
 * @Github: https://github.com/Certseeds/CS305_2019F_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-19 16:06:56
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-08-08 23:08:32
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## <div>CS305 Computer Network</div>
## <div>Report_Lab13</div>
**SID**:  \*\*\*\*\*\*\*\*   
**Name**:  nanoseeds  

### Question 1
1. 首先,使用pc和2560-switch建立结构如图所示的网络 
2. 将其整体复制,粘贴,使用时间加速,其则为图中形状 测试ping mac地址.
3. 若通,则继续复制,直到有三份结构相同的网络.(一份原来的,三份复制品,测试用)
4. 对测试品一来说,使用  
“enable  
Show spanning-tree”  
获取spanning-tree root 为下方的switch  
5. 对测试品二来说,获取spanning-root  
关闭switch5的Fa 0/3,yellow spot change,  
Spanning-tree root 没有发生变化  
6. 对复制品3来说,重复二的步骤  
对左侧switch,  
“enable  
Spanning-tree vlan 1 priority 8192   
Show spanning-tree  
”即可发现其变为了root(或者使用spanning-tree vlan 1 root primary)
这样,一二三四就全部满足了.  

### Question 2 
参考[博客园的文章](https://www.cnblogs.com/mchina/archive/2012/07/14/2591598.html)  
1. 首先,建立如图所示网络  
2. 其次,整体复制,粘贴,时间加速,使其为图中形状,  
3. 对复制体1,  
完成步骤一后,can not ping each other.  
设定好ip address,mask,gateway之后,  
分别使用  
vlan 10, exit  
vlan 20, exit  
inter fa 0/1, switch acc vlan 10 ,exit  
inter fa 0/2, switch acc vlan 20 ,exit  
之后,进行测试,完全不通.
4. 对复制体2,进行如上操作,
对每一个2960,
Enable  
Conf ter	  
Inter fa 0/3  
Switchport mode trunk  
End
5. 
同样,建立vlan 10,vlan 20
分别对interface vlan 10/20 配置
ip address 192.168.10.254 255.255.255.0 
ip routing
结束.

<div>
  <img src="Path_Of_Picture"><br />
  <div>Some details</div>
</div>
<style type="text/css">
div{
  text-align: center;
}
div>div {
  text-align: center;
  border-bottom: 1px solid #d9d9d9;
  display: inline-block;
  padding: 2px;
}
div>img{
  border-radius: 0.3125em;
  box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);
}
</style>