from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

def compute_hash(word):
    '''
        Donne un identifiant numérique à chaque mot
    '''
    res=0
    for i, letter in enumerate(word):
        res+=7**(len(word)-i)*(ord(letter)-97)
    return res%4096

def create_hash(df):
    '''
        Identifie numériquement chaque mot s'il n'est pas dans 'ban_words'
    '''
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


models = [SVC(kernel='sigmoid',max_iter=100, random_state=0),
          LogisticRegression(random_state=0, class_weight='balanced', max_iter=50, solver='liblinear', C=1),
          RandomForestClassifier(random_state=0, n_estimators=200, max_depth=3, class_weight='balanced')]

name_models = ['SVC', 'Logistic Regression', 'Random Forest']



def compare_models(models):
    columns = list(dic_genres.keys())[:17] + ['Mean']
    res = np.zeros((len(models), 18))
    for j, clf in enumerate(models):
      l_res = []
      for i in range(17):
        print(i, clf)
        clf.fit(X_train, y_train[:,i])
        y_pred = clf.predict(X_test)
        l_res.append(F1_score(y_pred, y_test[:,i]))
      l_res.append(np.mean(l_res))
      res[j, :] = l_res
    res = pd.DataFrame(res, columns=columns)
    res['Model Name'] = name_models
    res = res[['Model Name'] + columns]
    return res
