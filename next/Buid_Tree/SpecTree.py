from next.Buid_Tree.SubTree import get_subtree, SubTree
from nltk.stem import WordNetLemmatizer


"""
关系挖掘：多对一，一对一关系
多对一: the T cases => each test case
一对一: a line <=> each line

关键短语识别改进： 关键词 + 包含输入信息(int, char, string...)
"""
#########################################################
"""
roots一对多关系判断挖掘 return 0 一对多关系 1 多对一关系  
"""
def get_multi_relation(phrase1, phrase2):
    lemmatizer = WordNetLemmatizer()
    phrase1_list = str(phrase1).split(" ")
    phrase2_list = str(phrase2).split(" ")
    lemmatizer1 = []
    lemmatizer2 = []
    map1 = {}
    map2 = {}
    for i in phrase1_list:
        lemmatizer1.append(lemmatizer.lemmatize(i))
    for j in phrase2_list:
        lemmatizer2.append(lemmatizer.lemmatize(j))
    for n in lemmatizer1:
        for m in lemmatizer2:
            if n == m:
                index1 = lemmatizer1.index(n)
                index2 = lemmatizer2.index(m)
                if phrase1_list[index1] != phrase2_list[index2]:
                    map1[phrase1_list[index1]] = n
                    map2[phrase2_list[index2]] = m
    for k in range(len(map1.keys())):
        if list(map1.keys())[k] == list(map1.values())[k] and list(map2.keys())[k] != list(map2.values())[k]:
            return 1

"""
roots一对一关系判断挖掘 return 0 没有一对一关系 1 一对一关系  
"""
single_tag = ["a", "each"]
def get_single_relation(p1, p2):
    p_l1 = str(p1).split(" ")
    p_l2 = str(p2).split(" ")
    flag1 = 0
    flag2 = 0
    for i in p_l1:
        for j in p_l2:
            if i in single_tag and j in single_tag:
                flag1 = 1
                p_l1.remove(i)
                p_l2.remove(j)
    for i in p_l1:
        for j in p_l2:
            if i == j:
                flag2 = 1
    if flag1 == 1 and flag2 == 1:
        return 1

"""
构造规范树 基于Node类
    规则：
        1.首先查看子树的roots中有无the input类似节点，若有则作为规范树根节点，若无则创建根节点value（即name）= the input
        2.再查询所有子树roots，若有"一对多关系"，如the T cases |-> Each test case，则将Each test case作为the T cases的子节点
        3.对于所有不符合step2的句子（即仍是子树的句子），将这些句子的roots中的一个root1去遍历其他roots所代表子树的所有节点，
          如果有"一对一关系"，将这个root加到与其"一对一"节点的父节点上，如Each line == a line，则Each line所在子树加到a line所在子树上
        4.最终所有子树连接到the input节点，形成 Specification Tree，根节点为 the input
"""
class SpecTree:
    """
    root list 存储所有初始子树的根节点的value
    subtree_tag 以list的形式标记是否为the input子树   1 表示仍为独立子树 -1 表示为the input子树
    input_tag 用于识别roots中是否有the input,etc作为一个需求对应的规范树的root
    """
    def __init__(self):
        self.all_subtree = get_subtree()
        self.root_list = []
        self.node_list = []
        self.map = {}
        self.subtree_tag = []
        self.input_tags = ["the input", "The input"]
        for i in range(len(self.all_subtree)):
            self.root_list.append(self.all_subtree[i].root.value)
            self.node_list.extend(self.all_subtree[i].node_name_list)
            self.map[self.all_subtree[i].root.value] = self.all_subtree[i]
            self.subtree_tag.append(1)
        self.step1()
        self.step2()
        self.step3()
        self.spec_tree = self.step4()

    # def dump(self):
    #     for subtree in self.all_subtree:
    #         subtree.dump()

    """返回the input子树"""
    def get_input_subtree(self):
        return self.all_subtree[self.subtree_tag.index(-1)]

    """第一步，flag用于判断在root根节点的list中是否存在the input节点，不存在则flag=0，创建新子树"""
    def step1(self):
        flag = 0
        for root_value in self.root_list:
            if root_value in self.input_tags:
                index = self.root_list.index(root_value)
                self.subtree_tag[index] = -1
                flag = 1
        """创建新子树"""
        if flag == 0:
            the_input_subtree = SubTree()
            the_input_subtree.add_child("the input")
            self.all_subtree.append(the_input_subtree)
            self.root_list.append(the_input_subtree.root.value)
            self.map[the_input_subtree.root.value] = the_input_subtree
            self.subtree_tag.append(-1)

    # 这里可以优化~
    def step2(self):
        # 注：为避免边遍历边移动数组出现错误，遍历复制数组，修改原数组
        root_list = self.root_list[:]
        for root_name in root_list:  # root 节点加到 node节点
            for node_name in self.node_list:  # node节点（包含root）
                """存在一对多关系，改动：
                    1.子树root add到子树node上 
                    2.all_subtree中移除add的子树
                    3.root列表移除子树root的名称
                    4.子树标记列表将子树root移除
                """
                if get_multi_relation(root_name, node_name) == 1:
                    for subtree in self.all_subtree:
                        if node_name in subtree.node_name_list:
                            subtree.cur_add_node(node_name, self.map[root_name])
                            subtree.root.reference = root_name
                    self.all_subtree.remove(self.map[root_name])
                    self.subtree_tag.pop(self.root_list.index(root_name))
                    self.root_list.remove(root_name)

    """将root节点加到与其有一对一关系的节点（非root）的parent节点下"""
    def step3(self):
        subtree_tag = self.subtree_tag[:]
        num = 0
        for i in range(len(subtree_tag)):
            if subtree_tag[i] == 1:
                for node_name in self.node_list:  # node节点（包含root）
                    # node节点不是根节点且node不在root这个子树上，则root可以做一对一关系识别，若成功，则加到对应node的parent节点上
                    if node_name not in self.root_list and node_name not in self.all_subtree[i - num].node_list:
                        if get_single_relation(self.root_list[i - num], node_name) == 1:  # 识别成功
                            subtree = self.all_subtree[i - num]  # 当前subtree中tag为1的子树
                            # 子树要加到node_name的节点上  node是一定存在的
                            # node = None
                            # node_name_subtree = None
                            for node_name_subtree in self.all_subtree:
                                if node_name in node_name_subtree.node_name_list:
                                    node = node_name_subtree.get_node(node_name)
                                    # print(node_name)
                                    # print(self.root_list[i - num])
                                    parent_name = node.parent.value
                                    # print(parent_name)
                                    # node_name_subtree是当前parent的子树，subtree是root对应的子树
                                    node_name_subtree.cur_add_node(parent_name, subtree)
                                    self.all_subtree.remove(subtree)
                                    self.root_list.remove(subtree.root.value)
                                    self.subtree_tag.pop(i - num)
                            num += 1

    def step4(self):
        the_input_subtree = self.get_input_subtree()
        root = the_input_subtree.root  # Specification Tree的根节点
        for i in range(len(self.subtree_tag)):
            if self.subtree_tag[i] == 1:
                the_input_subtree.cur_add_node(root.value, self.all_subtree[i])
        return the_input_subtree


# if __name__ == '__main__':
#     s = SpecTree()
#     print(s.subtree_tag)
#     print(s.spec_tree)

