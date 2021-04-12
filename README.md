# QuestionAnswerSystem
![](https://github.com/JiajingFang/QuestionAnswerSystem/blob/master/simple_movie_qa_with_KG-master/movie_QA_with_KQ/image.png)
## Setup 
### 0.pip instal modules in requirements.txt<br>
### 1.load the data csv into Neo4j and do the merge and match eg. use person.xls in import folder<br>
remain database in Neo4j running when using the QA<br>
### 2.go to simple_movie_qa_with_KG-master\movie_QA_with_KQ folder <br>
```python
python code.py 127.0.0.1:1234
```
### 3.visit 127.0.0.1:1234 in browser


## Building Process
Language: Python<br>
Database:  Neo4j Knowledge Graph<br>
NLP&NER: SpaCy<br>
Classify:     sklearn.naive_bayes<br>

### data: 
KG is built in neo4j<br> 
Query templates are set in data folder<br>
Query template types are trained<br>
<br>
1.Question Received<br>
2.Tokenizing and NER<br>
3.Match question to certain query template<br>
4.Template function is used to query answer<br>

