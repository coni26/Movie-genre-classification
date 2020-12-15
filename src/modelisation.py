import numpy as np
import math
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



class LogisticRegression_MultiLabel:
    
    def __init__(self, max_iter, C1, C2, random_state, solver='liblinear'):
        self.max_iter = max_iter
        self.C1 = C1
        self.C2 = C2
        self.class_weight = 'balanced'
        self.random_state = random_state
        self.solver = solver
        self.l_clf1 = None
        self.l_clf2 = None
        self.nb_genres = None
        
        
    def fit(self, X, y):
        nb_genres = y.shape[1]
        self.nb_genres = nb_genres
        buf = np.concatenate([X,y], axis=1)
        
        mat_pred = np.zeros((X.shape[0],nb_genres))
        l_clf1 = []
        for i in range(nb_genres):
            clf1 = LogisticRegression(random_state=self.random_state, class_weight=self.class_weight, max_iter=self.max_iter, solver=self.solver, C=self.C1)
            clf1.fit(X, y[:,i])
            l_clf1.append(clf1)
            prob = clf1.predict_proba(X)[:,1]
            mat_pred[:,i] = prob
        mat_pred = np.concatenate([mat_pred, X], axis=1)
        self.l_clf1 = l_clf1
        
        l_clf2 = []
        for i in range(nb_genres):
            clf2 = LogisticRegression(random_state=self.random_state, class_weight=self.class_weight, max_iter=self.max_iter, solver=self.solver, C=self.C2)
            clf2.fit(mat_pred, y[:,i])
            l_clf2.append(clf2)
        self.l_clf2 = l_clf2    
        
        
    def predict(self, X):
        res = np.zeros((X.shape[0], self.nb_genres))
        mat_test = np.zeros((X.shape[0],self.nb_genres))
        
        for i in range(self.nb_genres):
            clf1 = self.l_clf1[i]
            prob = clf1.predict_proba(X)[:,1]
            mat_test[:,i] = prob
        mat_test = np.concatenate([mat_test, X], axis=1)
        
        for i in range(self.nb_genres):
            clf2 = self.l_clf2[i]
            pred = clf2.predict(mat_test)
            res[:,i] = pred
        
        return res 
        


