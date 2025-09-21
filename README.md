SQL Robot
一个基于LangChain和LangGraph的智能SQL助手，能够连接MySQL数据库执行查询、提取数据、执行Python代码和生成可视化图表。

功能特性
数据库查询 - 使用sql_inter工具执行SQL查询
数据提取 - 使用extract_data工具将数据库表提取到Python环境
Python代码执行 - 使用python_inter工具执行Python代码
数据可视化 - 使用fig_inter工具生成并保存图表
网络搜索 - 集成Tavily搜索功能


环境配置
在使用之前，请确保配置了以下环境变量：

HOST: MySQL服务器地址
PORT: MySQL端口
USER: MySQL用户名
PASSWORD: MySQL密码
DATABASE: 数据库名称
这些变量应配置在项目根目录的.env文件中。

工具说明
sql_inter
执行SQL查询语句并返回结果。

使用场景：当需要查询数据库中的信息时

参数：

sql_query: SQL查询语句
extract_data
从数据库中提取数据表并保存为DataFrame。

使用场景：当需要将整个表或查询结果加载到Python环境中进行分析时

参数：

sql_query: SQL查询语句
df_name: 保存数据的变量名
python_inter
执行Python代码。

使用场景：当需要进行数据分析、计算或其他Python操作时

参数：

py_code: Python代码
fig_inter
生成并保存可视化图表。

使用场景：当需要创建数据可视化图表时

参数：

py_code: 生成图表的Python代码
fname: 图表对象的变量名