# Imports
import pandas            as pd
import streamlit         as st
import numpy             as np

from datetime            import datetime
from PIL                 import Image
from io                  import BytesIO

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# Função para converter o df para excel
@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data


### Criando os segmentos
def recencia_class(x, r, q_dict):
    """Classifica como melhor o menor quartil 
       x = valor da linha,
       r = recencia,
       q_dict = quartil dicionario   
    """
    if x <= q_dict[r][0.25]:
        return 'A'
    elif x <= q_dict[r][0.50]:
        return 'B'
    elif x <= q_dict[r][0.75]:
        return 'C'
    else:
        return 'D'

def freq_val_class(x, fv, q_dict):
    """Classifica como melhor o maior quartil 
       x = valor da linha,
       fv = frequencia ou valor,
       q_dict = quartil dicionario   
    """
    if x <= q_dict[fv][0.25]:
        return 'D'
    elif x <= q_dict[fv][0.50]:
        return 'C'
    elif x <= q_dict[fv][0.75]:
        return 'B'
    else:
        return 'A'

# Função principal da aplicação
def main():
    # Configuração inicial da página da aplicação
    st.set_page_config(
        page_title="EBAC | Módulo 31 | Streamlit 5 | Practice 1",
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
    ### **Módulo 31** | Streamlit 5 | Practice 1

    **Aluno:** [Rafael Rosa](https://www.linkedin.com/in/rafael-rosa-alves/)<br>

    ---
    """,
        unsafe_allow_html=True,
    )

    # Título principal da aplicação
    st.write("""# RFV

RFV, abreviação de recência, frequência e valor, é uma técnica empregada na segmentação de clientes com base em seus padrões de compra, agrupando-os em clusters similares. Este método de agrupamento possibilita a implementação de ações de marketing e CRM mais direcionadas, contribuindo para a personalização do conteúdo e aprimorando a retenção de clientes.

Para cada cliente, é essencial calcular as seguintes métricas:

- Recência (R): Representa o intervalo de tempo decorrido desde a última compra realizada.
- Frequência (F): Indica o número total de compras efetuadas durante o período analisado.
- Valor (V): Refere-se ao montante total gasto em compras ao longo do período.

A seguir, será realizado o cálculo dessas métricas para cada cliente.
    """)
    st.markdown("---")
    
    # Apresenta a imagem na barra lateral da aplicação
    st.sidebar.image('https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/utilities/newebac_logo_black_half.png')

    # Botão para carregar arquivo na aplicação
    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank marketing data", type = ['csv','xlsx'])

    if data_file_1 is None:
        if st.sidebar.button('Carregar Arquivo Demonstrativo', 
                            help='./input/dados.csv', 
                            use_container_width=True, 
                            key='uploadDemoButton', 
                            disabled=st.session_state.get('uploadDemoButton', False)):
            data_file_1 = './input/dados.csv'
            st.sidebar.button('Limpar e Reiniciar', use_container_width=True)


    # Verifica se há conteúdo carregado na aplicação
    if (data_file_1 is not None):
        df_compras = pd.read_csv(data_file_1, infer_datetime_format=True, parse_dates=['DiaCompra'])

        st.write('## Recência (R)')

        
        dia_atual = df_compras['DiaCompra'].max()
        st.write('Dia máximo na base de dados: ', dia_atual)

        st.write('Quantos dias faz que o cliente fez a sua última compra?')

        df_recencia = df_compras.groupby(by='ID_cliente', as_index=False)['DiaCompra'].max()
        df_recencia.columns = ['ID_cliente','DiaUltimaCompra']
        df_recencia['Recencia'] = df_recencia['DiaUltimaCompra'].apply(lambda x: (dia_atual - x).days)
        st.write(df_recencia.head())

        df_recencia.drop('DiaUltimaCompra', axis=1, inplace=True)

        st.write('## Frequência (F)')
        st.write('Quantas vezes cada cliente comprou com a gente?')
        df_frequencia = df_compras[['ID_cliente','CodigoCompra']].groupby('ID_cliente').count().reset_index()
        df_frequencia.columns = ['ID_cliente','Frequencia']
        st.write(df_frequencia.head())

        st.write('## Valor (V)')
        st.write('Quanto que cada cliente gastou no periodo?')
        df_valor = df_compras[['ID_cliente','ValorTotal']].groupby('ID_cliente').sum().reset_index()
        df_valor.columns = ['ID_cliente','Valor']
        st.write(df_valor.head())
        

        st.write('## Tabela RFV final')
        df_RF = df_recencia.merge(df_frequencia, on='ID_cliente')
        df_RFV = df_RF.merge(df_valor, on='ID_cliente')
        df_RFV.set_index('ID_cliente', inplace=True)
        st.write(df_RFV.head())

        st.write('## Segmentação utilizando o RFV')
        st.write("Uma abordagem para segmentar os clientes envolve a criação de quartis para cada componente do RFV, onde o quartil mais alto é designado como 'A', o segundo melhor quartil como 'B', o terceiro melhor como 'C' e o pior quartil como 'D'. A classificação de melhor e pior depende da natureza da componente. Por exemplo, para a recência, quanto menor o intervalo desde a última compra, melhor é o cliente (pois comprou recentemente), portanto, o quartil mais baixo seria rotulado como 'A'. Já para a frequência, a lógica é invertida; ou seja, quanto maior a frequência de compras do cliente, melhor ele é considerado, então, o quartil mais alto recebe a designação 'A'.")
        st.write('Se a gente tiver interessado em mais ou menos classes, basta a gente aumentar ou diminuir o número de quantils pra cada componente.')

        st.write('Quartis para o RFV')
        quartis = df_RFV.quantile(q=[0.25,0.5,0.75])
        st.write(quartis)

        st.write('Tabela após a criação dos grupos')
        df_RFV['R_quartil'] = df_RFV['Recencia'].apply(recencia_class,
                                                        args=('Recencia', quartis))
        df_RFV['F_quartil'] = df_RFV['Frequencia'].apply(freq_val_class,
                                                        args=('Frequencia', quartis))
        df_RFV['V_quartil'] = df_RFV['Valor'].apply(freq_val_class,
                                                    args=('Valor', quartis))
        df_RFV['RFV_Score'] = (df_RFV.R_quartil 
                            + df_RFV.F_quartil 
                            + df_RFV.V_quartil)
        st.write(df_RFV.head())

        st.write('Quantidade de clientes por grupos')
        st.write(df_RFV['RFV_Score'].value_counts())

        st.write('#### Clientes com menor recência, maior frequência e maior valor gasto')
        st.write(df_RFV[df_RFV['RFV_Score']=='AAA'].sort_values('Valor', ascending=False).head(10))

        st.write('### Ações de marketing/CRM')

        dict_acoes = {'AAA': 'Enviar cupons de desconto, Pedir para indicar nosso produto pra algum amigo, Ao lançar um novo produto enviar amostras grátis pra esses.',
        'DDD': 'Churn! clientes que gastaram bem pouco e fizeram poucas compras, fazer nada',
        'DAA': 'Churn! clientes que gastaram bastante e fizeram muitas compras, enviar cupons de desconto para tentar recuperar',
        'CAA': 'Churn! clientes que gastaram bastante e fizeram muitas compras, enviar cupons de desconto para tentar recuperar'
        }

        df_RFV['acoes de marketing/crm'] = df_RFV['RFV_Score'].map(dict_acoes)
        st.write(df_RFV.head())


        # df_RFV.to_excel('./auxiliar/output/RFV_.xlsx')
        df_xlsx = to_excel(df_RFV)
        st.download_button(label='📥 Download',
                           data=df_xlsx,
                           file_name= 'RFV_.xlsx')

        st.write('Quantidade de clientes por tipo de ação')
        st.write(df_RFV['acoes de marketing/crm'].value_counts(dropna=False))

if __name__ == '__main__':
	main()
    