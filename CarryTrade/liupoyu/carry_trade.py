
# coding: utf-8

# In[201]:

import pandas as pd
import numpy as np
import os, re
from datetime import datetime, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl

SUB_PATH = os.path.abspath('..').split('/')[-1]
DATA_PATH = '..'+os.sep+'..'+os.sep+'..'+os.sep+'data'+os.sep+SUB_PATH+os.sep+'01_carry_trade_returns'+os.sep

def today(string):
    return datetime.now().strftime('%Y%m%d_')+string

freq_list = ['1m', '3m', '6m', '12m']
# m_currs_list = range(10, 61, 2)


# In[ ]:




# In[13]:

# currency_list


# In[ ]:




# In[ ]:




# In[107]:

"""creating column names function"""
def curr_cols(currency_list, typ, mat):
    if mat != 'SPOT':
        mat += 'FWD'
    return currency_list.apply(lambda x: '{:s}_{:s}_{:s}'.format(x, typ, mat))
	
def curr_cols_fd(sub_curr_list, mat):
    if mat != 'SPOT':
        mat += 'FWD'
        
    return pd.Series(sub_curr_list).apply(lambda x: '{:s}_{:s}_{:s}_FD'.format(x, 'MID', mat)) 


# In[141]:

"""extract currency list"""
freq = '1m'
data = pd.read_csv(os.path.join(DATA_PATH,('20160524_DATA_FX_Dollar_Rates_MID.csv')))
currency_list = pd.Series(map(lambda x: x[:-9], filter(lambda x: x[-8:]=='ASK_SPOT', list(data.columns))))


# In[ ]:




# In[142]:

developed_currency_list = pd.Series(['AUSTRALIANDOLLAR',
 'BELGIANFRANC',
 'CADIANDOLLAR',
 'DANISHKRONE',
 'EURO',
 'FRENCHFRANC',
 'GERMANMARK',
 'ITALIANLIRA',
 'JAPANESEYEN',
 'NETHGUILDER',
 'NEWZEALANDDOLLAR',
 'NORWEGIANKRONE',
 'SWEDISHKRO',
 'SWISSFRANC',
 'UKPOUND'])


# In[143]:

all_currency_list = pd.Series(['AUSTRALIANDOLLAR',
 'AUSTRIANSCHIL',
 'BELGIANFRANC',
 'BRAZILIANREAL',
 'BULGARIANLEV',
 'CADIANDOLLAR',
 'CROATIANKU',
 'CYPRUSPOUND',
 'CZECHKORU',
 'DANISHKRONE',
 'EGYPTIANPOUND',
 'EURO',
 'FINNISHMARKKA',
 'FRENCHFRANC',
 'GERMANMARK',
 'GREEKDRACHMA',
 'HONGKONGDOLLAR',
 'HUNGARIANFORINT',
 'ICELANDICKRO',
 'INDIANRUPEE',
 'INDONESIANRUPIAH',
 'IRISHPUNT',
 'ISRAELISHEKEL',
 'ITALIANLIRA',
 'JAPANESEYEN',
 'KUWAITIDIR',
 'MALAYSIANRINGGIT',
 'MEXICANPESO',
 'NETHGUILDER',
 'NEWZEALANDDOLLAR',
 'NORWEGIANKRONE',
 'PHILIPPINEPESO',
 'POLISHZLOTY',
 'PORTUGUESEESCUDO',
 'RUSSIANROUBLE',
 'SAUDIRIYAL',
 'SINGAPOREDOLLAR',
 'SLOVAKKORU',
 'SLOVENIANTOLAR',
 'SOUTHAFRICARAND',
 'SOUTHKOREANWON',
 'SPANISHPESETA',
 'SWEDISHKRO',
 'SWISSFRANC',
 'TAIWANNEWDOLLAR',
 'THAIBAHT',
 'UKPOUND',
 'UKRAINEHRYVNIA'])


# In[144]:

