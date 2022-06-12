from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from itertools import chain
from collections import Counter
# module to read the contents of the file from a csv file
from contextlib import redirect_stdout

# module to redirect the output to a text file
terms = []
# list to store the terms present in the documents

keys = []
# list to store the names of the documents

vec_Dic = {}
# dictionary to store the name of the document and the boolean vector as list

dicti = {}
# dictionary to store the name of the document and the terms present in it as a
# vector

dummy_List = []
# list for performing some operations and clearing them


def get_logical_view():
    result = {}
    stop_words = list(stopwords.words('english'))
    stop_words = stop_words+['!', '#', '$', '%', '&', '(', ')', '*', '+', '-', ';', '/', '.',
                             ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', ',', '''"''', "'", "'''", 'e.g.', 'ex.', 'etc.', 'etc', 'could', 'would', 'should', 'must']

    tokenized_words = []
    logical_view = []
    for i in range(1, 11):
        file1 = open(f"docs/file{i}.txt", 'r')
        for word in file1.readlines():
            tokenized_words.append(word_tokenize(word.strip('\n')))
        tokenized_words = list(chain(*tokenized_words))
        tokenized_words = [i.lower() for i in tokenized_words]
        processed_text = []
        for word1 in tokenized_words:
            if word1 not in stop_words and word1.isnumeric() == False and word1.isdecimal() == False and word1.isalpha() and len(word1) >= 3:
                processed_text.append(word1)
        logical_view.append(processed_text)
        result[f"file{i}.txt"] = processed_text

    # print(Counter((chain(*logical_view))))
    # logical_view = list(set(chain(*logical_view)))
    cnt_temp = Counter(chain(*logical_view))
    logical_view = [i for i, j in cnt_temp.items()]
    sorted_list = list(sorted(logical_view))

    return sorted_list, result


''' 
def filter(documents, rows, cols):
    function to read and separate the name of the documents and the terms
    present in it to a separate list  from the data frame and also create a
    dictionary which has the name of the document as key and the terms present in
    it as the list of strings  which is the value of the key
 
    for i in range(0,rows):
        for j in range(0,cols):
            # traversal through the data frame
 
            if(j == 0):
                # first column has the name of the document in the csv file
                #print(documents.iloc[i].iat[j])
                keys.append(documents.iloc[i].iat[j])
            else:
                dummy_List.append(documents.iloc[i].iat[j])
                # dummy list to update the terms in the dictionary
 
                if documents.iloc[i].iat[j] not in terms:
                    # add the terms to the list if it is not present else continue
                    terms.append(documents.iloc[i].iat[j])
 
        copy = dummy_List.copy()
        # copying the the dummy list to a different list
 
        dicti.update({documents.iloc[i].iat[0]: copy})
        # adding the key value pair to a dictionary
 
        dummy_List.clear()
        #print(dicti)
        #print(terms)
        #print(keys)
        # clearing the dummy list
'''


def bool_Representation(dicti):
    '''In this function we get a boolean representation of the terms present in the
    documents in the form of lists, later we create a dictionary which contains
    the the name of the documents as key and value as the list of boolean values
    representing the terms present in the document'''
    '''
    for i in range(len(terms)):
        terms[i]=str(terms[i])
    
    terms.sort()
    '''
    # print(terms)
    # we sort the elements in the alphabetical order for the convience, the order
    # of the term does not make any difference
    # print(terms)
    # print(dicti)
    for i in (dicti):
        # for every document in the dictionary we check for each string present in
        # the list

        for j in terms:
            # if the string is present in the list we append 1 else we append 0

            if j in dicti[i]:
                dummy_List.append(1)
            else:
                dummy_List.append(0)
            # appending 1 or 0 for obtaining the boolean representation

        copy = dummy_List.copy()
        # copying the the dummy list to a different list

        vec_Dic.update({i: copy})
        # print(vec_Dic)
        # adding the key value pair to a dictionary

        dummy_List.clear()
        # clearing the dummy list
    # print(vec_Dic)


def query_Vector(query):
    '''In this function we represent the query in the form of boolean vector'''

    qvect = []
    # query vector which is returned at the end of the function

    for i in terms:
        # if the word present in the list of terms is also present in the query
        # then append 1 else append 0

        if i in query:
            qvect.append(1)
        else:
            qvect.append(0)
    # print(qvect)
    return qvect
    # return the query vector which is obtained in the boolean form


def check(dictionary, val):
    '''Function to return the key when the value is known'''

    for key, value in dictionary.items():
        if(val == value):
            # if the given value is same as the value present in the dictionary
            # return the key
            # print(key)
            return key


def prediction(q_Vect):
    '''In this function we make the prediction regarding which document is related
    to the given query by performing the boolean operations'''

    dictionary = {}
    listi = []
    count = 0
    # initialisation of the dictionary , list and a variable which is further
    # required for performing the computation

    term_Len = len(terms)
    # number of terms present in the term list

    for i in vec_Dic:
        # for every document in the dictionary containing the terms present in it
        # the form of boolean vector

        for t in range(term_Len):
            if(q_Vect[t] == vec_Dic[i][t] and q_Vect[t] == 1):
                # print(q_Vect[t])
                # print(vec_Dic[i][t])
                # if the words present in the query is also present in the
                # document or if the words present in the query is also absent in
                # the document

                count += 1
                # increase the value of count variable by one
                # the condition in which words present in document and absent in
                #query , present in query and absent in document is not considered

        dictionary.update({i: count})
        # dictionary updation here the name of the document is the key and the
        # count variable computed earlier is the value

        count = 0
        # reinitialisaion of count variable to 0
    # print(dictionary)
    for i in dictionary:
        listi.append(dictionary[i])
        # here we append the count value to list

    listi = sorted(listi, reverse=True)
    # print(listi)
    # we sort the list in the descending order which is needed to rank the
    # documents according to the relevance

    ans = ' '
    # variable to store the name of the document which is most relevant

    with open('output.txt', 'w') as f:
        with redirect_stdout(f):
            # to redirect the output to a text file

            #print("ranking of the documents")

            for count, i in enumerate(listi):
                key = check(dictionary, i)
                # Function call to get the key when the value is known
                if count == 0:
                    ans = key
                    # to store the name of the document which is most relevant

                #print(key, "rank is", count+1)
                # print the name of the document along with its rank

                dictionary.pop(key)
                # remove the key from the dictionary after printing

            print(ans, "is the most relevant document for the given query")
            # to print the name of the document which is most relevant
    return ans+" is the most relevant document for the given query"


def main():
    res, res1 = get_logical_view()
    # print(res)
    # print(res1)
    global terms
    terms = res.copy()
    dicti = res1.copy()
    # print(terms)
    '''
    rows=[]
    for i,j in res1.items():
        rows.append([i]+j)
    # name of csv file
    filename = "documents.csv"
    # writing to csv file
    with open(filename, 'w',newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile) 
        # writing the data rows
        csvwriter.writerows(rows)
    '''
    print("The logical view of all documents are as follow:\n")
    for i in range(len(res)):
        print(res[i], end=",")
    '''   
    documents = pandas.read_csv(r'documents.csv')
    # to read the data from the csv file as a dataframe
 
    rows = len(documents)
    # to get the number of rows
    #print(rows)
 
    cols = len(documents.columns)
    #print(cols)
    # to get the number of columns
    
    filter(documents, rows, cols)
    '''
    # function call to read and separate the name of the documents and the terms
    # present in it to a separate list  from the data frame and also create a
    # dictionary which has the name of the document as key and the terms present in
    # it as the list of strings  which is the value of the key

    bool_Representation(dicti)
    # In this function we get a boolean representation of the terms present in the
    # documents in the form of lists, later we create a dictionary which contains
    # the the name of the documents as key and value as the list of boolean values
    # representing the terms present in the document
    print("\n")
    query = input("Enter query:\n")
    # to get the query input from the user, the below input is given for obtaining
    # the output as in output.txt file
    # hockey is a national sport
    query = query.lower()
    query = query.split(' ')
    # spliting the query as a list of strings

    q_Vect = query_Vector(query)
    # function call to represent the query in the form of boolean vector
    print()
    print(prediction(q_Vect))
    # Function call to make the prediction regarding which document is related to
    # the given query by performing the boolean operations


main()
