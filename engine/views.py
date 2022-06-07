from django.shortcuts import render
from django.http import HttpResponse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from itertools import chain
from collections import Counter

# Custom imports
from .util_suffix_array import suffix_array_engine
from .util_kmp import KMP_String
from .util_bm import search
from .util_shift_or import shift_or


# import nltk
# nltk.download('stopwords')


def find_invIndex():
    stop_words = list(stopwords.words('english'))
    stop_words = stop_words+['!', '#', '$', '%', '&', '(', ')', '*', '+', '-', ';', '/', '.',
                             ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', ',', '''"''', "'", "'''", 'e.g.', 'ex.', 'etc.', 'etc', 'could', 'would', 'should', 'must']

    tokenized_words = []
    logical_view = []
    d1 = '''Note that depending on how they are used, badges may be confusing for users of screen readers and similar assistive technologies. While the styling of badges provides a visual cue as to their purpose, these users will simply be presented with the content of the badge. Depending on the specific situation, these badges may seem like random additional words or numbers at the end of a sentence, link, or button'''
    d2 = '''When using button classes on <a> elements that are used to trigger in-page functionality (like collapsing content), rather than linking to new pages or sections within the current page, these links should be given a role="button" to appropriately convey their purpose to assistive technologies such as screen readers'''
    d3 = '''Cards are built with as little markup and styles as possible, but still manage to deliver a ton of control and customization. Built with flexbox, they offer easy alignment and mix well with other Bootstrap components. They have no margin by default, so use spacing utilities as needed'''
    d4 = '''Temporary navigation drawers can toggle open or closed. Closed by default, the drawer opens temporarily above all other content until a section is selected. The Drawer can be cancelled by clicking the overlay or pressing the Esc key. It closes when an item is selected, handled by controlling the open prop.'''
    d5 = '''All form controls should have labels, and this includes radio buttons, checkboxes, and switches. In most cases, this is done by using the <label> element (FormControlLabel). When a label can't be used, it's necessary to add an attribute directly to the input component. In this case, you can apply the additional attribute (e.g. aria-label, aria-labelledby, title) via the inputProps property.'''

    docs_data = [d1.lower(), d2.lower(), d3.lower(), d4.lower(), d5.lower()]

    for word in docs_data:
        tokenized_words.append(word_tokenize(word))
        tokenized_words = list(chain(*tokenized_words))
        tokenized_words = [i.lower() for i in tokenized_words]
        processed_text = []
        for word1 in tokenized_words:
            if word1 not in stop_words and word1.isnumeric() == False and word1.isdecimal() == False and word1.isalpha() and len(word1) >= 3:
                processed_text.append(word1)
        logical_view.append(processed_text)

    cnt_temp = Counter(chain(*logical_view))
    logical_view = [i for i, j in cnt_temp.items() if j >= 1]

    sorted_list = list(sorted(logical_view))
    doc_pos = {index_term: [] for index_term in sorted_list}

    for index_term in sorted_list:
        for i, doc in enumerate(docs_data):
            if doc.find(index_term) >= 0:
                doc_pos[index_term].append((i+1, doc.find(index_term)))
    return [logical_view, sorted_list, doc_pos]


def get_home(req):
    return render(req, 'index.html')


def get_logical_view(req):
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

    # print(Counter((chain(*logical_view))))
    # logical_view = list(set(chain(*logical_view)))
    cnt_temp = Counter(chain(*logical_view))
    logical_view = [i for i, j in cnt_temp.items() if j >= 2]

    return render(req, 'logical_view.html', {'data': logical_view})


def get_query_patterns(req):
    rest = find_invIndex()
    return render(req, 'query_patterns.html', {'data': rest[0]})


def search_by_query_patterns(req):
    rest = find_invIndex()
    query = req.GET['query']
    query_type = req.GET['qtype']

    if query_type == '1':
        result = {}
        words = query.split(' ')
        # print(words)
        for word in words:
            if word.strip('.') in list(rest[2].keys()):
                result[word.strip('.')] = rest[2][word.strip('.')]
        return render(req, 'query_patterns.html', {'data': rest[0], 'sorted_data': rest[1], 'inv_index': rest[2], 'result': result, 'flag': 1})
    elif query_type == '2':
        result = {}
        for i, j in rest[2].items():
            if i.startswith(query):
                result[i] = rest[2][i]
        return render(req, 'query_patterns.html', {'data': rest[0], 'sorted_data': rest[1], 'inv_index': rest[2], 'result': result, 'flag': 1})

    elif query_type == '3':
        result = {}

        for word in rest[2].keys():
            if word >= query.split(',')[0] and word <= query.split(',')[1]:
                result[word] = rest[2][word]
        return render(req, 'query_patterns.html', {'data': rest[0], 'result': result, 'flag': 1})
    else:
        return HttpResponse("Please select query Type")


def get_inverted_index(req):
    rest = find_invIndex()
    return render(req, 'inverted_index.html', {'data': rest[0], 'sorted_data': rest[1], 'inv_index': rest[2]})


def search_by_invIndex(req):
    rest = find_invIndex()
    query = req.GET['query']
    query_type = req.GET['qtype']

    if query_type == '1':
        result = {}
        words = query.split(' ')
        # print(words)
        for word in words:
            if word.strip('.') in list(rest[2].keys()):
                result[word.strip('.')] = rest[2][word.strip('.')]
        return render(req, 'inverted_index.html', {'data': rest[0], 'sorted_data': rest[1], 'inv_index': rest[2], 'result': result, 'flag': 1})
    elif query_type == '2':
        result = {}
        for i, j in rest[2].items():
            if i.startswith(query):
                result[i] = rest[2][i]
        return render(req, 'inverted_index.html', {'data': rest[0], 'sorted_data': rest[1], 'inv_index': rest[2], 'result': result, 'flag': 1})

    elif query_type == '3':
        result = {}

        for word in rest[2].keys():
            if word >= query.split(',')[0] and word <= query.split(',')[1]:
                result[word] = rest[2][word]
        return render(req, 'inverted_index.html', {'data': rest[0], 'sorted_data': rest[1], 'inv_index': rest[2], 'result': result, 'flag': 1})
    else:
        return HttpResponse("Please select query Type")


def get_suffix_array(req):
    return render(req, 'suffix_array.html')


def suffix_array_algo(req):
    S = req.GET['text']
    P = req.GET['pattern']
    res = suffix_array_engine(S, P)
    return render(req, 'suffix_array.html', {'found_pos': res[0], 'suffix_arr': res[1], 'flag': 1, 'params': [S, P]})


def get_brut_force(req):
    return render(req, 'brutforce.html')


def brut_force_algo(req):
    S = req.GET['text']
    P = req.GET['pattern']
    SL = len(S)
    PL = len(P)
    if PL > SL:
        print("No Match Found")
    else:
        Found = False
        pos = []
        found_pos = []
        for i in range(0, SL-1):
            j = 0
            while j < PL and S[i] == P[j]:
                i = i+1
                j = j+1
                pos.append((i, j))
            if j == PL:
                Found = True
                found_pos.append(i-PL+1)
        if not Found:
            return HttpResponse('No Matching Found !')
        # print(pos)
    return render(req, 'brutforce.html', {'pos': pos, 'found_pos': found_pos, 'flag': 1, 'params': [S, P]})


def get_KMP(req):
    return render(req, 'kmpalgo.html')


def kmp_algo(req):
    S = req.GET['text']
    P = req.GET['pattern']
    # print(KMP_String(pat, txt))
    res = KMP_String(P, S)
    return render(req, 'kmpalgo.html', {'pos': res[0], 'found_pos': res[1], 'flag': 1, 'params': [S, P]})


def get_BM(req):
    return render(req, 'bm_algo.html')


def bm_algo(req):
    S = req.GET['text']
    P = req.GET['pattern']
    return render(req, 'bm_algo.html', {'found_pos': search(S, P), 'flag': 1, 'params': [S, P]})


def get_Shift_Or(req):
    return render(req, 'shift_or_algo.html')


def shift_or_algo(req):
    S = req.GET['text']
    P = req.GET['pattern']
    return render(req, 'shift_or_algo.html', {'found_pos': shift_or(S, P), 'flag': 1, 'params': [S, P]})
