# -*- coding: utf-8 -*-

import codecs
import logging
import random
import os

def data_processing():
    with codecs.open("data/questions.txt", mode="w", encoding="utf-8") as wfquestion:
        with codecs.open("data/answers.txt", mode="w", encoding="utf-8") as wfanswer:
            try:
                wfquestion.truncate()
                wfanswer.truncate()
            except Exception as e:
                logging.info("data_processing:clear data_processing.txt error:" + str(e))
            finally:
                wfquestion.close()
                wfanswer.close()
    
    question = ''
    answer = ''
    QAQAQ = ''
    countQuestion = 0
    countAnswer = 0
    sessionId = ''
    with codecs.open("data/chat.txt", mode = 'r', encoding = "utf-8") as rf:
        with codecs.open("data/questions.txt", mode="a", encoding="utf-8") as wf_question:
            with codecs.open("data/answers.txt", mode="a", encoding="utf-8") as wf_answer:
                try:
                    line = rf.readline()
                    while line:
                        splitline = line.strip('\r\n').split("\t")

                        # 直接跳过不存在的条目
                        if splitline[6].strip() == '':
                            line = rf.readline()
                            continue

                        if sessionId == splitline[0]:
                            try:
                                if splitline[2] == '0':
                                    # 生成对话
                                    if QAQAQ != '' and answer != '':
                                        wf_question.write(QAQAQ + "\n")
                                        wf_answer.write(answer + "\n")

                                    if answer != '':
                                        # 如果一段对话以A起始的话则忽略第一条A
                                        if QAQAQ != '':
                                            QAQAQ = QAQAQ + answer + '<s>'
                                        answer = ''
                                        countAnswer = countAnswer + 1

                                    if question == '':
                                        question = question + splitline[6].strip()
                                    else:
                                        question = question + u'，' + splitline[6].strip()

                                elif splitline[2] == '1':
                                    if question != '':
                                        QAQAQ = QAQAQ + question + '<s>'
                                        question = ''
                                        countQuestion = countQuestion + 1

                                    if answer == '':
                                        answer = answer + splitline[6].strip()
                                    else:
                                        answer = answer + u'，' + splitline[6].strip()

                            except Exception as e:
                                logging.error("data_processing:write into chatmasked_user failure" + str(e))
                        else:
                            # 生成对话
                            if QAQAQ != '' and answer != '':
                                wf_question.write(QAQAQ + "\n")
                                wf_answer.write(answer + "\n")
                            sessionId = splitline[0]
                            question = ''
                            answer = ''
                            QAQAQ = ''
                            countQuestion = 0
                            countAnswer = 0
                            continue

                        line = rf.readline()

                    # 生成对话
                    if QAQAQ != '' and answer != '':
                        wf_question.write(QAQAQ + "\n")
                        wf_answer.write(answer + "\n")

                except Exception as e:
                    logging.error("data_processing: data processing failure!" + str(e))
                finally:
                    rf.close()
                    wf_question.close()
                    wf_answer.close()
   
def cutDataToTrainDevBy91():
    randomList = []
    with codecs.open("data/devQuestions.txt", mode="w", encoding="utf-8") as wf_devQuestion:
        with codecs.open("data/devAnswers.txt", mode="w", encoding="utf-8") as wf_devAnswer:
            with codecs.open("data/trainQuestions.txt", mode="w", encoding="utf-8") as wf_trainQuestion:
                with codecs.open("data/trainAnswers.txt", mode="w", encoding="utf-8") as wf_trainAnswer:
                    try:
                        wf_devQuestion.truncate()
                        wf_devAnswer.truncate()
                        wf_trainQuestion.truncate()
                        wf_trainAnswer.truncate()
                    except Exception as e:
                        logging.info("data_processing:clear data_processing.txt error:" + str(e))
                    finally:
                        wf_devQuestion.close()
                        wf_devAnswer.close()
                        wf_trainQuestion.truncate()
                        wf_trainAnswer.truncate()    
    
    with codecs.open("data/questions.txt", mode = 'r', encoding = "utf-8") as rf_question:
        with codecs.open("data/answers.txt", mode = 'r', encoding = "utf-8") as rf_answer:
            try:
                questionLines = rf_question.readlines()
                answerLines = rf_answer.readlines()
                #trainset的十分之一的数据集作为devset
                randomList = random.sample(range(len(questionLines)-1), int(len(questionLines)/10))
                with codecs.open("data/devQuestions.txt", mode = 'a', encoding = "utf-8") as wf_devQuestion:
                    with codecs.open("data/devAnswers.txt", mode = 'a', encoding = "utf-8") as wf_devAnswer:
                        try:
                            for i in randomList:
                                wf_devQuestion.write(questionLines[i])
                                wf_devAnswer.write(answerLines[i])
                        except Exception as e:
                            logging.error("cutDataToTrainDevBy91: failure" + str(e))
                        finally:
                            wf_devQuestion.close()
                            wf_devAnswer.close()
                
            except Exception as e:
                logging.error("cutDataToTrainDevBy91: failure" + str(e))
            finally:
                rf_question.close()
                rf_answer.close()
                
    with codecs.open("data/questions.txt", mode = 'r', encoding="utf-8") as rf_question:
        with codecs.open("data/answers.txt", mode='r',encoding="utf-8") as rf_answer:
            questions = rf_question.readlines()
            answers = rf_answer.readlines()
            with codecs.open("data/trainQuestions.txt",mode='a',encoding="utf-8") as wf_question:
                with codecs.open("data/trainAnswers.txt",mode='a',encoding="utf-8") as wf_answer:
                    for i in range(len(questions)):
                        if i not in randomList:
                            wf_question.write(questions[i])
                    for i in range(len(answers)):
                        if i not in randomList:
                            wf_answer.write(answers[i])
                            
                    rf_question.close()
                    rf_answer.close()
                    wf_question.close()
                    wf_answer.close()
    
                            
    # os.remove("questions.txt")
    # os.remove("answers.txt")
                            
                
if __name__ == "__main__": 
    data_processing()
    cutDataToTrainDevBy91()
 