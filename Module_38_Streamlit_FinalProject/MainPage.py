
# Imports
import pandas            as pd
import streamlit         as st

from io                     import BytesIO
from pycaret.classification import load_model, predict_model

# Função principal da aplicação
def main():
    # Configuração inicial da página da aplicação
    st.set_page_config(
        page_title="EBAC | Module 38",
        page_icon='https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/utilities/regular_ebac-logo.ico', 
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.markdown('''
                        # **Profissão: Cientista de Dados**
                        ### **Projeto de Agrupamento Hierárquico**

                        **Por:** [Rafael Rosa](https://www.linkedin.com/in/rafael-rosa-alves/)<br>
                        
                        ---
                        ''', unsafe_allow_html=True)

    with st.sidebar.expander(label="Bibliotecas/Pacotes", expanded=False):
        st.code('''
                import pandas            as pd
                import streamlit         as st

                from io                     import BytesIO
                from pycaret.classification import load_model, predict_model
                ''', language='python')

    st.markdown('''
                <div style="text-align:center">
                    <img src="https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/utilities/newebac_logo_black_half.png" alt="ebac_logo-data_science" width="100%">
                </div>

                ---

                <!-- # **Profissão: Cientista de Dados** -->
                ### **Module 38**

                **Por:** [Rafael Rosa](https://www.linkedin.com/in/rafael-rosa-alves/)<br>

                ---
                ''', unsafe_allow_html=True)

@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# Função para converter o df para excel
@st.cache
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


    # Título principal da aplicação
    st.write("""## Escorando o modelo gerado no pycaret """)
    st.markdown("---")
    
    # Botão para carregar arquivo na aplicação
    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank Credit Dataset", type = ['csv','ftr'])

    # Verifica se há conteúdo carregado na aplicação
    if (data_file_1 is not None):
        df_credit = pd.read_feather(data_file_1)
        df_credit = df_credit.sample(50000)

        model_saved = load_model('Best Model Projeto Final 122022')
        predict = predict_model(model_saved, data=df_credit)

        df_xlsx = to_excel(predict)
        st.download_button(label='📥 Download',
                            data=df_xlsx ,
                            file_name= 'predict.xlsx')


if __name__ == '__main__':
	main()









