import timeit
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# from PIL import Image
from io import BytesIO
import xlsxwriter


sns.set_theme(style="ticks", rc={"axes.spines.right": False, "axes.spines.top": False})


# FUNÇÃO PARA CARREGAR OS DADOS
@st.cache_data(show_spinner=True)
def load_data(file_data: str, sep: str) -> pd.DataFrame:
    try:
        return pd.read_csv(filepath_or_buffer=file_data, sep=sep)
    except:
        return pd.read_excel(io=file_data)


@st.cache_data
def multiselect_filter(
    data: pd.DataFrame, col: str, selected: list[str]
) -> pd.DataFrame:
    if "all" in selected:
        return data
    else:
        return data[data[col].isin(selected)].reset_index(drop=True)


@st.cache_data
def df_to_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False)


@st.cache_data
def df_to_excel(df: pd.DataFrame):
    output = BytesIO()
    writer = pd.ExcelWriter(path=output, engine="xlsxwriter")
    df.to_excel(excel_writer=writer, index=False, sheet_name="Sheet1")
    writer.close()
    processed_data = output.getvalue()
    return processed_data


def main():
    st.set_page_config(
        page_title="EBAC | Módulo 19 | Streamlit II | Exercício 2",
        page_icon="https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/Module_19_-_Streamlit2/Practice%201/img/telmarketing_icon.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # TÍTULO
    st.markdown(
        """
    <div style="text-align:center">
        <a href="https://github.com/raafarosa/Ebac_Data_Scientist_General/tree/main/Module%2019%20-%20Streamlit%20II/Practice%201">
            <img src="https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/utilities/newebac_logo_black_half.png" alt="ebac_logo-data_science" width=100%>
        </a>
    </div> 

    ---

    <!-- # **Profissão: Cientista de Dados** -->
    ### **Módulo 19** | Streamlit II | Exercício 2

     **Por:** [Rafael Rosa Alves](https://www.linkedin.com/in/rafael-rosa-alves/)<br>

    ---
    """,
        unsafe_allow_html=True,
    )

    st.write("# Telemarketing analysis")
    st.markdown(body="---")

    # SIDEBAR
    # image = Image.open(fp='Módulo_19_-_Streamlit_II/Exercício_1/img/Bank-Branding.jpg')
    # st.sidebar.image(image=image)
    st.sidebar.markdown(
        body='<img src="https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/Module_19_-_Streamlit2/Practice%201/img/Bank-Branding.jpg" width=100%>',
        unsafe_allow_html=True,
    )

    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader(
        label="Bank marketing data", type=["csv", "xlsx"]
    )

    if data_file_1 is not None:
        start = timeit.default_timer()

        bank_raw = load_data(
            # file_data="https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/Module_19_-_Streamlit2/Practice%201/data/input/bank-additional-full.csv",
            file_data=data_file_1,
            sep=";",
        )
        bank = bank_raw.copy()

        st.write("Time:", timeit.default_timer() - start)

        st.write("## Antes dos filtros")
        st.write(bank_raw)
        st.write("Quantidade de linhas:", bank_raw.shape[0])
        st.write("Quantidade de colunas:", bank_raw.shape[1])

        with st.sidebar.form(key="my_form"):
            # TIPO DE GRÁFICO
            graph_type = st.radio("Tipo de gráfico:", ("Barras", "Pizza"))

            # IDADE
            min_age = min(bank["age"])
            max_age = max(bank["age"])

            idades = st.slider(
                label="Idade:",
                min_value=min_age,
                max_value=max_age,
                value=(min_age, max_age),
                step=1,
            )

            # PROFISSÕES
            jobs_list = bank["job"].unique().tolist()
            jobs_list.append("all")
            jobs_selected = st.multiselect(
                label="Profissões:", options=jobs_list, default=["all"]
                .pipe(multiselect_filter, "contact", contact_selected)
                .pipe(multiselect_filter, "month", month_selected)
                .pipe(multiselect_filter, "day_of_week", day_of_week_selected)
            )

            submit_button = st.form_submit_button(label="Aplicar")

        st.write("## Após os filtros")
        st.write(bank)
        st.write("Quantidade de linhas:", bank.shape[0])
        st.write("Quantidade de colunas:", bank.shape[1])

        col1, col2 = st.columns(spec=2)

        csv = df_to_csv(df=bank)
        col1.write("### Download CSV")
        col1.download_button(
            label="📥 Baixar como arquivo .csv",
            data=csv,
            file_name="df_csv.csv",
            mime="text/csv",
        )

        excel = df_to_excel(df=bank)
        col2.write("### Download Excel")
        col2.download_button(
            label="📥 Baixar como arquivo .xlsx",
            data=excel,
            file_name="df_excel.xlsx",
        )

        st.markdown("---")

        # Coluna 1
        bank_raw_target_pct = (
            bank_raw["y"].value_counts(normalize=True).to_frame() * 100
        )
        bank_raw_target_pct = bank_raw_target_pct.sort_index()
        # Coluna 2
        bank_target_pct = bank["y"].value_counts(normalize=True).to_frame() * 100
        bank_target_pct = bank_target_pct.sort_index()

        # PLOTS
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
        if graph_type == "Barras":
            sns.barplot(
                x=bank_raw_target_pct.index,
                y="proportion",
                data=bank_raw_target_pct,
                ax=axes[0],
            )
            axes[0].bar_label(container=axes[0].containers[0])
            axes[0].set_title(label="Dados brutos", fontweight="bold")
            sns.barplot(
                x=bank_target_pct.index,
                y="proportion",
                data=bank_target_pct,
                ax=axes[1],
            )
            axes[1].bar_label(container=axes[1].containers[0])
            axes[1].set_title(label="Dados filtrados", fontweight="bold")
        else:
            bank_raw_target_pct.plot(
                kind="pie", autopct="%.2f", y="proportion", ax=axes[0]
            )
            axes[0].set_title("Dados brutos", fontweight="bold")
            bank_target_pct.plot(kind="pie", autopct="%.2f", y="proportion", ax=axes[1])
            axes[1].set_title("Dados filtrados", fontweight="bold")
        st.write("## Proporção de aceite")
        st.pyplot(plt)


if __name__ == "__main__":
    main()