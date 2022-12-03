# importing modules
import nltk
# nltk.download()
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
# from string import punctuation
from zhon.hanzi import punctuation
import string


# ps = PorterStemmer() #creating an instance of the class

# sentence = "Runners have planned for 20km run. Previously, they ran a 15km run up." #sentence to be stemmed

# def string_stream_stem(string_stream):
#     threshhold = 5
#     dicts={i:' ' for i in punctuation}
#     for i in string.punctuation:
#         dicts[i] = " "
#     punc_table=str.maketrans(dicts)
#     string_stream=string_stream.translate(punc_table)
#     ps = PorterStemmer()
#     words_of_stream = word_tokenize(string_stream)
#     words_map = {}
#     stem_string = ""
#     stop_words = set(stopwords.words("english"))
#     filtered_sentence = [ps.stem(w) for w in words_of_stream if not w in stop_words]
#     filtered_sentence = nltk.pos_tag(filtered_sentence) 
#     for str_pair in filtered_sentence:
#         if (str_pair[1] == 'NN'     or 
#             str_pair[1] == 'NNP'    or 
#             str_pair[1] == 'NNS'    or 
#             str_pair[1] == 'NNPS'
#             ):
#             stem_string += (str_pair[0] + " ")
#             if(words_map.get(str_pair[0]) == None):
#                 words_map[str_pair[0]] = 1
#             else:
#                 words_map[str_pair[0]] += 1

#     return (words_map, stem_string)


def string_stream_stem(string_stream, threshhold=5):
    dicts={i:' ' for i in punctuation}
    for i in string.punctuation:
        dicts[i] = " "
    punc_table=str.maketrans(dicts)
    string_stream=string_stream.translate(punc_table)
    ps = PorterStemmer()
    words_of_stream = word_tokenize(string_stream)
    words_map = {}
    stem_string = ""
    stop_words = set(stopwords.words("english"))
    filtered_sentence = [ps.stem(w) for w in words_of_stream if not w in stop_words]
    filtered_sentence = nltk.pos_tag(filtered_sentence) 
    for str_pair in filtered_sentence:
        if (str_pair[1] == 'NN'     or 
            str_pair[1] == 'NNP'    or 
            str_pair[1] == 'NNS'    or 
            str_pair[1] == 'NNPS'
            ):
            if(words_map.get(str_pair[0]) == None):
                words_map[str_pair[0]] = 1
            else:
                words_map[str_pair[0]] += 1
    for word in words_map:
        if(words_map[word] >= threshhold):
            stem_string += (word + " ")
    new_map = sorted(words_map.items(),  key=lambda d: d[1], reverse=True)
    new_words_map = {}
    for word in new_map:
        new_words_map[word[0]] = words_map[word[0]]

    return (new_words_map, stem_string)

# words = word_tokenize(sentence) #tokenizing the words of a sentence

# #printing the results of stemming the words of a sentence
# for x in words:
#     print(x, " : ", ps.stem(x))

# map_of_words = {}
# for x in words:
#     if(map_of_words.get(x) == None):
#         map_of_words[x] = 1
#     else:
#         map_of_words[x] += 1

# print(map_of_words)


# example_sent = "This is a sample sentence, showing off the stop words filtration."

# stop_words = set(stopwords.words('english')) 

# word_tokens = word_tokenize(example_sent) 

# filtered_sentence = [w for w in word_tokens if not w in stop_words] 

# print(word_tokens) 
# print(filtered_sentence)

# import nltk

# line = 'i love this world which was beloved by all the people here'

# tokens = nltk.word_tokenize(line)

# # ['i', 'love', 'this', 'world', 'which', 'was', 'beloved', 'by',

# # 'all', 'the', 'people', 'here']

# pos_tags = nltk.pos_tag(tokens)

# # [('i', 'RB'), ('love', 'VBP'), ('this', 'DT'), ('world', 'NN'), ('which', 'WDT'),

# # ('was', 'VBD'), ('beloved', 'VBN'), ('by', 'IN'), ('all', 'PDT'), ('the', 'DT'),

# # ('people', 'NNS'), ('here', 'RB')]

# for word,pos in pos_tags:
#     if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
#         print(word, pos)




