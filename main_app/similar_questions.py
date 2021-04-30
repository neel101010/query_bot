import numpy as np
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
e_col = "embed_sentence_bert_embeddings"
import pandas as pd



#function that will print most similar answer
def similar_answer_finder(sim_mat, df , question):
  max_sim = -1
  index_sim = -1
  for index, percent in enumerate(sim_mat):
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
def get_sim_df_for_iloc(question_predictions, faq_questions_predictions, question , df , e_col=e_col ):
  #This sentence calculates distance for each iloc positions
  #putting embeddings into matrix
  # all_faq_questions = ["what is machine learning?" , "what does the role of machine learning and data scientist looks like?" , "what are the requirements of data scientist job?" ]
  # all_faq_answers = ["Absc" ,"Absc" ,"Absc"]

  # dataframe = {'questions' : all_faq_questions , 'answers' : all_faq_answers}
  # df=pd.DataFrame(dataframe)
  embed_mat = np.array([x for x in faq_questions_predictions[e_col]])
  question_mat = np.array([x for x in question_predictions[e_col]])
  print(embed_mat)
  print(question_mat)
  # nsamples, nx, ny = embed_mat.shape
  # d2_train_dataset = embed_mat.reshape((nsamples,nx*ny))
  # nsamples1, nx1, ny1 = question_mat.shape
  # d2_train_dataset1 = question_mat.reshape((nsamples1,nx1*ny1))
  #calculate distance between every pair  
  sim_mat = cosine_similarity(embed_mat, question_mat)
  similar_answer_finder(sim_mat, df , question)





def predict_similar_questions(question , faqquestions):
    #Doing embedding of questions
    question_predictions = pipe.predict(question , output_level='document')
    print(question_predictions)
    all_faq_questions = ["what is machine learning?" , "what does the role of machine learning and data scientist looks like?" , "what are the requirements of data scientist job?" ]
    all_faq_answers = ["Absc" ,"Absc" ,"Absc"]

    dataframe = {'questions' : all_faq_questions , 'answers' : all_faq_answers}
    df=pd.DataFrame(dataframe)
    #Doing embeddings of all FAQ questions
    faq_questions_predictions = pipe.predict(df.questions , output_level='document')
    print("getting ==>" , faq_questions_predictions["embed_sentence_bert_embeddings"])
    sim_df_for_one_sent = get_sim_df_for_iloc(question_predictions, faq_questions_predictions, question ,df ,  e_col)
    print("Done question matching")
    return 1
    