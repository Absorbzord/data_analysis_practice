import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

file_path = 'multiple_choice_responses.csv'
df = pd.read_csv(file_path)
df = df[1:]

# print(df.head())

#Zadanie 1

fig1 = px.histogram(
    df,
    x = "Q2",
    title = "Zadanie 1: Rozkład płci",
    labels = {"Q2": "Gender", "count": "Count"}
)
fig1.show()

# Zadanie 2

fig2 = px.bar(
    df,
    x = "Q1",
    color = "Q2",
    title = "Zadanie 2: Zgrupowany rozkład płci",
    labels = {"Q1": "Age", "value": "Gender", "count": "Count"}
)
fig2.show()

# Zadanie 3 

# 3.1
fig3_1 = px.histogram(
    df,
    x = "Q4",
    title = "Zadanie 3.1: Formalne wykształcenie uczestników",
    labels = {"Q4": "Education level", "count": "Count"}
)
fig3_1.show()

# 3.2
fig3_2 = px.bar(
    df,
    x = "Q4",
    color = "Q2",
    title = "Zadanie 3.2: Liczba formalnego wykształcenia wg płci",
    labels = {"Q4": "Education level", "Q2": "Gender", "count": "Count"},
    barmode = "group"
)
fig3_2.show()

# Zadanie 4

language_columns = [col for col in df.columns if col.startswith('Q16_Part_')]

age_column = 'Q1'
language_data = df.groupby(age_column)[language_columns].count()
language_percentages = language_data.div(language_data.sum(axis=1), axis=0) * 100

fig4 = make_subplots(
    rows=4, cols=3,
    subplot_titles=language_percentages.columns.tolist(),
    vertical_spacing=0.1
)

row, col = 1, 1

for language in language_percentages.columns:

    fig4.add_trace(
        go.Bar(
            x = language_percentages.index,
            y = language_percentages[language], 
            name=language
        ),
        row=row, col=col
    )
    col += 1
    if col > 3: 
        col = 1
        row += 1

fig4.update_layout(
    height=800, width=1000,
    title_text="Percentage of Known Programming Languages by Age",
    showlegend=False
)

fig4.update_xaxes(title_text="Age Group")
fig4.update_yaxes(title_text="Percentage")

fig4.show()
# Zadanie 5
job_title = "Q5"

languages = [col for col in df.columns if col.startswith("Q16_part_")]

heatmap = df[[job_title] + languages]
heatmap[languages] = heatmap[languages].isnull().astype(int)
heatmap_matrix = heatmap.groupby(job_title).sum()

fig5 = px.imshow(
    heatmap_matrix,
    title = "Zadanie 5: Powiązanie j. programowania i nazwy zawodu",
    labels = {"x": "Programming Language", "y": "Job Title", "color": "Count"},
    x = languages,
    y = heatmap_matrix.index,
    color_continuous_scale = "Viridis"
)
fig5.show()

# Zadanie 6
gender = "Q2"
salary = "Q10"
boxplot = df[[gender, salary]].dropna()

fig6 = px.box(
    boxplot,
    x = gender,
    y = salary,
    title = "Zadanie 6: Salary per gender",
    labels = {gender: "Gender", salary: "Salary"},
    color = gender
)
fig6.show()