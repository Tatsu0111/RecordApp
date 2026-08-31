import plotly.graph_objects as go
from datetime import datetime

def get_cumulative_profit(summary):
    cumulative = []
    total = 0
    for row in summary:
        total += row['profit']
        cumulative.append(total)
    return cumulative

def create_lifetime_graph(summary):
    x = [datetime.strptime(row['date'], '%Y-%m-%d')for row in summary]
    cumulative = get_cumulative_profit(summary)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=cumulative, mode='lines+markers', name='累計収支'))
    fig.update_xaxes(tickformat='%m/%d',title='日付')
    fig.update_layout(title='収支グラフ', yaxis_title='収支（円）')
    return fig

def create_yearly_graph(summary):
    x = [row['year'] for row in summary]
    profit = [row['profit'] for row in summary]
    cumulative = get_cumulative_profit(summary)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=profit, name='年別収支'))
    fig.add_trace(go.Scatter(x=x, y=cumulative, mode='lines+markers', name='累計収支'))
    fig.update_layout(title='収支グラフ', xaxis_title='年', yaxis_title='収支（円）')
    return fig

def create_monthly_graph(summary):
    x = [row['ym'] for row in summary]
    profit = [row['profit'] for row in summary]
    cumulative = get_cumulative_profit(summary)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=profit, name='月別収支'))
    fig.add_trace(go.Scatter(x=x, y=cumulative, mode='lines+markers', name='累計収支'))
    fig.update_layout(title='収支グラフ', xaxis_title='月', yaxis_title='収支（円）')
    return fig

def create_daily_graph(summary):
    x = [datetime.strptime(row['ymd'], '%Y-%m-%d')for row in summary]
    profit = [row['profit'] for row in summary]
    cumulative = get_cumulative_profit(summary)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=profit, name='日別収支'))
    fig.add_trace(go.Scatter(x=x, y=cumulative, mode='lines+markers', name='累計収支'))
    fig.update_xaxes(tickformat='%m/%d',title='日付')
    fig.update_layout(title='収支グラフ', yaxis_title='収支（円）')
    return fig

def create_place_graph(summary):
    x = [row['place'] for row in summary]
    profit = [row['profit'] for row in summary]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=profit, name='場所別収支'))
    fig.update_layout(title='収支グラフ', xaxis_title='場所', yaxis_title='収支（円）')
    return fig

def create_category_graph(summary):
    x = [row['category'] for row in summary]
    profit = [row['profit'] for row in summary]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=profit, name='カテゴリ別収支'))
    fig.update_layout(title='収支グラフ', xaxis_title='カテゴリ', yaxis_title='収支（円）')
    return fig