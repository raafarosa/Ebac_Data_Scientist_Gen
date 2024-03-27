# Imports
import pandas as pd
import streamlit as st
import xlsxwriter
from io import BytesIO
from pycaret.classification import load_model, predict_model

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# Função para converter o df para excel
@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# Função principal da aplicação
def main():
    # Configuração inicial da página da aplicação
    st.set_page_config(
        page_title="Final Project",
        page_icon='https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/utilities/regular_ebac-logo.ico', 
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # TÍTULO
    st.markdown(
        """
    <div style="text-align:center">
        <a href="https://github.com/raafarosa/Ebac_Data_Scientist_General">
            <img src="https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/utilities/newebac_logo_black_half.png" alt="ebac_logo-data_science" width=100%>
        </a>
    </div> 

    ---

    <!-- # **Profissão: Cientista de Dados** -->
    # **Projeto final**

    **Aluno:** [Rafael Rosa](https://www.linkedin.com/in/rafael-rosa-alves/)<br>

    ---
    """,
        unsafe_allow_html=True,
    )
    
    # Apresenta a imagem na barra lateral da aplicação
    st.sidebar.image('https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/utilities/newebac_logo_black_half.png')

    #Bibliotecas
    with st.sidebar.expander(label="Bibliotecas/Pacotes", expanded=False):
        st.code('''
                import pandas as pd
                import streamlit as st
                from io import BytesIO
                from pycaret.classification import load_model, predict_model
                ''', language='python')

    # Botão para carregar arquivo na aplicação
    st.sidebar.write("#### Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank Credit Dataset", type=['csv', 'ftr'])

    # Descrição
    st.markdown('# Geração de dados convertidos do pycaret em excel')

    # Verifica se há conteúdo carregado na aplicação
    if (data_file_1 is not None):
        df_credit = pd.read_feather(data_file_1)
        df_credit = df_credit.sample(50000)

        model_saved = load_model('model_march_2024')
        predict = predict_model(model_saved, data=df_credit)

        df_xlsx = to_excel(predict)
        st.download_button(label='📥 Download',
                           data=df_xlsx,
                           file_name='data.xlsx')


if __name__ == '__main__':
    main()