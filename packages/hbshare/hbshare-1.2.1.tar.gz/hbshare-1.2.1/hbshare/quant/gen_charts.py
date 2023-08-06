from hbshare.quant.load_data import load_funds_data, load_funds_alpha
import pandas as pd
import numpy as np
import pyecharts.options as opts
from datetime import datetime, timedelta
from pyecharts.charts import Line, Tab, Grid
from pyecharts.globals import ThemeType
import pymysql
from sqlalchemy import create_engine

pymysql.install_as_MySQLdb()


def nav_lines(
        fund_list, start_date, end_date,
        title='', zz=False, axis_cross=None, db_path='', cal_path='', all_selected=True
):
    if axis_cross:
        axis_cross = opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")

    if zz:
        funds_data = load_funds_alpha(
            fund_list=fund_list,
            first_date=start_date,
            end_date=end_date,
            db_path=db_path,
            cal_db_path=cal_path
        )['eav']
    else:
        funds_data = load_funds_data(
            fund_list=fund_list,
            first_date=start_date,
            end_date=end_date,
            db_path=db_path,
            cal_db_path=cal_path,
            # freq='',
            # fillna=False
        )

    web = Line(
        init_opts=opts.InitOpts(
            page_title=title,
            width='700px',
            height='500px',
            theme=ThemeType.CHALK
        )
    ).set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=True),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    ).add_xaxis(
        xaxis_data=funds_data['t_date'].tolist()
    )
    funds = funds_data.columns.tolist()

    funds.remove('t_date')
    for j in funds:
        nav_data = funds_data[j] / funds_data[funds_data[j] > 0][j].tolist()[0]
        web.add_yaxis(
            series_name=j,
            y_axis=nav_data.round(4).tolist(),
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
            is_selected=all_selected
        )

    web.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            is_scale=True,
            type_="category", boundary_gap=False
        ),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        legend_opts=opts.LegendOpts(
            # type_='scroll',
            pos_top='5%'
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ],
        title_opts=opts.TitleOpts(title=title),
        tooltip_opts=axis_cross
    )

    return web


def gen_grid(
        end_date, funds, zz=False,
        lookback_years=3, grid_width=1200, grid_height=500, axis_cross=None, db_path='', cal_path='', all_selected=True
):
    if axis_cross:
        axis_cross = opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")

    engine = create_engine(db_path)
    start_date = end_date - timedelta(days=365 * lookback_years + 7)
    start_date2 = end_date - timedelta(days=365 + 7)
    if len(funds) > 1:
        fund_list = pd.read_sql_query(
            'select * from fund_list where `name` in ' + str(tuple(funds)) + ' order by `name`', engine
        )
    else:
        fund_list = pd.read_sql_query(
            'select * from fund_list where `name`="' + str(funds[0]) + '"', engine
        )

    grid_nav = Grid(init_opts=opts.InitOpts(width=str(grid_width) + "px", height=str(grid_height) + "px"))

    web = nav_lines(
        fund_list=fund_list,
        start_date=start_date,
        end_date=end_date,
        zz=zz,
        db_path=db_path,
        cal_path=cal_path,
        all_selected=all_selected
    )

    web2 = nav_lines(
        fund_list=fund_list,
        start_date=start_date2,
        end_date=end_date,
        zz=zz,
        db_path=db_path,
        cal_path=cal_path,
        all_selected=all_selected
    )

    grid_nav.add(
        web.set_global_opts(
            title_opts=opts.TitleOpts(
                title='近' + str(lookback_years) + '年: '
                      + start_date.strftime('%Y/%m/%d') + '~' + end_date.strftime('%Y/%m/%d')
                ,
                pos_right="5%"
            ),
            tooltip_opts=axis_cross,
            legend_opts=opts.LegendOpts(
                pos_top="7%"
            )
        ),
        grid_opts=opts.GridOpts(pos_left='55%', pos_top="23%")
    ).add(
        web2.set_global_opts(
            title_opts=opts.TitleOpts(
                title='近一年: '
                      + start_date2.strftime('%Y/%m/%d') + '~' + end_date.strftime('%Y/%m/%d')
                ,
                pos_left="5%"
            ),
            tooltip_opts=axis_cross,
            legend_opts=opts.LegendOpts(
                pos_top="7%"
            )
        ),
        grid_opts=opts.GridOpts(pos_right='55%', pos_top="23%")
    )
    return grid_nav

