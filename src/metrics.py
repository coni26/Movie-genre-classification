
def precision(y_pred, y):
    res = 0
    if len(y.shape)==1:
        for i in range(len(y)):
            res += y_pred[i]*y[i]
        res/=max(sum(y_pred),1)
    else:
        n = y.shape[1]
        for i in range(len(y)):
            res +=  sum(abs(y_pred[i,:]*y[i,:]))/max(sum(y_pred[i,:]),1)
        res/=len(y)
    return res


def recall(y_pred, y):
    res = 0
    if len(y.shape)==1:
        for i in range(len(y)):
            res += y_pred[i]*y[i]
        res/=sum(y)
    else:
        n = y.shape[1]
        for i in range(len(y)):
            res += sum(abs(y_pred[i,:]*y[i,:]))/max(sum(y[i,:]),1)
        res/=len(y)
    return res


def F1_score(y_pred, y):
    rec = recall(y_pred, y)
    prec = precision(y_pred, y)
    return 2*(rec*prec)/(rec+prec)




