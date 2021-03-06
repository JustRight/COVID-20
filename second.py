import pandas as pd
# 导入matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker
import datetime

# 读取数据
today_world = pd.read_csv("today_world_2020_04_03.csv")
name_dict = {'date':'日期','name':'名称','id':'编号','lastUpdateTime':'更新时间',
             'today_confirm':'当日新增确诊','today_suspect':'当日新增疑似',
             'today_heal':'当日新增治愈','today_dead':'当日新增死亡',
             'today_severe':'当日新增重症','today_storeConfirm':'当日现存确诊',
             'total_confirm':'累计确诊','total_suspect':'累计疑似',
             'total_heal':'累计治愈','total_dead':'累计死亡','total_severe':'累计重症',
             'total_input':'累计输入病例','today_input':'当日输入病例'}

# 更改列名
today_world.rename(columns=name_dict,inplace=True)    # inplace参数判断是否在原数据上进行修改

# 缺失值处理
today_world['当日现存确诊'] = today_world['累计确诊']-today_world['累计治愈']-today_world['累计死亡']

print(today_world.head())
print(today_world.info())# 查看数据基本信息
print(today_world.describe())# 默认只计算数值型特征的统计信息

# 计算缺失值比例
today_world_nan = today_world.isnull().sum()/len(today_world)
# 转变为百分数
print(today_world_nan.apply(lambda x: format(x, '.1%')) )

# 计算病死率,且保留两位小数
today_world['病死率'] = (today_world['累计死亡']/today_world['累计确诊']).apply(lambda x: format(x, '.2f'))
# 将病死率数据类型转换为float
today_world['病死率'] = today_world['病死率'].astype('float')
# 根据病死率降序排序
today_world.sort_values('病死率',ascending=False,inplace=True)
print(today_world.head(10))# 显示病死率前十国家

# 将国家名称设为索引
today_world.set_index('名称',inplace=True)
print(today_world.head(3))

print(today_world.loc['中国'])#可以通过传入列表获取指定国家的数据

# 查看当前累计确诊人数前十国家
world_top10 = today_world.sort_values(['累计确诊'],ascending=False)[:10]
world_top10 = world_top10[['累计确诊','累计死亡','病死率']]
print(world_top10)

#绘图准备
plt.rcParams['font.sans-serif']=['SimHei']    #正常显示中文
plt.rcParams['figure.dpi'] = 120      #设置所有图片的清晰度
# 绘制条形图
world_top10.sort_values('累计确诊').plot.barh(subplots=True,layout=(1,3),sharex=False,
                                             figsize=(7,4),legend=False,sharey=True)
plt.tight_layout()   #调整子图间距
plt.show()

# 读取数据
today_province = pd.read_csv("today_province_2020_04_03.csv")
# 创建中文列名字典
name_dict = {'date':'日期','name':'名称','id':'编号','lastUpdateTime':'更新时间',
             'today_confirm':'当日新增确诊','today_suspect':'当日新增疑似',
             'today_heal':'当日新增治愈','today_dead':'当日新增死亡',
             'today_severe':'当日新增重症','today_storeConfirm':'当日现存确诊',
             'total_confirm':'累计确诊','total_suspect':'累计疑似',
             'total_heal':'累计治愈','total_dead':'累计死亡','total_severe':'累计重症',
             'total_input':'累计输入病例','today_input':'当日输入病例'}

# 更改列名
today_province.rename(columns=name_dict,inplace=True)    # inplace参数是否在原对象基础上进行修改
print(today_province.head())
print(today_province.info())# 查看数据基本信息
print(today_province.describe())# 查看数值型特征的统计量

# 计算各省当日现存确诊人数
today_province['当日现存确诊'] = today_province['累计确诊']-today_province['累计治愈']-today_province['累计死亡']
# 将各省名称设置为索引
today_province.set_index('名称',inplace=True)
print(today_province.info())

