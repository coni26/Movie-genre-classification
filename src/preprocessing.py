import pandas as pd



def clean_text(s):
    return s.replace("’"," ").replace("'"," ").replace(".", "").replace(":", "").replace(",","").replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ù","u").replace("û","u").replace("â","a").replace("ç","c").replace("ï","i").replace('…','').replace('(',' ').replace(')',' ').lower().split(" ")
