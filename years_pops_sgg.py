import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import os

# 1. 데이터 준비
# 현재 파일(__init__.py)의 디렉토리 경로
pkgDir = os.path.dirname(__file__)

# 엑셀파일 읽기
csvPath = os.path.join(pkgDir, "data/sgg_2019_2023_long.csv")
data = pd.read_csv(csvPath)

# 데이터 확인 및 변환
data['year'] = data['year'].astype(int)  # year를 정수형으로 변환
categories = ['총인구수', '세대수', '세대당 인구', '남자 인구수', '여자 인구수', '남여 비율']

# 2. Dash 앱 생성
app = dash.Dash(__name__)
app.title = "인구 데이터 대시보드"

# 3. 레이아웃 정의
app.layout = html.Div([
    html.H1("인구 데이터 대시보드", style={"text-align": "center"}),

    # Dropdowns for Year, Sido, Sgg, and Category
    html.Div([
        html.Label("년도 선택:"),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": str(year), "value": year} for year in sorted(data['year'].unique())],
            value=sorted(data['year'].unique())[0],
            clearable=False
        ),
        html.Label("시도 선택:"),
        dcc.Dropdown(
            id="sido-dropdown",
            options=[{"label": "시도를 선택하세요", "value": None}],
            value=None,
            clearable=False
        ),
        html.Label("시군구 선택:"),
        dcc.Dropdown(
            id="sgg-dropdown",
            options=[{"label": "시군구를 선택하세요", "value": None}],
            value=None,
            clearable=False
        ),
        html.Label("유형 선택:"),
        dcc.Dropdown(
            id="category-dropdown",
            options=[{"label": category, "value": category} for category in categories],
            value="총인구수",
            clearable=False
        ),
    ], style={"width": "50%", "margin": "auto"}),

    # Graph
    dcc.Graph(id="bar-graph")
])

# 4. 콜백 정의

# 시도 Dropdown 업데이트
@app.callback(
    Output("sido-dropdown", "options"),
    Input("year-dropdown", "value")
)
def update_sido_options(selected_year):
    # 년도에 따라 시도를 필터링
    available_sidos = data[data['year'] == selected_year]['sido'].unique()
    return [{"label": "전체", "value": "전체"}] + [{"label": sido, "value": sido} for sido in sorted(available_sidos)]

# 시군구 Dropdown 업데이트
@app.callback(
    Output("sgg-dropdown", "options"),
    [Input("year-dropdown", "value"), Input("sido-dropdown", "value")]
)
def update_sgg_options(selected_year, selected_sido):
    if selected_sido in [None, "전체"]:
        return [{"label": "전체", "value": "전체"}]
    available_sggs = data[(data['year'] == selected_year) & (data['sido'] == selected_sido)]['sgg'].unique()
    return [{"label": "전체", "value": "전체"}] + [{"label": sgg, "value": sgg} for sgg in sorted(available_sggs)]




# 5. 앱 실행
if __name__ == "__main__":
    app.run_server(debug=True)