currencies_list = pd.Series([currency_list, all_currency_list, developed_currency_list], [60, 48, 15])
currencies_list.to_pickle(os.path.join(TEMP_PATH, today('currencies_list.p'))


# In[ ]:




# In[44]:

"""delete ceased-trading currencies"""
d = pd.read_csv(DATA_PATH+'20160524_DATA_FX_Dollar Rates_MID.csv', index_col=0)


# In[45]:

maturity = pd.Series(['SPOT', '1mFWD', '3mFWD', '6mFWD', '12mFWD'])

#From the columns, get all the currency names. There are totally 60 currencies.
currencies_list = pd.read_pickle(DATA_PATH+('20160919_currencies_list.pickle'))


# In[46]:

currency_list = currencies_list[60]


# In[ ]:




# In[47]:

if not len(currency_list) == 60:
    print 'currency_list not of len 60'


# In[48]:

#From the currency names create LOG column names
log_col_df = (maturity.apply(lambda mat: currency_list.apply(lambda x: x+'_MID_'+mat))).applymap(lambda x: x+'_LOG')

log_col_df

#Flatten 2D df into 1D list
to_be_logged = pd.Series([x for y in (maturity.apply(lambda mat: currency_list.apply(lambda x: x+'_MID_'+mat))).iterrows() for x in y[1]])
#Flatten LOG columns names
logged = to_be_logged.apply(lambda x: x+'_LOG')

to_be_logged

logged

#Log all the numbers
d[logged] = d[to_be_logged].applymap(np.log)

log_col_df



fd_list = []
for i, log_col in log_col_df.iloc[1:].iterrows():
#     print log_col
#     print log_col_df.iloc[0]

    #Get forward and spot DFs
    fwd = d[log_col][:]
    spot = d[log_col_df.iloc[0]][:]
    #Change columns names so that they can substract
    fwd.columns = range(len(fwd.columns))
    spot.columns = range(len(spot.columns))
    fd = fwd - spot
    fd.columns = log_col.apply(lambda x: x[:-3]+'FD')
    fd_list.append(fd)
d_fd = pd.concat([d]+fd_list, axis=1)


# In[ ]:




# In[88]:

d_fd.to_pickle(DATA_PATH+today('fx_rates_mid_fd.pickle'.format(freq)))
d_fd.to_csv(DATA_PATH+today('fx_rates_mid_fd.csv'.format(freq)))


# In[ ]:




# In[60]:

"""delete non-trading entries"""
data = pd.read_pickle(DATA_PATH+('20160918_fx_rates_mid_fd.pickle'))


# In[78]:

data['datetime'] = data['Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))


# In[83]:

dates = data['datetime']


# In[61]:
# Do not have this file
termination = pd.read_excel(DATA_PATH+'Euro Currencies Termination Dates.xlsx')


# In[63]:

curr_cols = pd.Series(data.columns)


# In[85]:

for iitem in termination.iterrows():
    i, item = iitem
    curr, date = item
    date = date.to_datetime()
    year = date.year

    del_cols = curr_cols[curr_cols.apply(lambda x: x.find(curr)!=-1)]
    del_idx = data[data['datetime'] >= date].index
    data.ix[del_idx, del_cols] = np.nan
    print len(del_cols)


# In[89]:

data.to_pickle(DATA_PATH+today('fx_rates_mid_fd_trading.pickle'))
data.to_csv(DATA_PATH+today('fx_rates_mid_fd_trading.csv'))


# In[ ]:




# In[ ]:




# In[91]:

"""extract frequencies"""
data = pd.read_pickle(DATA_PATH+('20160919_fx_rates_mid_fd_trading.pickle'))


# In[96]:

data['1m'] = data['datetime'].apply(lambda x: x.strftime('%Y_%m'))

data['3m'] = data['datetime'].apply(lambda x: '{:d}_{:d}'.format(x.year, pd.Timestamp(x).quarter))

data['6m'] = data['datetime'].apply(lambda x: '{:d}_{:d}'.format(x.year, 1 if x.month<=6 else 2))

data['12m'] = data['datetime'].apply(lambda x: '{:d}'.format(x.year))

# data.to_csv(DATA_PATH+'01_periods'+os.sep+today('fx_rates_min_fd_{:s}.csv'.format('daily')))
# data.to_pickle(DATA_PATH+'01_periods'+os.sep+today('fx_rates_min_fd_{:s}.pickle'.format('daily')))

freq_list = ['1m', '3m', '6m', '12m']

for freq in freq_list:
    d = data.groupby(freq).apply(lambda x: x.loc[x['datetime'].idxmax()])
    d.to_csv(os.path.join(TEMP_PATH, '01_frequencies', today('fx_rates_mid_fd_{:s}.csv'.format(freq))))
    d.to_pickle(os.path.join(TEMP_PATH, '01_frequencies', today('fx_rates_mid_fd_{:s}.p'.format(freq))))


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[105]:

"""calculate returns"""
freq = '1m'
freq_list = ['1m', '3m', '6m', '12m']
currencies_list = pd.read_pickle(DATA_PATH+('20160919_currencies_list.pickle'))
currency_list = currencies_list[60]
for freq in freq_list:
    data = pd.read_pickle(os.path.join(TEMP_PATH, '01_frequencies', today('fx_rates_mid_fd_{:s}.p'.format(freq))))    



    #There are 8 different retrn calculation method. I am creating a file for each returns
    return_type_list = ['long_one', 'short_one', 'long_prev', 'short_prev', 'long_afte', 'short_afte', 'long_cont', 'short_cont']

    #long_one
    long_one = pd.DataFrame(np.array(data[curr_cols(currency_list, 'BID', freq)].applymap(np.log).shift(1)) - np.array(data[curr_cols(currency_list, 'ASK', 'SPOT')].applymap(np.log)), columns=currency_list, index=data['datetime'])

    #short_one
    short_one = pd.DataFrame(- np.array(data[curr_cols(currency_list, 'ASK', freq)].applymap(np.log).shift(1)) + np.array(data[curr_cols(currency_list, 'BID', 'SPOT')].applymap(np.log)), columns=currency_list, index=data['datetime'])





    #long_prev
    long_prev = pd.DataFrame(np.array(data[curr_cols(currency_list, 'MID', freq)].applymap(np.log).shift(1)) - np.array(data[curr_cols(currency_list, 'ASK', 'SPOT')].applymap(np.log)), columns=currency_list, index=data['datetime'])

    #short_prev
    short_prev = pd.DataFrame(- np.array(data[curr_cols(currency_list, 'MID', freq)].applymap(np.log).shift(1)) + np.array(data[curr_cols(currency_list, 'BID', 'SPOT')].applymap(np.log)), columns=currency_list, index=data['datetime'])

    #long_afte
    long_afte = pd.DataFrame(np.array(data[curr_cols(currency_list, 'BID', freq)].applymap(np.log).shift(1)) - np.array(data[curr_cols(currency_list, 'MID', 'SPOT')].applymap(np.log)), columns=currency_list, index=data['datetime'])

    #short_afte
    short_afte = pd.DataFrame(- np.array(data[curr_cols(currency_list, 'ASK', freq)].applymap(np.log).shift(1)) + np.array(data[curr_cols(currency_list, 'MID', 'SPOT')].applymap(np.log)), columns=currency_list, index=data['datetime'])

    #long_cont
    long_cont = pd.DataFrame(np.array(data[curr_cols(currency_list, 'MID', freq)].applymap(np.log).shift(1)) - np.array(data[curr_cols(currency_list, 'MID', 'SPOT')].applymap(np.log)), columns=currency_list, index=data['datetime'])

    #short_cont
    short_cont = pd.DataFrame(- np.array(data[curr_cols(currency_list, 'MID', freq)].applymap(np.log).shift(1)) + np.array(data[curr_cols(currency_list, 'MID', 'SPOT')].applymap(np.log)), columns=currency_list, index=data['datetime'])

    returns = pd.Series([long_one, short_one, long_prev, short_prev, long_afte, short_afte, long_cont, short_cont], return_type_list)



    returns.to_pickle(os.path.join(TEMP_PATH, '02_single_returns', today('single_returns_{:s}.p'.format(freq))))
    returns['long_cont'].to_csv(os.path.join(TEMP_PATH, '02_single_returns', today('single_returns_{:s}.csv'.format(freq))))


# In[147]:

currencies_list[48]


# In[ ]:




# In[167]:

"""trading: short and long portfolios"""
freq = '1m'
freq_list = ['1m', '3m', '6m', '12m']
currencies_list = pd.read_pickle(DATA_PATH+('20160919_currencies_list.pickle'))[[15, 48]]
for currency_list in currencies_list:
    for freq in freq_list[:]:
        returns = pd.read_pickle(os.path.join(TEMP_PATH, '02_single_returns', today('single_returns_{:s}.p'.format(freq))))['long_one'].shift(-1)
        data = pd.read_pickle(os.path.join(TEMP_PATH, '01_frequencies', today('fx_rates_mid_fd_{:s}.p'.format(freq))))    
        #     currency_list = pd.read_pickle(DATA_PATH+'20160626_currency_list.p')



        # if not os.path.exists(DATA_PATH+'strategies'+os.sep+freq):
        #     os.makedirs(DATA_PATH+'strategies'+os.sep+freq)

        #     currency_list = all_countries_currs

        bas_list = currency_list.apply(lambda x: x+'_BAS')

        fd_list = curr_cols_fd(currency_list, freq)

#         data


        for m_currs in range(10, len(currency_list)+1, 2) + [len(currency_list)] if len(currency_list)%2 else range(10, len(currency_list)+1, 2):
            print m_currs
            for k_parts in [2, 3, 5, m_currs/2, m_currs]:



                output = []
                for i, item in data.iloc[:-1].iterrows():
                    date = item['datetime']
                    currs_with_returns = set(list(returns.loc[date].dropna().index))

                    fd_sort = item[curr_cols_fd(currency_list, freq)].sort_values(ascending=False).dropna()
                    fd_sort_currs = fd_sort.index.map(lambda x: '_'.join(x.split('_')[:-3]))
                    fd_sort.index = fd_sort_currs

                    bas_sort = item[currency_list.apply(lambda x: x+'_BAS')].sort_values().dropna()
                    bas_sort_currs = bas_sort.index.map(lambda x: x[:-4])
                    bas_sort.index = bas_sort_currs

                    most_liquid_currs = pd.Series(bas_sort[fd_sort_currs].sort_values().iloc[:m_currs].index)
        #                 if len(most_liquid_currs) < len(fd_sort):
        #                     print 'Truncated'
                    most_liquid_currs_with_returns = most_liquid_currs[most_liquid_currs.apply(lambda x: x in currs_with_returns)].dropna()

                    fd_liquid_sort = fd_sort[most_liquid_currs_with_returns].sort_values(ascending=True)
                    fd_liquid_currs = list(fd_liquid_sort.index)

                    num_seq = np.linspace(0, len(fd_liquid_currs), num=min(k_parts, len(fd_liquid_currs))+1, dtype=np.int32)

                    ranges = zip(num_seq[:-1], num_seq[1:])
                    long_port = fd_liquid_currs[ranges[-1][0]: ranges[-1][1]]
                    short_port = fd_liquid_currs[ranges[0][0]: ranges[0][1]]

                    temp = {}
                    temp['datetime'] = item['datetime']
                    temp['long'] = set(long_port)
                    temp['short'] = set(short_port)
                    output.append(temp)
        #                 break



                pd.DataFrame(output).to_pickle(os.path.join(TEMP_PATH, '03_long_short', today('{:d}_currs_{:d}_liquid_{:d}_parts.p').format(len(currency_list), m_currs, k_parts)))              
                pd.DataFrame(output).to_csv(os.path.join(TEMP_PATH, '03_long_short', today('{:d}_currs_{:d}_liquid_{:d}_parts.csv').format(len(currency_list), m_currs, k_parts)))


# In[ ]:




# In[ ]:




# In[177]:

"""trading: return types"""
freq = '1m'
m_currs = 48
k_parts = 5
for currency_num in [15, 48]:
    for freq in freq_list[:]:
        current_path = os.path.join(TEMP_PATH, '04_return_types', freq)
        if not os.path.isdir(current_path):
            os.makedirs(current_path)

        for m_currs in range(10, currency_num+1, 2) + [currency_num] if currency_num%2 else range(10, currency_num+1, 2):
            print m_currs
            for k_parts in [2, 3, 5, m_currs/2, m_currs]:
                if not os.path.isfile(os.path.join(TEMP_PATH, '03_long_short', today('{:d}_currs_{:d}_liquid_{:d}_parts.p').format(len(currency_list), m_currs, k_parts))):
                    continue
                strategy = pd.read_pickle(os.path.join(TEMP_PATH, '03_long_short', today('{:d}_currs_{:d}_liquid_{:d}_parts.p').format(len(currency_list), m_currs, k_parts))).set_index('datetime').shift(1)
#                 break

                strategy.ix[0, 'long'] = set([])
                strategy.ix[0, 'short'] = set([])

                tail_padding = pd.DataFrame([{'long': set([]), 'short': set([])}], index=[datetime(2030, 1, 1)])
                strategy = pd.concat([strategy, tail_padding])

                strategy

                output = []
                for i, itemi in enumerate(strategy.iterrows()):
                    date, item = itemi
                    if i == 0:
                        continue
                    elif i == len(strategy) - 1:
                        continue
                    temp = {}
                    temp['datetime'] = date

                    temp['long_one'] = item['long'] - strategy.ix[i-1, 'long'] - strategy.ix[i+1, 'long']
                    temp['short_one'] = item['short'] - strategy.ix[i-1, 'short'] - strategy.ix[i+1, 'short']

                    temp['long_prev'] = (item['long'] - strategy.ix[i+1, 'long']) & strategy.ix[i-1, 'long']
                    temp['short_prev'] = (item['short'] - strategy.ix[i+1, 'short']) & strategy.ix[i-1, 'short']

                    temp['long_afte'] = (item['long'] - strategy.ix[i-1, 'long']) & strategy.ix[i+1, 'long']
                    temp['short_afte'] = (item['short'] - strategy.ix[i-1, 'short']) & strategy.ix[i+1, 'short']

                    temp['long_cont'] = item['long'] & strategy.ix[i-1, 'long'] & strategy.ix[i+1, 'long']
                    temp['short_cont'] = item['short'] & strategy.ix[i-1, 'short'] & strategy.ix[i+1, 'short']

                    output.append(temp)    

                pd.DataFrame(output).set_index('datetime').applymap(list).to_pickle(os.path.join(current_path, today('{:d}_currs_{:d}_liquid_{:d}_parts.pickle').format(currency_num, m_currs, k_parts)))
                pd.DataFrame(output).set_index('datetime').applymap(list).to_csv(os.path.join(current_path, today('{:d}_currs_{:d}_liquid_{:d}_parts.csv').format(currency_num, m_currs, k_parts)))


# In[160]:

strategy = pd.read_pickle(DATA_PATH+'03_long_short'+os.sep+'1m'+os.sep+('20160919_{:d}_currs_{:d}_liquid_{:d}_parts.p').format(15, 10, 2)).set_index('datetime')


# In[161]:

strategy


# In[ ]:




# In[179]:

"""trading: returns"""
return_type_list = ['long_one', 'short_one', 'long_prev', 'short_prev', 'long_afte', 'short_afte', 'long_cont', 'short_cont']
freq = '1m'
currencies_list = pd.read_pickle(DATA_PATH+('20160919_currencies_list.pickle'))[[15, 48]]
for freq in freq_list[:]:
    return_matrix = []
    for currency_list in currencies_list:

    #     if not os.path.exists(DATA_PATH+'portfolio_returns'+os.sep+freq):
    #         os.makedirs(DATA_PATH+'portfolio_returns'+os.sep+freq)
        for m_currs in range(10, len(currency_list)+1, 2) + [len(currency_list)] if len(currency_list)%2 else range(10, len(currency_list)+1, 2):
            print freq, m_currs
            for k_parts in [2, 3, 5, m_currs/2, m_currs]:

#         for m_currs in m_currs_list:
#             print freq, m_currs
#             for k_parts in [2, 3, 5, m_currs/2, m_currs]:
    #             strategy_return = {}
    #             strategy_return['name'] = '{:d}_currs_{:d}_parts'.format(m_currs, k_parts)
                returns = pd.read_pickle(DATA_PATH+'02_single_returns'+os.sep+'20160919_single_returns_{:s}.pickle'.format(freq))

    #             m_currs = 48
    #             k_parts = 5
                return_type_currs = pd.read_pickle(DATA_PATH+'04_return_types'+os.sep+freq+os.sep+('20160919_{:d}_currs_{:d}_liquid_{:d}_parts.pickle').format(len(currency_list), m_currs, k_parts))

                output = []
                for date, return_type_currs_date in return_type_currs.iterrows():

                    temp = {}
                    temp['datetime'] = date
                    return_nums = []
                    for return_type, return_type_curr in return_type_currs_date.iteritems():
    #                     print return_type, return_type_curr
    #                     print list(returns[return_type].ix[date, return_type_curr])
                        return_nums += list(returns[return_type].ix[date, return_type_curr])
    #                 if m_currs == 22 and k_parts == 2:
    #                     print date, return_nums
                    temp['return'] = np.mean(return_nums)
                    output.append(temp)
    #                 break

                strategy_return = pd.DataFrame(output).set_index('datetime')['return']
                strategy_return.name = '{:d}_currs_{:d}_liquid_{:d}_parts'.format(len(currency_list), m_currs, k_parts)
                return_matrix.append(strategy_return)
    #             break

    pd.DataFrame(return_matrix).transpose().to_csv(DATA_PATH+'05_portfolio_returns'+os.sep+today('{:s}.csv').format(freq))
    pd.DataFrame(return_matrix).transpose().to_pickle(DATA_PATH+'05_portfolio_returns'+os.sep+today('{:s}.pickle').format(freq))

        


# In[ ]:




# In[ ]:




# In[136]:

factor = 12.0 / np.array(range(1, len(return48)+1))


# In[138]:

((return48.apply(lambda x: x+1).cumprod()-1)*factor).plot()


# In[139]:

plt.show()


# In[591]:

(return15.apply(lambda x: (x-1)).apply(np.log).plot()
(return48.apply(lambda x: (x-1)).apply(np.log).plot()
plt.legend(['Developed Countries', 'All 48 Countries'], loc='upper left')


# In[23]:

output = pd.concat([return15.apply(lambda x: x*100), return48.apply(lambda x: x*100)], axis=1)
output.columns=['Developed', 'All 48']


# In[24]:

output.to_excel(DATA_PATH+today('15_48_returns.xlsx'))


# In[33]:

output12 = output.applymap(lambda x: x*12)


# In[36]:

pd.DataFrame([output12.mean(), output12.median(), output12.std()], index=['Mean', 'Median', 'Std. dev.'])


# In[39]:

output12.loc[:datetime(2010, 1, 1)].describe()


# In[616]:

return48.apply(lambda x: x*12).describe()


# In[21]:

return48.cumsum().apply(lambda x: x*12+1).apply(np.log).plot()
plt.show()


# In[195]:

"""update"""
p_returns = pd.Series(map(lambda x: pd.read_pickle(DATA_PATH+'05_portfolio_returns'+os.sep+'20160919_{:s}.pickle'.format(x)), freq_list), freq_list)


# In[ ]:




# In[196]:

for i, item in p_returns.iteritems():
    p_returns[i].columns = item.columns.map(lambda x: x+'_'+i)


# In[197]:

func_list = pd.Series([lambda x: '{:d}_{:d}'.format(x.year, pd.Timestamp(x).quarter), 
             lambda x: '{:d}_{:d}'.format(x.year, 1 if x.month <= 6 else 2),
             lambda x: '{:d}'.format(x.year)], freq_list[1:])


# In[198]:

p_returns['1m'].to_pickle(DATA_PATH+'05_portfolio_returns'+os.sep+today('1m_updated.pickle'))
p_returns['1m'].to_csv(DATA_PATH+'05_portfolio_returns'+os.sep+today('1m_updated.csv'))


# In[199]:

#update 3m
freq = '3m'
freq_prev = '1m'

for freq, freq_prev in zip(freq_list[1:], freq_list[:-1]):
    func = func_list[freq]
    return_prev = pd.read_pickle(DATA_PATH+'05_portfolio_returns'+os.sep+('20160919_{:s}_updated.pickle'.format(freq_prev)))

    group_freq = return_prev.groupby(func)

    index_freq = p_returns[freq].index.map(func)

    return_prev_cpd = group_freq.apply(lambda x: x.applymap(lambda x: x+1).product().apply(lambda x: x-1))

    return_prev_cpd = return_prev_cpd.loc[index_freq]

    return_prev_cpd.index = p_returns[freq].index

    return_updated = pd.concat([p_returns[freq], return_prev_cpd], axis=1)

    return_updated.to_pickle(DATA_PATH+'05_portfolio_returns'+os.sep+today('{:s}_updated.pickle'.format(freq)))
    return_updated.to_csv(DATA_PATH+'05_portfolio_returns'+os.sep+today('{:s}_updated.csv'.format(freq)))


# In[ ]:




# In[192]:

#udpate 6m
group_6m = pd.read_pickle(DATA_PATH+'05_portfolio_returns'+os.sep+('20160919_3m_updated.pickle')).groupby(lambda x: '{:d}_{:d}'.format(x.year, 1 if x.month <= 6 else 2))


# In[193]:

index_6m = p_returns['6m'].index.map(lambda x: '{:d}_{:d}'.format(x.year, 1 if x.month <= 6 else 2))


# In[194]:

return_6m_3m = group_6m.apply(lambda x: x.applymap(lambda x: x+1).product().apply(lambda x: x-1))


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:

"""backup"""
row_len = 4
col_len = 2


plt.clf()
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
with PdfPages(DATA_PATH+'pics'+os.sep+'long_cont_cumulative.pdf') as pdf:
    counter = 1
    page = 1
#     print doc_topics
    for number, curr in long_cont.iteritems():
        plt.subplot(row_len, col_len, counter)
#         plt.gca().get_xaxis().set_ticks([])

#         doc_topic[doc_topic>=param[3]].hist()
#         perc = len(doc_topic[doc_topic>0.2]) / float(len(doc_topic))
#         plt.text(param[4], param[5], 'P(p>0.2) = {:0.4f}'.format(perc))
#         plt.text(param[4], param[6], 'max = {:0.4f}'.format(doc_topic.max()))
        curr.apply(lambda x: x+1).cumprod().plot()


        plt.title(str(number), fontsize=10)
        if counter == 8:
            plt.tight_layout()

            pdf.savefig()
            plt.clf()
            print page
#             break
            page += 1
            counter = 0
        counter += 1
    if counter != 1:
        pdf.savefig()


# In[26]:

m_currs_list


# In[ ]:




# In[206]:

output = []
# m_currs = 60
# k_parts = 5
freq = '1m'
# for freq in freq_list:
#     for m_currs in m_currs_list:
#         print m_currs
#         for k_parts in [2, 3, 5, m_currs/2, m_currs]:
currencies_list = pd.read_pickle(DATA_PATH+('20160919_currencies_list.pickle'))[[15, 48]]
for freq in freq_list[:]:
#     return_matrix = []
    for currency_list in currencies_list:

    #     if not os.path.exists(DATA_PATH+'portfolio_returns'+os.sep+freq):
    #         os.makedirs(DATA_PATH+'portfolio_returns'+os.sep+freq)
        for m_currs in range(10, len(currency_list)+1, 2) + [len(currency_list)] if len(currency_list)%2 else range(10, len(currency_list)+1, 2):
#             print freq, m_currs
            for k_parts in [2, 3, 5, m_currs/2, m_currs]:
                currency_num = len(currency_list)

#                 strategy = pd.read_pickle(DATA_PATH+'strategies'+os.sep+freq+os.sep+('20160703_{:d}_currs_{:d}_parts.p').format(m_currs, k_parts)).set_index('datetime').shift(1)
                strategy = pd.read_pickle(DATA_PATH+'03_long_short'+os.sep+freq+os.sep+('20160919_{:d}_currs_{:d}_liquid_{:d}_parts.p').format(currency_num, m_currs, k_parts)).set_index('datetime').shift(1)

                traded_currs = strategy.apply(lambda x: 'long: {:s}, short: {:s}'.format(re.sub('set|[\(\)\'\[\]]', '', str(x['long'])), re.sub('set|[\(\)\'\[\]]', '', str(x['short']))), axis=1)

                name = '{:d}_currs_{:d}_liquid_{:d}_parts_{:s}'.format(currency_num, m_currs, k_parts, freq)

                traded_currs.name = name
                output.append(traded_currs)


# In[ ]:




# In[207]:

output_df = pd.DataFrame(output).T


# In[209]:

output_df.to_csv(DATA_PATH+'03_long_short'+os.sep+today('traded_currs.csv'))


# In[212]:

output_df['48_currs_48_liquid_48_parts_1m']


# In[ ]:



