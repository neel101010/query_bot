import nlu
import numpy as np
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
e_col = "embed_sentence_bert_embeddings"
import pandas as pd


pipe = nlu.load('embed_sentence.bert')

e_col = "embed_sentence_bert_embeddings"



# function that will print most similar answer
def similar_answer_finder(sim_mat, df , question):
  max_sim = -1
  index_sim = -1
  for index, percent in enumerate(sim_mat):
    print(f"{ percent } {df.iloc[index, 0]}")
  
    if percent > max_sim:
      max_sim = percent
      index_sim = index

  dataObj = {}
  if max_sim[0] < 0.8 :
    dataObj = {
      "percentmatched" : max_sim[0],
      "ismatched" : False,
      "question" : question,
      "matchedquestion" : "",
      "matchedanswer" : ""
    }
  else:
    matchedquestion = df.iloc[index_sim, 0]
    matchedanswer = df.iloc[index_sim , 1]
    dataObj = {
      "percentmatched" : max_sim[0],
      "ismatched" : True,
      "question" : question,
      "matchedquestion" : matchedquestion,
      "matchedanswer" : matchedanswer
    }
  
  print("\n\n")
  print(dataObj)
  return dataObj
  




#This function will give similarity matrix 
def get_sim_df_for_iloc(question_predictions, faq_questions_predictions, question , df , e_col=e_col ):
  
  embed_mat = np.array([x for x in faq_questions_predictions[e_col]])
  question_mat = np.array([x for x in question_predictions[e_col]])
  print(embed_mat)
  print(question_mat)
  sim_mat = cosine_similarity(embed_mat, question_mat)
  dataObj = similar_answer_finder(sim_mat, df , question)
  return dataObj




def predict_similar_questions(question , allQuestions , allAnswers):
    # Doing embedding of questions
    question_predictions = pipe.predict(question , output_level='document')
    print(question_predictions)
    
    dataframe = {'questions' : allQuestions , 'answers' : allAnswers}
    df=pd.DataFrame(dataframe)
    # Doing embeddings of all FAQ questions
    faq_questions_predictions = pipe.predict(df.questions , output_level='document')
    print("getting ==>" , faq_questions_predictions["embed_sentence_bert_embeddings"])
    sim_df_for_one_sent = get_sim_df_for_iloc(question_predictions, faq_questions_predictions, question ,df ,  e_col)
    print("Done question matching")
    print(sim_df_for_one_sent)
    return sim_df_for_one_sent
    