#-*- coding: UTF-8 -*-
# @Time    : 2019/4/14 13:21
# @Author  : xiongzongyang
# @Site    : 
# @File    : question_template.py
# @Software: PyCharm

'''



9:nnt 参演评分 小于 x
10:nnt 电影类型
11:nnt nnr 合作 电影列表
12:nnt 电影数量
13:nnt 出生日期
'''
from query import Query
import re

class QuestionTemplate():
    def __init__(self):
        self.q_template_dict={
            0:self.get_bp,
            1:self.get_numberofchild,
            2:self.get_sibling,
            3:self.get_birthname,
            4:self.get_father,
            5:self.get_birthdate,
            6:self.get_haircolor,
            7:self.get_author,
            8:self.get_spouse,
            9:self.get_movie_rating_smaller,
            10:self.get_actor_movie_type,
            11:self.get_cooperation_movie_list,
            12:self.get_actor_movie_num,
            13:self.get_actor_birthday
        }

        # 连接数据库
        self.graph = Query()
        # 测试数据库是否连接上
        # result=self.graph.run("match (m:Movie)-[]->() where m.title='卧虎藏龙' return m.rating")
        # print(result)
        # exit()

    def get_question_answer(self,question,template):
        # 如果问题模板的格式不正确则结束
        assert len(str(template).strip().split("\t"))==2
        template_id,template_str=int(str(template).strip().split("\t")[0]),str(template).strip().split("\t")[1]
        self.template_id=template_id
        self.template_str2list=str(template_str).split()

        # 预处理问题
        question_word,question_flag=[],[]
        for one in question:
            word, flag = one.split("/")
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        assert len(question_flag)==len(question_word)
        self.question_word=question_word
        self.question_flag=question_flag
        self.raw_question=question
        # 根据问题模板来做对应的处理，获取答案
        answer=self.q_template_dict[template_id]()
        return answer

    # 获取电影名字
    def get_movie_name(self):
        ## 获取nm在原问题中的下标
        tag_index = self.question_flag.index("nm")
        ## 获取电影名称
        movie_name = self.question_word[tag_index]
        return movie_name
    def get_name(self,type_str):
        name_count=self.question_flag.count(type_str)
        if name_count==1:
            ## 获取nm在原问题中的下标
            tag_index = self.question_flag.index(type_str)
            ## 获取电影名称
            name = self.question_word[tag_index]
            return name
        else:
            result_list=[]
            for i,flag in enumerate(self.question_flag):
                if flag==str(type_str):
                    result_list.append(self.question_word[i])
            return result_list

    def get_num_x(self):
        x = re.sub(r'\D', "", "".join(self.question_word))
        return x
    # 0:PERSON birthplace
    def get_bp(self):
        actor_name = self.get_name('PERSON')
        
     #   cql = f"match(n:Person)-[]->() where n.name='{actor_name}' return n.birthplace"
        cql = f"MATCH (n) WHERE (n.name='{actor_name}') RETURN n.birthplace"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = actor_name+"'s birthplace is "+answer+"."
        return final_answer
    # 1:PERSON numberofchildren
    def get_numberofchild(self):
        actor_name = self.get_name('PERSON')
        cql = f"MATCH (n) WHERE (n.name='{actor_name}') RETURN n.childrennumber"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = answer
        return final_answer
    # 2:PERSON sibling
    def get_sibling(self):
        actor_name = self.get_name('PERSON')
        cql = f"MATCH (n) WHERE (n.name='{actor_name}') RETURN n.sibling"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = answer
        return final_answer
    # 3:PERSON birthname
    def get_birthname(self):
        actor_name = self.get_name('PERSON')
        cql = f"MATCH (n) WHERE (n.name='{actor_name}') RETURN n.birthname"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = answer
        return final_answer
    # 4:PERSON father
    def get_father(self):
        actor_name = self.get_name('PERSON')
        cql = f"MATCH (n) WHERE (n.name='{actor_name}') RETURN n.father"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = answer
        return final_answer
    # 5:PERSON birthdate
    def get_birthdate(self):
        actor_name = self.get_name('PERSON')
        cql = f"MATCH (n) WHERE (n.name='{actor_name}') RETURN n.birthdate"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = answer
        return final_answer
    # 6:PERSON haircolor
    def get_haircolor(self):
        actor_name = self.get_name('PERSON')
        cql = f"MATCH (n) WHERE (n.name='{actor_name}') RETURN n.haircolor"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = answer
        return final_answer
    # 7:PERSON author
    def get_author(self):
        work_name = self.get_name('WORK_OF_ART')

        cql = f"MATCH (n) WHERE (n.work=~'.*{work_name}.*') RETURN n.name"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = answer
        return final_answer
    # 8:PERSON spouse
    def get_spouse(self):
        actor_name = self.get_name('PERSON')
        cql = f"MATCH (n) WHERE (n.name='{actor_name}') RETURN n.spouse"
        print(cql)
        answer = self.graph.run(cql)
        final_answer = answer
        return final_answer

    # 8:nnt 参演评分 大于 x
    def get_movie_rating_bigger(self):
        actor_name=self.get_name('nr')
        x=self.get_num_x()
        cql = f"match(n:Person)-[r:actedin]->(m:Movie) where n.name='{actor_name}' and m.rating>={x} return m.title"
        print(cql)
        answer = self.graph.run(cql)
        answer = "、".join(answer)
        answer = str(answer).strip()
        final_answer=actor_name+"演的电影评分大于"+x+"分的有"+answer+"等！"
        return final_answer
    def get_movie_rating_smaller(self):
        actor_name = self.get_name('nr')
        x = self.get_num_x()
        cql = f"match(n:Person)-[r:actedin]->(m:Movie) where n.name='{actor_name}' and m.rating<{x} return m.title"
        print(cql)
        answer = self.graph.run(cql)
        answer = "、".join(answer)
        answer = str(answer).strip()
        final_answer = actor_name + "演的电影评分小于" + x + "分的有" + answer + "等！"
        return final_answer
    def get_actor_movie_type(self):
        actor_name = self.get_name("nr")
        # 查询电影名称
        cql = f"match(n:Person)-[]->(m:Movie) where n.name='{actor_name}' return m.title"
        print(cql)
        movie_name_list = list(set(self.graph.run(cql)))
        # 查询类型
        result = []
        for movie_name in movie_name_list:
            movie_name = str(movie_name).strip()
            try:
                cql = f"match(m:Movie)-[r:is]->(t) where m.title='{movie_name}' return t.name"
                # print(cql)
                temp_type = self.graph.run(cql)
                if len(temp_type) == 0:
                    continue
                result+=temp_type
            except:
                continue
        answer = "、".join(list(set(result)))
        print(answer)
        final_answer = actor_name + "演过的电影有" + answer + "等类型。"
        return final_answer
    def get_cooperation_movie_list(self):
        # 获取演员名字
        actor_name_list=self.get_name('nr')
        movie_list={}
        for i,actor_name in enumerate(actor_name_list):
            answer_list=self.get_actorname_movie_list(actor_name)
            movie_list[i]=answer_list
        result_list=list(set(movie_list[0]).intersection(set(movie_list[1])))
        print(result_list)
        answer="、".join(result_list)
        final_answer=actor_name_list[0]+"和"+actor_name_list[1]+"一起演过的电影主要是"+answer+"!"
        return final_answer

    def get_actor_movie_num(self):
        actor_name=self.get_name("nr")
        answer_list=self.get_actorname_movie_list(actor_name)
        movie_num=len(set(answer_list))
        answer=movie_num
        final_answer=actor_name+"演过"+str(answer)+"部电影!"
        return final_answer
    def get_actor_birthday(self):
        actor_name = self.get_name('nr')
        cql = f"match(n:Person)-[]->() where n.name='{actor_name}' return n.birth"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = actor_name+"的生日是"+answer+"。"
        return final_answer
