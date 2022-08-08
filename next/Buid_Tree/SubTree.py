import re

import spacy


class Node:
    def __init__(self, noun, noun_type=None, parent=None):
        self.value = noun
        self.enum = None
        self.type = noun_type
        self.parent = parent
        self.child = []
        self.reference = None  # 只有出现一对多的关系（T cases|->a case）时，在T cases这个树的这个属性标记为self.reference="a case"

class SubTree:
    def __init__(self):
        self.root = None
        self.leaf = None
        self.node_name_list = []
        self.node_list = []

    """在当叶子节点处，增加子节点"""
    def add_child(self, noun):
        node = Node(noun, find_type(noun))
        self.node_list.append(node)
        if self.root is None:
            self.root = node
            self.leaf = node

        else:
            queue = [self.leaf]
            while queue:
                cur = queue.pop(0)
                cur.child.append(node)
                node.parent = cur
                self.leaf = node
        self.node_name_list.append(node.value)

    """打印出树结构"""
    # def dump(self, indent=0):
    #     if indent > 0:
    #         try:
    #             tab = "     " * (indent - 1) + "|-"
    #             print("%s%s" % (tab, self.node_name_list[indent]))
    #             self.dump(indent + 1)
    #         except:
    #             pass
    #     noun_pharse_get:
    #         tab = ""
    #         print("%s%s" % (tab, self.node_name_list[indent]))
    #         self.dump(indent + 1)

    # def dump(self, cur_node, indent=0):
    #     if indent > 0:
    #         try:
    #             tab = "     " * (indent - 1) + "|-"
    #             o = []
    #             for obj in cur_node:
    #                 o.append(obj.value)
    #             print("%s%s" % (tab, o))
    #             for obj in cur_node:
    #                 self.dump(obj.child, indent + 1)
    #         except:
    #             pass
    #     noun_pharse_get:
    #         tab = ""
    #         print("%s%s" % (tab, cur_node.value))
    #         self.dump(cur_node.child, indent + 1)

    """获取指定node名称的 node节点"""
    def get_node(self, node_name):
        for node in self.node_list:
            if node_name == node.value:
                return node

    """在指定节点处，添加子节点"""
    def cur_add_node(self, cur_node_name, subtree):
        cur_node = self.get_node(cur_node_name)
        # print(cur_node.child[0].value)
        cur_node.child.append(subtree.root)
        self.node_list.extend(subtree.node_list)
        self.node_name_list.extend(subtree.node_name_list)
        # print(cur_node.child[1].value)
        subtree.root.parent = cur_node
        # print(subtree.root.parent.value)


"""查找关键短语中是否有 数据类型"""
def find_type(key_phrase):
    def_type = ["integer", "string", "character", "char", "int", "boolean", "characters", "integers", "strings"]
    for tp in def_type:
        if tp in key_phrase:
            return tp


def get_subtree():
    all_subtree = []

    """nlp处理数据"""
    nlp = spacy.load("en_core_web_sm")

    text = ["The input contains a single integer T that indicates the number of test cases.",
            "Then follow the T cases.",
            "Each test case begins with a line contains an Integer N, represent the original wall.",
            "Each line contains N characters"]
    # text = ["Create a custom attribute on the project", "the project id is #%1", "key is #%authority", "the value is #%0."]
    for t in text:
        subtree = SubTree()
        t = t.lower()
        doc = nlp(t)
        '''
        each_sent_noun_phrase 记录每个句子的名词短语
        [('The input', 'contains'), ('a single integer T', 'contains'), ...,  ('test cases', 'of')]
        '''
        each_sent_noun_phrase = []
        for np in doc.noun_chunks:
            each_sent_noun_phrase.append((np.text, np.root.head.text))

        key_phrases_tag = ["begins", "contains", "with", "follow"]
        '''
        each_sent_key_phrases 记录每个句子的关键短语
        ['The input', 'a single integer T']
        '''

        for i in each_sent_noun_phrase:
            if i[1] in key_phrases_tag:
                if '#%' in i[0]:
                    node = subtree.node_list[-1]
                    node.enum = i[0][2:]
                else:
                    subtree.add_child(i[0])
        if '#%' in t:
            en = re.findall(r'#%/w+', t)

        all_subtree.append(subtree)
        """
        subtree.dump() 查看子树结构
        “Each test case begins with a line contains an Integer N, represent the original wall.”
        Each test case
            |-a line
                |-an Integer N
    
        print(subtree.node_list) 查看子树所有节点value列表
        ['Each test case', 'a line', 'an Integer N']
        
        print(subtree.root.child[0].value) 查看根节点的第一个子节点（从左到右）的value值
        print(subtree.leaf.parent.value) 查看叶子节点（最后一个叶子节点）的父节点
        """
    return all_subtree

get_subtree()