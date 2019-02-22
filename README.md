#接口自动化测试框架
##介绍
   该自动化测试框架使用excel编写测试用例，通过handleCase类将用例数据解析后，
   循环从数据中调用每一个接口，自动生成excel类型测试报告，适用于单接口，多重关联
   的接口

1. 环境：
   + python3.7
   + mysql 5.7.24
2. 依赖库
   + requests   
   `pip install requests` 
   + xlwd   
   `pip install xlrd`
   + xlwt  
   `pip install xlwt`
   + pymysql  
   `pip install pymysql`
    
3. 使用
   + 用例编写规范
     + 用例使用xlsx 文件(xls 不支持)，文件名case_ 开头作为用例匹配的文件，如case_exmple.xlsx，
       用例统一写在第一张表中
     + 用例编号唯一
     + 接口路径不要带域名，请求方式只能使用小写字母
     + 接口编号与接口路径对应，同一个路径的接口必须使用同一个接口编号
     + 关联接口填写依赖的接口编号
     + 检查点形式：单个检查点以“=”连接，多重json键之间用.隔开多个检查点以“;"隔开（";"为英文
      分号）如：a=4;b=5;c.d=6(表示{"c":{"d":6}})
      数据库期望，目前填写执行sql所期望返回的数据条数
     + 是否执行，不填默认为执行，填y或Y为执行，其余为不执行
     + 参数化：relatedParams有多个时用;隔开，接口参数中需要参数化的字段
      用$+参数名表示，relatedParams中的值与参数名一样，如$name表示name参数
 
4. 运行
    `python newRun.py -env 1`
    + env表示接口测试运行的环境，可选值为0，1，2，默认为2
    + 0:真是环境，1：fp01,2:fp02