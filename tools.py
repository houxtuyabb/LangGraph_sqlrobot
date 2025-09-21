import os
import json
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pymysql
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from pydantic import BaseModel, Field


load_dotenv(override=True)
search_tool = TavilySearch(max_results=5)


class SQLQuerySchema(BaseModel):
    sql_query: str = Field(description="SQL查询")


@tool("sql_query", args_schema=SQLQuerySchema)
def sql_inter(sql_query: str):
    """
    当用户需要进行数据库查询工作时，请调用该函数。
    该函数用于在指定MySQL服务器上运行一段SQL代码，完成数据查询相关工作，
    并且当前函数是使用pymsql连接MySQL数据库。
    本函数只负责运行SQL代码并进行数据查询，若要进行数据提取，则使用另一个extract_data函数。
    :param sql_query: 字符串形式的SQL查询语句，用于执行对MySQL中telco_db数据库中各张表进行查询，并获得各表中的各类相关信息
    :return：sql_query在MySQL中的运行结果。
    """

    load_dotenv(override=True)
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    database = os.getenv("DATABASE")

    try:
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            charset="utf8mb4",)

        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    finally:
        if 'conn' in locals():
            conn.close()

    return json.dumps(result, ensure_ascii=False)


class ExtractQuerySchema(BaseModel):
    sql_query : str = Field(description="SQL查询语句")
    df_name: str = Field(description="数据结果")


@tool("extract_data", args_schema=ExtractQuerySchema)
def extract_data(sql_query: str, df_name: str):
    """
    用于在MySQL数据库中提取一张表到当前Python环境中，注意，本函数只负责数据表的提取，
    并不负责数据查询，若需要在MySQL中进行数据查询，请使用sql_inter函数。
    同时需要注意，编写外部函数的参数消息时，必须是满足json格式的字符串，
    :param sql_query: 字符串形式的SQL查询语句，用于提取MySQL中的某张表。
    :param df_name: 将MySQL数据库中提取的表格进行本地保存时的变量名，以字符串形式表示。
    :return：表格读取和保存结果
    """

    load_dotenv(override=True)
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    database = os.getenv("DATABASE")

    try:
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            charset="utf8mb4",)


        df = pd.read_sql(sql_query, con=conn)
        globals()[df_name] = df
        return f"成功将{df_name}保存到当前环境中"

    except Exception as e:
        return f"提取数据失败：{e}"

    finally:
        if 'conn' in locals():
            conn.close()


class PythonCodeInput(BaseModel):
    py_code: str = Field(description="Python代码")


@tool(args_schema=PythonCodeInput)
def python_inter(py_code):
    """
    当用户需要编写Python程序并执行时，请调用该函数。
    该函数可以执行一段Python代码并返回最终结果，需要注意，本函数只能执行非绘图类的代码，若是绘图相关代码，则需要调用fig_inter函数运行。
     """
    g = globals()
    try:
        result = str(eval(py_code, g))
        return result

    except Exception as e:
        global_vars_before = set(g.keys())

        try:
            exec(py_code, g)
        except Exception as e:
            return f"执行代码失败：{e}"

        global_vars_after = set(g.keys())
        new_vars = global_vars_after - global_vars_before
        if new_vars:
            result = {var: g[var] for var in new_vars}
            return str(result)
        else:
            return "执行代码成功，但未创建新变量"


class FigCodeInput(BaseModel):
    py_code: str = Field(description="Python代码")
    fname: str = Field(description="图片文件名")


@tool(args_schema=FigCodeInput)
def fig_inter(py_code: str, fname: str):
    """
    当用户需要使用 Python 进行可视化绘图任务时，请调用该函数。
     """

    current_backend = matplotlib.get_backend()
    matplotlib.use("Agg")

    local_vars = {"plt": plt, "pd":pd, "sns":sns}
    base_dir = r"E:\Langchain项目"
    images_dir = os.path.join(base_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    try:
        g = globals()
        exec(py_code, g, local_vars)
        g.update(local_vars)

        fig = local_vars.get(fname,None)
        if fig:
            image_filename = f"{fname}.png"
            abs_path = os.path.join(images_dir, image_filename)#绝对路径
            rel_path = os.path.join("images", image_filename)#相对路径

            fig.savefig(abs_path,bbox_inches='tight')
            return f"图片已保存至{rel_path}"
        else:
            return "未找到指定的图表对象"
    except Exception as e:
        return f"生成图片失败：{e}"
    finally:
        plt.close('all')
        matplotlib.use(current_backend)