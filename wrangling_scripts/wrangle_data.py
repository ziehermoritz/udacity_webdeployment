#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to wrangle data for the web deployment page.
In the course of the data science udacity nanodegree.

Author: Mo Zi
Date: 22.02.2024
"""
import pandas as pd
import plotly.graph_objs as go


def return_figures():
    """Create five plotly visualizations.

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    # read in world bank commodity data
    wb_data = pd.read_excel(
        'data/CMO-Historical-Data-Monthly.xlsx',
        sheet_name='Monthly Prices',
        header=4)

    # get the first column name an rename it
    first_col = list(wb_data.columns)[0]
    wb_data.rename(columns={first_col: 'YearMonth'}, inplace=True)

    # get units of spreadsheet
    units_lst = list(wb_data.iloc[0])

    # drop remaining header rows
    wb_data.drop([0, 1], inplace=True)

    # get column names of gold, platinum and silver
    cols_of_interest = wb_data.columns[-3:].to_list()  # columns of interest
    # also get year-month column
    cols_of_interest.insert(0, wb_data.columns[0])

    # filter world bank data to the columns of interest
    wb_data_filtered = wb_data[cols_of_interest]

    # remove months from years
    wb_data_filtered.loc[:,
                         'YearMonth'] = wb_data_filtered['YearMonth'].str[:4]

    # compute average over a year
    avg_wb_data = wb_data_filtered.groupby('YearMonth').mean()

    # set up gold price diagramm
    gold_df = avg_wb_data.loc[:, 'Gold']
    gold_df = gold_df.reset_index()

    gold_graph = []
    # f"Gold Price {units_lst[-3].strip('()')}"
    # gold_graph.append(px.scatter(gold_df, x='YearMonth', y='Gold'))
    gold_graph.append(go.Scatter(x=avg_wb_data.index.to_list(),
                                 y=avg_wb_data.loc[:,
                      'Gold'].to_list(),
                                 mode='lines',
                                 line=dict(color="#baa952")))

    gold_layout = dict(
        title="Avg. Gold Price",
        xaxis=dict(
            title='Year',
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                1960,
                2025]),
        yaxis=dict(
            title=f"Price [{units_lst[-3].strip('()')}]",
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                0,
                2200]))

    # set up platinum price diagramm
    platinum_df = avg_wb_data.loc[:, 'Platinum']
    platinum_df = platinum_df.reset_index()

    platinum_graph = []
    platinum_graph.append(go.Scatter(x=avg_wb_data.index.to_list(
    ), y=avg_wb_data.loc[:, 'Platinum'].to_list(), mode='lines',
        line=dict(color="#6a6a8d")))

    platinum_layout = dict(
        title="Avg. Platinum Price",
        xaxis=dict(
            title='Year',
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                1960,
                2025]),
        yaxis=dict(
            title=f"Price [{units_lst[-3].strip('()')}]",
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                0,
                2200]))
    # set up silver price diagramm
    silver_df = avg_wb_data.loc[:, 'Silver']
    silver_df = silver_df.reset_index()

    silver_graph = []
    # silver_graph.append(px.scatter(silver_df, x='YearMonth', y='Silver'))
    silver_graph.append(go.Scatter(x=avg_wb_data.index.to_list(
    ), y=avg_wb_data.loc[:, 'Silver'].to_list(), mode='lines',
        line=dict(color="#a6a6a6")))

    silver_layout = dict(
        title="Avg. Silver Price",
        xaxis=dict(
            title='Year',
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                1960,
                2025]),
        yaxis=dict(
            title=f"Price [{units_lst[-3].strip('()')}]",
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                0,
                45]))

    stat_df = pd.concat(
        [pd.to_numeric(wb_data_filtered['YearMonth'], errors='coerce'),
         pd.to_numeric(wb_data_filtered['Gold'], errors='coerce'),
         pd.to_numeric(wb_data_filtered['Platinum'], errors='coerce'),
         pd.to_numeric(wb_data_filtered['Silver'], errors='coerce')], axis=1)

    desc_df = stat_df.groupby('YearMonth').describe()

    # Gold error bars
    gold_mean = desc_df.loc[:, 'Gold'].loc[:, 'mean']
    gold_min = desc_df.loc[:, 'Gold'].loc[:, 'mean'] - \
        desc_df.loc[:, 'Gold'].loc[:, 'min']
    gold_max = desc_df.loc[:, 'Gold'].loc[:, 'max'] - \
        desc_df.loc[:, 'Gold'].loc[:, 'mean']

    gold_df = pd.concat([gold_mean, gold_min, gold_max], axis=1)
    gold_df = gold_df.reset_index()
    gold_df.columns = ['YearMonth', 'mean', 'min', 'max']

    gold_error = []
    gold_error_y = dict(type='data',
                        symmetric=False,
                        array=gold_df.loc[:,
                                          'max'].to_numpy(),
                        arrayminus=gold_df.loc[:,
                                               'min'].to_numpy())
    gold_error.append(go.Scatter(x=gold_df['YearMonth'].to_list(),
                                 y=gold_df.loc[:,
                                               'mean'],
                                 error_y=gold_error_y,
                                 name="avg. price per year",
                                 line=dict(color="#baa952")))
    gold_error_layout = dict(
        title="Min/Max Gold Price per Year",
        xaxis=dict(
            title='Year',
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                1960,
                2025]),
        yaxis=dict(
            title=f"Price [{units_lst[-3].strip('()')}]",
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                0,
                2200]),
        showlegend=True)

    # Platinum error bars
    platinum_mean = desc_df.loc[:, 'Platinum'].loc[:, 'mean']
    platinum_min = (desc_df.loc[:,
                                'Platinum'].loc[:,
                    'mean'] - desc_df.loc[:,
                                          'Platinum'].loc[:,
                    'min'])
    platinum_max = (desc_df.loc[:,
                                'Platinum'].loc[:,
                    'max'] - desc_df.loc[:,
                                         'Platinum'].loc[:,
                    'mean'])

    platinum_df = pd.concat(
        [platinum_mean, platinum_min, platinum_max], axis=1)
    platinum_df = platinum_df.reset_index()
    platinum_df.columns = ['YearMonth', 'mean', 'min', 'max']

    platinum_error = []
    platinum_error_y = dict(type='data',
                            symmetric=False,
                            array=platinum_df.loc[:,
                                                  'max'].to_numpy(),
                            arrayminus=platinum_df.loc[:,
                                                       'min'].to_numpy())
    platinum_error.append(go.Scatter(x=platinum_df['YearMonth'].to_list(
    ), y=platinum_df.loc[:, 'mean'], error_y=platinum_error_y,
        name="avg. price per year", line=dict(color="#6a6a8d")))
    platinum_error_layout = dict(
        title="Min/Max Platinum Price per Year",
        xaxis=dict(
            title='Year',
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                1960,
                2025]),
        yaxis=dict(
            title=f"Price [{units_lst[-3].strip('()')}]",
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                0,
                2200]),
        showlegend=True)

    # Silver error bars
    silver_mean = desc_df.loc[:, 'Silver'].loc[:, 'mean']
    silver_min = (desc_df.loc[:,
                              'Silver'].loc[:,
                  'mean'] - desc_df.loc[:,
                                        'Silver'].loc[:,
                  'min'])
    silver_max = (desc_df.loc[:, 'Silver'].loc[:, 'max'] -
                  desc_df.loc[:, 'Silver'].loc[:, 'mean'])

    silver_df = pd.concat([silver_mean, silver_min, silver_max], axis=1)
    silver_df = silver_df.reset_index()
    silver_df.columns = ['YearMonth', 'mean', 'min', 'max']

    silver_error = []
    silver_error_y = dict(type='data',
                          symmetric=False,
                          array=silver_df.loc[:,
                                              'max'].to_numpy(),
                          arrayminus=silver_df.loc[:,
                                                   'min'].to_numpy())
    silver_error.append(go.Scatter(x=silver_df['YearMonth'].to_list(
    ), y=silver_df.loc[:, 'mean'], error_y=silver_error_y,
        name="avg. price per year", line=dict(color="#a6a6a6")))
    silver_error_layout = dict(
        title="Min/Max Silver Price per Year",
        xaxis=dict(
            title='Year',
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                1960,
                2025]),
        yaxis=dict(
            title=f"Price [{units_lst[-3].strip('()')}]",
            mirror=True,
            ticks='inside',
            showline=True,
            range=[
                0,
                45]),
        showlegend=True)

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=gold_graph, layout=gold_layout))
    figures.append(dict(data=platinum_graph, layout=platinum_layout))
    figures.append(dict(data=silver_graph, layout=silver_layout))
    # -
    figures.append(dict(data=gold_error, layout=gold_error_layout))
    figures.append(dict(data=platinum_error, layout=platinum_error_layout))
    figures.append(dict(data=silver_error, layout=silver_error_layout))

    return figures


if __name__ == '__main__':
    figures = return_figures()
