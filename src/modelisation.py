def compute_hash(word):
    '''Donne un identifiant numérique à chaque mot'''
    res=0
    for i, letter in enumerate(word):
        res+=7**(len(word)-i)*(ord(letter)-97)
    return res%4096

def create_hash(df):
    l_hash = [None]*4096
    index = 0
    l_words = []
    
    banned_words = ban_words(df)

    for word in banned_words:
        if len(word)>2:
            buf = compute_hash(word)
            if l_hash[buf]==None:
                l_hash[buf] = {}
            if not(word in l_hash[buf]):
                l_hash[buf][word] = None


    for i, row in df.iterrows():
        l = row['Synopsis']
        for word in l:
            if len(word)>2:
                buf = compute_hash(word)
                if l_hash[buf]==None:
                    l_hash[buf] = {}
                if not(word in l_hash[buf]):
                    l_hash[buf][word] = index
                    l_words.append(word)
                    index+=1
                    
    return l_hash, index


def create_tfidf(df):
    l_hash, index = create_hash(df)
    mat = np.zeros((len(df), index), dtype=int)
    l_presence = [0]*index
    l_len = [0]*len(df)

    for i, row in df.iterrows():
        l = row['Synopsis']
        for k, word in enumerate(l):
            if len(word)>2:
                buf = compute_hash(word)
                ind = l_hash[buf][word]
                if ind!=None:
                    l_len[i]+=1
                    mat[i, ind]+=1
                    if not(word in l[:k]):
                        l_presence[ind]+=1
    mat_tfidf = np.zeros((len(df), index))
    n = len(df)

    for i, row in df.iterrows():
        l = row['Synopsis']
        for k, word in enumerate(l):
            if len(word)>2:
                buf = compute_hash(word)
                ind = l_hash[buf][word]
                if ind!=None:
                    mat_tfidf[i, ind] = mat[i, ind] / l_len[i] * math.log(n/l_presence[ind])
    
    return mat_tfidf, l_hash, index


def create_tfidf_test(df, l_hash, index):
    
    mat = np.zeros((len(df), index), dtype=int)
    l_presence = [0]*index
    l_len = [0]*len(df)

    for i, row in df.iterrows():
        l = row['Synopsis']
        for k, word in enumerate(l):
            if len(word)>2:
                buf = compute_hash(word)
                if l_hash[buf]!=None and word in l_hash[buf]:
                    ind = l_hash[buf][word]
                    if ind!=None:
                        l_len[i]+=1
                        mat[i, ind]+=1
                        if not(word in l[:k]):
                            l_presence[ind]+=1
    mat_tfidf = np.zeros((len(df), index))
    n = len(df)

    for i, row in df.iterrows():
        l = row['Synopsis']
        for k, word in enumerate(l):
            if len(word)>2:
                buf = compute_hash(word)
                if l_hash[buf]!=None and word in l_hash[buf]:
                    ind = l_hash[buf][word]
                    if ind!=None:
                        mat_tfidf[i, ind] = mat[i, ind] / l_len[i] * math.log(n/l_presence[ind])
    
    return mat_tfidf

def y_mat(df):
    y = np.zeros((len(df), len(dic_genres)), dtype=int)
    for i, row in df.iterrows():
        y[i,:] = row['Genre(s)']
    return y
