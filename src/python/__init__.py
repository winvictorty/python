"""python package.

Python 代码
"""

from bigmodule import I

# metadata
# 模块作者
author = "BigQuant"
# 模块分类
category = "自定义模块"
# 模块显示名
friendly_name = "运行Python代码"
# 文档地址, optional
doc_url = "https://bigquant.com/wiki/"
# 是否自动缓存结果
cacheable = True


DEFAULT_RUN = """# Python 代码入口函数，input_1/2/3 对应三个输入端，data_1/2/3 对应三个输出端
def bigquant_run(input_1, input_2, input_3):
    # 示例代码如下。在这里编写您的代码

    import dai

    df = input_1.read()
    ds = dai.DataSource.write_bdb(df)

    return dict(data_1=ds, data_2={"hello": "world"}, data_3=None)
"""

DEFAULT_POST_RUN = """# 后处理函数，可选。输入是主函数的输出，可以在这里对数据做处理，或者返回更友好的outputs数据格式。此函数输出不会被缓存。
def bigquant_run(outputs):
    return outputs
"""


def run(
    run: I.code("主函数，返回dict对象", I.code_python, default=DEFAULT_RUN, specific_type_name="函数", auto_complete_type="python"),
    post_run_outputs_: I.code(
        "后处理函数，输入是主函数的输出，此函数输出不会被缓存", I.code_python, default=DEFAULT_POST_RUN, specific_type_name="函数", auto_complete_type="python"
    ) = None,
    input_1: I.port("输入1，传入到函数的参数 input_1", optional=True) = None,
    input_2: I.port("输入2，传入到函数的参数 input_2", optional=True) = None,
    input_3: I.port("输入3，传入到函数的参数 input_3", optional=True) = None,
) -> [
    I.port("输出1，对应函数输出的 data_1", "data_1", optional=True),
    I.port("输出2，对应函数输出的 data_2", "data_2", optional=True),
    I.port("输出3，对应函数输出的 data_3", "data_3", optional=True),
]:
    """执行任意Python代码，支持缓存加速。"""

    return I.Outputs(**run(input_1, input_2, input_3))


def post_run(outputs):
    if hasattr(outputs, "post_run_outputs_"):
        outputs = outputs.post_run_outputs_(outputs)
        del outputs.post_run_outputs_

    return outputs
