from next.class_struct.pre_class import *
import random


# 字典中的key代表class的名字，value代表class有无初始化，0代表没有，1代表有
# class_name = {"The_Input":0, "A_Single_Integer_T":0, "The_T_Cases":0,"Each_Test_Case":0}
# instance_name = ["The_Input", "A_Single_Integer_T", "The_T_Cases", "Each_Test_Case"]
class_name = {}
instance_name = []
def get_class_name_and_instance_name():
    filePath = '../class_struct/pre_class.py'
    f = open(filePath, 'r', encoding='utf-8')
    datas = f.readlines()
    for data in datas:
        if 'class' in data:
            s = data[6:-2]
            class_name[s] = 0
            instance_name.append(s)
# 获取class_name，instance_name
get_class_name_and_instance_name()

# 用于判断每个实例
class_key_list = ["type", "value", "reference"]

# 基本数据类型
type_list = ["integer", "int", "string", "char", "boolean", "character"]
# fuzz
def fuzz(t): # t代表type类型
    li_integer = [7,8,9]
    li_int = [1,2,3]
    li_character = ['a', 'b', 'c']
    if t == "integer":
        return random.choice(li_integer)
    elif t == "int":
        return random.choice(li_int)
    elif t == "character":
        return random.choice(li_character)

# 存储所有生成的测试用例~~~
now_instance_objects = []

# def get_instance_son_dict_parent():
# 实例化class
instance_objects = []
for name in list(class_name.keys()):
    _instance = eval(name + '()')
    instance_objects.append(_instance)

instance_son_dict_parent = {}
# 处理获得每个实例引用了谁，谁被谁引用
# {'A_Single_Integer_T': ['The_Input'], 'The_T_Cases': ['The_Input'], 'Each_Test_Case': ['The_T_Cases']}
for instance_object_index in range(len(instance_objects)):
    dic = instance_objects[instance_object_index].__dict__
    for key in list(dic.keys()):
        if(key != instance_name[instance_object_index].lower()):
            if(key not in class_key_list):
                instance_son_dict_parent[key] = [instance_name[instance_object_index]]

    # return instance_son_dict_parent

# # 先执行一遍，找到具有基本数据类型的class，判断其父节点是否为list类型，若不是则fuzz赋值
# for i in range(len(class_name.keys())):
#     if list(class_name.values())[i] == 0: # 没有被赋值，拿出来看一下class的type是不是基本数据类型
#         instance_object = eval(instance_name[i] + '()')  # 第i个实例化对象
#         _type = instance_object.type
#         if _type in type_list:
#             # 判断父节点类型是否为list
#             # instance_son_dict_parent = get_instance_son_dict_parent()
#             parents = instance_son_dict_parent[instance_name[i]]
#             for parent in parents:
#                 index = instance_name.index(parent)
#                 parent_instance = eval(instance_name[index] + '()')
#                 if parent_instance.type != "list" and instance_object.value != []:
#                     instance_object.value = fuzz(_type)
#                     class_name[instance_name[i]] = 1
#                     now_instance_objects.append(instance_object)


num_tag = {"A_Single_Integer_T":["The_T_Cases"]}  # 选用基本数据类型的class作为key


def generation(now_index):

    # if list(class_name.values())[now_index] == 0: # 没有被赋值
    # 判断当前class对象是否已经实例化，为0是未实例化
    a = list(class_name.values())[now_index]
    if a == 0:
        instance_object = eval(instance_name[now_index] + '()')  # 实例化对象
        '''
          对象的type定义：
              如果是多对一的关系，type为list类型。
              如果是包含对象作为成员变量，则type为None，但是存在reference字段作为引用对象，且value为[]
              如果为基本数据类型，直接对应最终节点，根据类型fuzz  1.如果value为None无需特殊操作
                                                         2.如果value为[]，需要fuzz之后加入list
        '''
        _type = instance_object.type
        if _type == "list":
            # 查看多对一的数量映射关系
            for tag in list(num_tag.keys()):
                if instance_name[now_index] in list(num_tag[tag]):
                    # 获取到 T cases 的 T 值，然后循环遍历T次T cases中的reference代表的对象
                    # 先将class_name中的value改为1
                    class_name[list(class_name.keys())[now_index]] = 1

                    times = 0
                    for i_o in now_instance_objects:
                        if tag == i_o.__class__.__name__:
                            times = i_o.value

                    # times = now_instance_objects[instance_name.index(tag)].value
                    for time in range(times):
                        for refer in instance_object.reference:
                            reference_name = refer
                            _index = instance_name.index(reference_name)
                            inst = generation(_index)
                            instance_object.value.append(inst)
        elif _type == None and instance_object.value == []:
            reference_name = instance_object.reference
            if isinstance(reference_name, list):
                for ref in reference_name:
                    _index = instance_name.index(ref)
                    inst = generation(_index)
                    instance_object.value.append(inst)

        elif _type == None and instance_object.value == None:
            reference_name = instance_object.reference
            if isinstance(reference_name, list):
                for ref in reference_name:
                    _index = instance_name.index(ref)
                    inst = generation(_index)
                    instance_object.value.append(inst)

        elif _type in type_list and instance_object.value == None:
            instance_object.value = fuzz(_type)

        elif _type in type_list and instance_object.value == []:
            value = fuzz(_type)
            instance_object.value.append(value)

        if instance_object not in now_instance_objects:
            now_instance_objects.append(instance_object)
            return instance_object



for j in range(len(class_name.keys())):
    generation(j)

# def sout_value(value_list):
#     for val in value_list:
#         if not isinstance(val.value, list):
#             print(val.value)
#         else:
#             sout_value(val.value)
#
# for i in now_instance_objects:
#     if i.value:
#         if not isinstance(i.value, list):
#             print(i.value)
#         else:
#             sout_value(i.value)


for j in now_instance_objects:
    print(j.value)


# for j in range(len(class_name.keys())):
#     if instance_name[j] == "The_Input":
#         generation(j, 0)
#         break