# 查看全国新增确诊top10的地区,new_top6 就是指代新增确诊的10个地区
new_top6 = today_province['当日新增确诊'].sort_values(ascending=False)[:10]
print(new_top6)

# 绘制条形图和饼图
fig,ax = plt.subplots(1,2,figsize=(10,5))
new_top6.sort_values(ascending=True).plot.barh(fontsize=10,ax=ax[0])
new_top6.plot.pie(autopct='%.1f%%',fontsize=10,ax=ax[1])
plt.ylabel('')
plt.title('全国新增确诊top10地区',size=15)
plt.show()

# 查看全国现存确诊人数top10的省市
store_top10 = today_province['当日现存确诊'].sort_values(ascending=False)[:10]
print(store_top10)

# 绘制条形图
store_top10.sort_values(ascending=True).plot.barh(fontsize=10)
plt.title('全国现存确诊top10地区',size=15)
plt.show()

#全国历史数据探索性分析
# 读取数据
alltime_china = pd.read_csv("alltime_China_2020_04_03.csv")

# 创建中文列名字典
name_dict = {'date':'日期','name':'名称','id':'编号','lastUpdateTime':'更新时间',
             'today_confirm':'当日新增确诊','today_suspect':'当日新增疑似',
             'today_heal':'当日新增治愈','today_dead':'当日新增死亡',
             'today_severe':'当日新增重症','today_storeConfirm':'当日现存确诊',
             'total_confirm':'累计确诊','total_suspect':'累计疑似',
             'total_heal':'累计治愈','total_dead':'累计死亡','total_severe':'累计重症',
             'total_input':'累计输入病例','today_input':'当日输入病例'}
# 更改列名
alltime_china.rename(columns=name_dict,inplace=True)
print(alltime_china.head())
print(alltime_china.info())
print(alltime_china.describe())

# 缺失值处理
# 计算当日现存确诊人数
alltime_china['当日现存确诊'] = alltime_china['累计确诊']-alltime_china['累计治愈']-alltime_china['累计死亡']
# 删除更新时间一列
alltime_china.drop(['更新时间','当日新增重症'],axis=1,inplace=True)
print(alltime_china.info())

# 将日期改成datetime格式
alltime_china['日期'] = pd.to_datetime(alltime_china['日期'])
# 设置日期为索引
alltime_china.set_index('日期',inplace=True)     # 也可使用pd.read_csv("./input/alltime_China_2020_03_27.csv",parse_dates=['date'],index_col='date')
print(alltime_china.index)

# 举例
print(alltime_china.loc['2020-01'])

# 时间序列数据绘制折线图
fig, ax = plt.subplots(figsize=(8,4))
alltime_china.plot(marker='o',ms=2,lw=1,ax=ax)
ax.xaxis.set_major_locator(dates.MonthLocator())    #设置间距
ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))    #设置日期格式
fig.autofmt_xdate()    #自动调整日期倾斜
# 图例位置调整
plt.legend(bbox_to_anchor = [1,1])
plt.title('全国新冠肺炎数据折线图',size=15)
plt.ylabel('人数')
plt.grid(axis='y')
plt.box(False)
plt.show()

# 时间序列数据绘制折线图
fig, ax = plt.subplots(figsize=(8,4))
alltime_china['当日新增确诊'].plot(ax=ax, style='-',lw=1,color='c',marker='o',ms=3)
ax.xaxis.set_major_locator(dates.MonthLocator())    #设置间距
ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))    #设置日期格式
fig.autofmt_xdate()    #自动调整日期倾斜
plt.title('全国新冠肺炎新增确诊病例折线图',size=15)
plt.ylabel('人数')
plt.grid(axis='y')
plt.box(False)
plt.show()

