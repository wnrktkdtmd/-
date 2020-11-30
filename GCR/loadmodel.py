# -*- coding: utf-8 -*-
from gensim.models.doc2vec import Doc2Vec
from konlpy.tag import Okt
import json
from numpy import dot
from numpy.linalg import norm
import pickle
import re

model = Doc2Vec.load('model.doc2vec')
okt = Okt()

#with open('doctags.pickle', 'rb') as f:
#	doctags = pickle.load(f) # 단 한줄씩 읽어옴

vector_docs = model.docvecs.vectors_docs
doctags = []
for i, docvec in enumerate(vector_docs):
	tag = model.docvecs.index_to_doctag(i)
	doctags.append([tag, docvec])


stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

def preprocessing(text):
    # 개행문자 제거
    text =  str(text).strip('\t\n\r')
    pattern = re.compile(r'\s+')
    text = re.sub(pattern, ' ', str(text))
    # 특수문자 제거
    # 특수문자나 이모티콘 등은 때로는 의미를 갖기도 하지만 가사 처리에는 필요없다
    # text = re.sub('[?.,;:|\)*~`’!^\-_+<>@\#$%&-=#}※]', '', text)
    # 한글, 영문, 숫자만 남기고 모두 제거한다
    # text = re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9]', ' ', text)
    # 한글, 영문만 남기고 모두 제거한다
    text = re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z]', ' ', str(text))
    return text

def testData_preprocess(text):
    temp = preprocessing(text)
    temp_token = []
    temp_token = okt.morphs(temp, stem=True) # 토큰화
    temp_token = [word for word in temp_token if not word in stopwords]
    return temp_token

def cos_sim(A, B):
       return dot(A, B)/(norm(A)*norm(B))

def get_most_similar(docvec, topn=10):
    tag_similarity = []

    for i in range(len(doctags)):
        tag_similarity.append([doctags[i][0], cos_sim(docvec, doctags[i][1])])

    sorted_by_sim = sorted(tag_similarity, key=lambda tag_similarity: tag_similarity[1], reverse=True)

    return sorted_by_sim[:topn]

def get_title_1(title, topn=10): # 제목으로 가져오기
    result = []
    try: # 입력한 제목이 기존 태그에 있을 경우
        result = get_most_similar(model.docvecs[title], topn=topn)
    except: # 입력한 제목이 기존 태그에 없을 경우 (결과의 성능 보장 X)
        result = get_most_similar(model.infer_vector([title]), topn=topn)

    return result

def get_title_2(text, topn=10): # 문장으로 가져오기
    tokens = testData_preprocess(text)
    infered_vec = model.infer_vector(tokens)
    result = get_most_similar(infered_vec, topn)
    return result


def result_to_string(result):
	ret = ''

	for i in result:
		ret += i[0] + '@'
	return json.dumps(ret, ensure_ascii=False)




def find_(string, num = '10', sentense = '0'):
	if sentense == '0':
		l = get_title_1(string, int(num))
	elif sentense == '1':
		l = get_title_2(string, int(num))

	ret = ''

	for i in l:
		ret += i[0] + '@'
	
	return json.dumps(ret, ensure_ascii=False)
