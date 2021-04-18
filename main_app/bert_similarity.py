import os
import nlu
import pandas as pd
import nlu
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sys



# os.environ["JAVA_HOME"] = "C:/Program Files/Java/jdk1.8.0_221"
# os.environ["PATH"] = os.environ["JAVA_HOME"] + "/bin:" + os.environ["PATH"]
# Load dataset and examine dataset, rename columns to questions and answers 
# df = pd.read_csv("/content/drive/My Drive/FAQDataSet.csv")
# df.columns = ["questions" , "answers"]


lst = ['Geeks', 'For', 'Geeks', 'is', 'portal', 'for', 'Geeks']
lst2 = ["ff", "asf", "ahhdabc", "hdjdbnd", "dhajna", "hdffha", "aha"]
df = pd.DataFrame(list(zip(lst, lst2)),columns =['questions', 'answer'])
pipe = nlu.load('embed_sentence.bert')
question = "Is data scientist jobs requires algorithms and data structures?"

#Doing embedding of questions
question_predictions = pipe.predict(question , output_level='document')
print(question_predictions)

#Doing embeddings of all FAQ questions
faq_questions_predictions = pipe.predict(df.questions , output_level='document')
e_col = "embed_sentence_bert_embeddings"

#function that will print most similar answer
def similar_answer_finder(sim_mat, df):
    max_sim = -1
    index_sim = -1
    for index, percent in enumerate(sim_mat[0]):
        print(f"{ percent } {df.iloc[index, 0]}")
    
        if percent > max_sim:
            max_sim = percent
            index_sim = index

    print("\n")
    print(f"Question => {question}")
    print("\n")
    print(f"Retrieved: {df.iloc[index_sim, 0]}")
    print(df.iloc[index_sim , 1])

#This function will give similarity matrix 
def get_sim_df_for_iloc(question_predictions=question_predictions, faq_questions_predictions=faq_questions_predictions, e_col=e_col):
    #This sentence calculates distance for each iloc positions
    #putting embeddings into matrix
    embed_mat = np.array([x for x in faq_questions_predictions[e_col]])
    question_mat = np.array([x for x in question_predictions[e_col]])
    #calculate distance between every pair  
    sim_mat = cosine_similarity(question_mat, embed_mat)
    similar_answer_finder(sim_mat, df)


sim_df_for_one_sent = get_sim_df_for_iloc(question_predictions, faq_questions_predictions, e_col)