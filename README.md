# InputGen
InputGen是一个基于非结构化自然语言描述自动生成测试用例的工具，并且后续可以应用于REST API的自动化需求测试。

InputGen主要功能是根据需求描述挖掘测试用例的格式信息，然后根据预定义的规则将输入信息组合成信息树的结构。具体步骤可以分为：名词短语提取、关键短语挖掘、信息树生成、测试用例结构代码生成、测试用例生成。

## 使用说明

1.首先将需求描述放到./next/Build_Tree/requirements文件夹下，UTF-8编码。

2.运行./next/generation/class_generation.py文件，可以生成信息树所对应的结构体文件。 
```bash
python3 class_generation.py
```
3.结构体文件生成在./next/pre_class.py文件，可以自行查看。

4.运行./next/generation/test_case_generation.py文件，最终会生成需求对应的具体测试用例。
```bash
python3 test_case_generation.py
```
