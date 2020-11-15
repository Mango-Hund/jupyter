import numpy as np
import csv
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import Circle,MultiLine
import bokeh.plotting as bk
from bokeh.models import GMapOptions
from bokeh.io import output_file, show, save
import pandas as pd

#打开并读取数据
rowdata = open(r'TSNE.csv', "r")
reader = csv.reader(rowdata)
headers = next(reader)

loc_x,loc_y,clu_x,clu_y,ser_x,ser_y = [],[],[],[],[],[]

for row in reader:
    print(row)
    loc_x.append(float(row[1]))
    loc_y.append(float(row[2]))
    clu_x.append(float(row[3]))
    clu_y.append(float(row[4]))
    #ser_x.append(list(range(1,366)))
    ser_x.append(pd.date_range('2017-1-1', periods=365))
    ser_y.append(list(row[5:]))

#输出文件
output_file('play.html')

#定义数据源
source = ColumnDataSource(data=dict(x=loc_x,y=loc_y,xp=clu_x,yp=clu_y,xq=ser_x,yq=ser_y))


#定义谷歌地图API
api_key = "AIzaSyAAaqxUMuZ4QeZRWkXoouK4_MYaw5340Mg"
mid_lat = 31.1
mid_lon = 121.7
map_options = GMapOptions(lat = mid_lat, lng = mid_lon, map_type="terrain", zoom=10)  #satellite, roadmap, terrain or hybrid

#画地图
TOOLS = 'box_select,lasso_select,help'
left = bk.gmap(tools=TOOLS,google_api_key = api_key, map_options = map_options, x_axis_label='GPS-X', y_axis_label='GPS-Y')  #,title='Location distribution of different users based on power consumption patterns'
left.title.text_font_size = '10pt'    #标题字体
left.xaxis.axis_label_text_font_size = "15pt"  #坐标轴字体
left.yaxis.axis_label_text_font_size = "15pt"
c1 = left.circle('x','y', source=source)
c1.nonselection_glyph = Circle(fill_color='gray',fill_alpha=0.4, line_color=None)
c1.selection_glyph = Circle(fill_color='orange',line_color=None)

#画拓扑图
middle = figure(tools=TOOLS,plot_width=600,plot_height=600,x_axis_label='Topological relationship', y_axis_label='Topological relationship')  #,title='Logical topology distribution of different users based on power consumption patterns'
middle.title.text_font_size = '10pt'    #标题字体
middle.xaxis.axis_label_text_font_size = "15pt"  #坐标轴字体
middle.yaxis.axis_label_text_font_size = "15pt"
c2 = middle.circle('xp','yp', source=source)
c2.nonselection_glyph = Circle(fill_color='gray',fill_alpha=0.4, line_color=None)
c2.selection_glyph = Circle(fill_color='orange',line_color=None)

#画时序数据
right = figure(tools=TOOLS,plot_width=600,plot_height=600,x_axis_type='datetime',y_range=[0, 1500], x_axis_label='Time series (365 days)', y_axis_label='Daily power consumption (kWh)') #,title='Electricity consumption data of different users'
right.title.text_font_size = '10pt'    #标题字体
right.xaxis.axis_label_text_font_size = "15pt"  #坐标轴字体
right.yaxis.axis_label_text_font_size = "15pt"
c3 = right.multi_line(xs='xq',ys='yq',source=source)
c3.nonselection_glyph = MultiLine(line_color='gray',line_alpha=0.2)
c3.selection_glyph = MultiLine(line_color='orange')

p = gridplot([[left, middle, right]])
show(p)