#世界各国历史数据探索性分析
# 读取数据
alltime_world = pd.read_csv("alltime_world_2020_04_04.csv")
# 创建中文列名字典
name_dict = {'date':'日期','name':'名称','id':'编号','lastUpdateTime':'更新时间',
             'today_confirm':'当日新增确诊','today_suspect':'当日新增疑似',
             'today_heal':'当日新增治愈','today_dead':'当日新增死亡',
             'today_severe':'当日新增重症','today_storeConfirm':'当日现存确诊',
             'total_confirm':'累计确诊','total_suspect':'累计疑似',
             'total_heal':'累计治愈','total_dead':'累计死亡','total_severe':'累计重症',
             'total_input':'累计输入病例','today_input':'当日输入病例'}

# 更改列名
alltime_world.rename(columns=name_dict,inplace=True)
print(alltime_world.head())
print(alltime_world.info())# 查看数据基本信息
print(alltime_world.describe())

# 将日期一列数据类型变为datetime
alltime_world['日期'] = pd.to_datetime(alltime_world['日期'])
# 计算当日现存确诊
alltime_world['当日现存确诊'] = alltime_world['累计确诊']-alltime_world['累计治愈']-alltime_world['累计死亡']
print(alltime_world.info())

# 查看唯一值,可使用len()查看个数
alltime_world['名称'].unique()

# 统计每天有多少国家出现疫情，即哪20天疫情出现的最多
alltime_world['日期'].value_counts().head(20)

# 设置日期索引
alltime_world.set_index('日期',inplace=True)
# 3月31日数据统计不完全，我们将其删除
alltime_world = alltime_world.loc[:'2020-03-31']

# groupby创建层次化索引
data = alltime_world.groupby(['日期','名称']).mean()
print(data.head())

# 提取部分数据
data_part = data.loc(axis=0)[:,['中国','日本','韩国','美国','意大利','英国','西班牙','德国']]
print(data_part.head())

# 将层级索引还原
data_part.reset_index('名称',inplace=True)
print(data_part.head())

# 绘制多个国家的累计确诊人数折线图
fig, ax = plt.subplots(figsize=(8,4))
data_part['2020-02':].groupby('名称')['累计确诊'].plot(legend=True,marker='o',ms=3,lw=1)
ax.xaxis.set_major_locator(dates.MonthLocator())    #设置间距
ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))    #设置日期格式
fig.autofmt_xdate()    #自动调整日期倾斜
plt.title('各国新冠肺炎累计确诊病例折线图',size=15)
plt.ylabel('人数')
plt.grid(axis='y')
plt.box(False)
plt.legend(bbox_to_anchor = [1,1])
plt.show()

# 绘制各国新增确诊人数折线图
fig, ax = plt.subplots(figsize=(8,4))
data_part['2020-03':'2020-03-29'].groupby('名称')['当日新增确诊'].plot(legend=True,marker='o',ms=3,lw=1)
ax.xaxis.set_major_locator(dates.MonthLocator())    #设置间距
ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))    #设置日期格式
fig.autofmt_xdate()    #自动调整日期倾斜
plt.title('各国新冠肺炎新增确诊病例折线图',size=15)
plt.ylabel('人数')
plt.grid(axis='y')
plt.box(False)
plt.legend(bbox_to_anchor = [1,1])
plt.show()

#绘制日本新冠肺炎疫情折线图
japan = alltime_world[alltime_world['名称']=='日本']
fig, ax = plt.subplots(figsize=(8,4))
japan['累计确诊'].plot(ax=ax, fontsize=10, style='-',lw=1,color='c',marker='o',ms=3,legend=True)
ax.set_ylabel('人数', fontsize=10)
ax1 = ax.twinx()
ax1.bar(japan.index, japan['当日新增确诊'])
ax1.xaxis.set_major_locator(dates.DayLocator(interval = 5))
ax1.xaxis.set_major_formatter(dates.DateFormatter('%b %d'))
ax1.legend(['当日新增确诊'],loc='upper left',bbox_to_anchor=(0.001, 0.9))
plt.grid(axis='y')
plt.box(False)
plt.title('日本新冠肺炎疫情折线图',size=15)
plt.show()



