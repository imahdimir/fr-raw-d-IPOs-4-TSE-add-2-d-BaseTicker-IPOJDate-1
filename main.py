"""

    """

import json

import pandas as pd
from githubdata import GithubData
from mirutil.jdate import make_zero_padded_jdate_ie_iso_fmt as fu0


class GDUrl :
    with open('gdu.json' , 'r') as fi :
        gj = json.load(fi)

    cur = gj['cur']
    src = gj['src']
    src0 = gj['src0']
    trg = gj['trg']

gu = GDUrl()

class ColName :
    btic = 'BaseTicker'
    ipojd = 'IPO_JDate'
    tarz = 'تاريخ عرضه'
    name = 'نام شركت'
    cname = 'CompanyName'
    ch = 'ch'
    f = 'f'
    ftic = 'FirmTicker'

c = ColName()

df_ch_cols = [c.name , 'تاريخ درج' , c.tarz , 'ميانگين قيمت']
df_ch_0 = [None , None , None , 'روز اول عرضه-ريال']
df_ch = pd.DataFrame([df_ch_0] , columns = df_ch_cols)

def main() :
    pass

    ##

    gd_src = GithubData(gu.src)
    gd_src.overwriting_clone()
    ##
    df = gd_src.read_data()
    ##
    df1 = df.iloc[:1]
    assert df1.equals(df_ch) , "Not the same format as before"
    ##
    df = df[[c.name , c.tarz]]
    ##
    df.columns = [c.cname , c.ipojd]
    ##
    df = df.dropna()
    ##

    df[c.ipojd] = df[c.ipojd].str.strip()
    ##
    ptr = '\d+/\d+/\d+'
    df[c.ch] = df[c.ipojd].str.fullmatch(ptr)
    ##
    df = df[df[c.ch]]
    df = df.drop(c.ch , axis = 1)
    ##
    df[c.ipojd] = df[c.ipojd].str.replace('/' , '-')
    ##

    ptr = '1[34]\d{2}-[01]\d-[0123]\d'
    df[c.ch] = df[c.ipojd].str.fullmatch(ptr)
    ##
    msk = df[c.ch]
    df.loc[msk , c.f] = df[c.ipojd]

    ##
    ptr = r'1[34][089]\d-1?\d-[0123]?\d'
    df[c.ch] = df[c.ipojd].str.fullmatch(ptr)

    ##
    msk = df[c.ch]
    msk &= df[c.f].isna()

    df.loc[msk , c.f] = df[c.ipojd].apply(lambda x : fu0(x , sep = '-'))

    ##

    ptr = '([123]?\d)-(1?\d)-(1[34][089]\d)'
    df[c.ch] = df[c.ipojd].str.fullmatch(ptr)
    ##
    msk = df[c.ch]
    msk &= df[c.f].isna()

    df.loc[msk , c.f] = df[c.ipojd].str.replace(ptr , r'\3-\2-\1')
    ##
    df.loc[msk , c.f] = df[c.f].apply(lambda x : fu0(x , sep = '-'))
    ##

    ptr = '1[34]\d{2}-[01]\d-[0123]\d'
    assert df[c.f].str.fullmatch(ptr).all()

    ##
    df1 = df.copy()
    df1[c.ipojd] = df1[c.f]
    df1 = df1[[c.cname , c.ipojd]]

    ##

    gds0 = GithubData(gu.src0)
    gds0.overwriting_clone()
    ##
    d0 = gds0.read_data()
    ##
    d0 = d0.set_index(c.cname)
    ##

    ##
    df1[c.cname] = df1[c.cname].str.strip()
    ##
    df1[c.ftic] = df1[c.cname].map(d0[c.ftic])
    ##

    msk = df1[c.ftic].isna()

    df2 = df1[msk]
    print(len(df2))

    ##

    ##


    ##


    ##

##
if __name__ == '__main__' :
    main()

##
