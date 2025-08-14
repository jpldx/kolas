def copy_properties(source, target, exclude=None):
    """
    将源对象的属性拷贝到目标对象

    :param source: 源对象
    :param target: 目标对象
    :param exclude: 要排除的属性列表，默认为None
    """
    if exclude is None:
        exclude = []

    # 遍历源对象的所有属性
    for attr in vars(source):
        # 跳过需要排除的属性
        if attr not in exclude:
            # 将属性值赋给目标对象
            setattr(target, attr, getattr(source, attr))

