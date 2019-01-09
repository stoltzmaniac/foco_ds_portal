import pandas as pd
import altair as alt


def download_csv() -> pd.DataFrame:
    url = "http://samplecsvs.s3.amazonaws.com/SacramentocrimeJanuary2006.csv"
    data = pd.read_csv(url)
    return data[0:1000]


def plot_altair() -> alt.Chart:
    data = download_csv()
    base = alt.Chart(data)
    # Build chart
    bar = base.mark_bar().encode(
        x=alt.X('latitude', bin=True, axis=None),
        y='count()'
    )
    return bar
