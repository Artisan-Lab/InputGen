from next.Buid_Tree.SpecTree import SpecTree
from next.generation.template import BuildClass


spec_tree = SpecTree().spec_tree
# print(spec_tree)
root = spec_tree.root.value
# 用于记录树结构
tag = []

Num_Tag = []
for i in range(65, 91):
    Num_Tag.append(chr(i))

def class_file_path_generation(name):
    return name + '.py'

# """存在问题。。。a single integer T，明显T不是数量，但是处理错误，
# 所以一般来讲数量词会有词性或者存在于短语中前部分，不是最后一个部分"""
# def class_num_generation(name):
#     for n in Num_Tag:
#         if n in name:
#             return n
#         else:
#             return None

# 生成class name
def class_val_generation(class_val):
    class_val_list = str(class_val).split(" ")
    class_value = ""
    for v in range(len(class_val_list)):
        if v != len(class_val_list) - 1:
            class_value += (str(class_val_list[v].capitalize()) + "_")
        else:
            class_value += str(class_val_list[v].capitalize())
    return class_value

# 生成value name
def value_name_generation(class_val):
    class_val_list = str(class_val).split(" ")
    class_value = ""
    for v in range(len(class_val_list)):
        if v != len(class_val_list) - 1:
            class_value += (str(class_val_list[v].lower()) + "_")
        else:
            class_value += str(class_val_list[v].lower())
    return class_value

# 生成class的value，一般基础类型为None，list类型为[]
# 用nltk原生的词形还原部分，对比名词还原前后是否相同
from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()
def value_generation(class_val):
    class_val_list = str(class_val).split(" ")
    for value in class_val_list:
        value = str(value)
        try:
            class_value = wnl.lemmatize(value, 'n')
            if class_value != value:
                return []
        except:
            pass
    return None


def template_file_path_generation(reference):
    if reference:
        return 'Name_Type_Value_Reference.tmpl'
    elif reference is None:
        return 'Name_Type_Value.tmpl'

f = open('../class_struct/pre_class.py',"a")

def recursion_generation_input_code(node):
    self = 0
    parent = 0
    if node.child:  # node节点不是子节点，创建当前节点，然后递归遍历child
        # class_file_path = class_file_path_generation(node.value)
        class_val = node.value
        class_name = class_val_generation(class_val)
        value_name = value_name_generation(class_val)
        value = value_generation(class_val)

        # 不是叶节点,value的type可能为list或者None
        if value == []:
            value_type = "'list'"
        else:
            value_type = None

        referenc = []
        for c in node.child:
            referenc.append(class_val_generation(c.value))

        template_file_path = template_file_path_generation(referenc)
        node_build_class = BuildClass()
        node_build_class.class_code_generation(
            template_file_path=template_file_path,
            class_name=class_name, value_name=value_name,
            value_type=value_type, value=value, reference=referenc, node=node)

        for chi in node.child:
            recursion_generation_input_code(chi)
    else:  # node节点是子节点，填入数据名称和数据类型
        # class_file_path = class_file_path_generation(node.value)
        class_val = node.value
        class_name = class_val_generation(class_val)
        value_name = value_name_generation(class_val)
        value = value_generation(class_val)
        # 不是叶节点没有type
        value_type = node.type
        value_type = '"' + str(value_type) + '"'

        reference = '"' + str(class_val_generation(node.reference)) + '"'
        referenc = None
        if reference != '"None"':
            referenc = reference

        template_file_path = template_file_path_generation(referenc)
        node_build_class = BuildClass()

        node_build_class.class_code_generation(
            template_file_path=template_file_path,
            class_name=class_name, value_name=value_name,
            value_type=value_type, value=value, reference=referenc)

recursion_generation_input_code(spec_tree.root)
