import nlu
pipe = nlu.load('embed_sentence.bert')
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
e_col = "embed_sentence_bert_embeddings"
import pandas as pd



#function that will print most similar answer
def similar_answer_finder(sim_mat, df , question):
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
def get_sim_df_for_iloc(question_predictions, faq_questions_predictions, e_col=e_col , question):
  #This sentence calculates distance for each iloc positions
  #putting embeddings into matrix
  all_faq_questions = [];
  all_faq_answers = []

  dataframe = {'questions' : all_faq_questions , 'answers' : all_faq_answers}
  df=pd.DataFrame(dataframe)
  embed_mat = np.array([x for x in faq_questions_predictions[e_col]])
  question_mat = np.array([x for x in question_predictions[e_col]])
  #calculate distance between every pair  
  sim_mat = cosine_similarity(question_mat, embed_mat)
  similar_answer_finder(sim_mat, df , question)





def predict_similar_questions(question , faqquestions):
    #Doing embedding of questions

    question_predictions = pipe.predict(question , output_level='document')
    print(question_predictions)

    #Doing embeddings of all FAQ questions
    faq_questions_predictions = pipe.predict(faqquestions , output_level='document')
    sim_df_for_one_sent = get_sim_df_for_iloc(question_predictions, faq_questions_predictions, e_col , question)
    print("Done question matching")
    return 1
    