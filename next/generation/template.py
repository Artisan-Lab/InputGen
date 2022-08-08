from string import Template

class BuildClass:

    """
    class_file_path 生成input结构体（class）的文件目录
    template_file_path 模板的文件目录
    class_name class的名子，即节点的名称（value），驼峰命名
    value_name 节点的名称，全部小写，下划线连接
    value_type 叶子节点存在数据类型
    class_number 节点名称中存在数量词，如the T test cases，对应子节点的test case要生成T个
    """
    def class_code_generation(self, template_file_path, class_name=None,
                              value_name=None, value_type=None, value=None, reference=None, node=None):
        filePath = '../class_struct/pre_class.py'
        class_file = open(filePath, 'a+')

        template_code = []

        # 加载模板文件
        template_file = open('../template/' + template_file_path, 'r')
        tmpl = Template(template_file.read())

        # 模板替换
        '''
        class The_T_Cases:
            def __init__(self):
                self.the_t_cases = None
                self.type="list"
                self.value = []
                self.reference = "Each_Test_Case" 
        '''
        if template_file_path == 'Name_Type_Value_Reference.tmpl':
            template_code.append(tmpl.substitute(
                Class_Name=class_name,
                Value_Name=value_name,
                Type_Name=value_type,
                Reference_Name=reference))
            print('Name_Type_Num   '+class_name)
        # '''
        # class A_Single_Integer_T:
        #     def __init__(self):
        #         self.a_single_integer_t = None
        #         self.type = "integer"
        #         self.value = None
        # '''
        elif template_file_path == 'Name_Type_Value.tmpl':
            template_code.append(tmpl.substitute(
                Class_Name=class_name,
                Value_Name=value_name,
                Type_Name=value_type,
                Value=value))
            print('Name   '+class_name)

        # 将代码写入文件
        class_file.writelines(template_code)
        if node:
            for chi in node.child:
                class_val_list = str(chi.value).split(" ")
                class_value = ""
                for v in range(len(class_val_list)):
                    if v != len(class_val_list) - 1:
                        class_value += (str(class_val_list[v].capitalize()) + "_")
                    else:
                        class_value += str(class_val_list[v].capitalize())

                write_code = '\n        self.{}={}()'.format(class_value, class_value)
                class_file.write(write_code)
        class_file.writelines("\n")
        class_file.close()


# if __name__ == '__main__':
#     build = BuildClass()
#     build.class_init()

