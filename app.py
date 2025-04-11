<<<<<<< HEAD
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_modal import Modal

# Ler o arquivo Excel
df = pd.read_excel("TWILIO-MODELO_MENSAGENS.xlsx")

# Criar a barra lateral
st.sidebar.title("Opções")
opcao = st.sidebar.selectbox("Escolha uma opção:", ["Tabela", "Gráfico", "Adicionar Dados"])

# Exibir a tabela ou o gráfico com base na seleção
if opcao == "Tabela":
    st.title("Tabela de Mensagens")
    st.write(df)
elif opcao == "Gráfico":
    st.title("Gráfico de Mensagens")
    fig = px.bar(df, x='nome', y='tempo_em_mins', title='Gráfico de Mensagens')
    st.plotly_chart(fig)
elif opcao == "Adicionar Dados":
    modal = Modal("Adicionar Dados", key="adicionar_dados")
    if st.sidebar.button("Abrir Formulário"):
        modal.open()
    
    if modal.is_open():
        with modal.container():
            st.title("Adicionar Dados")
            nome = st.text_input("Nome")
            tempo_em_mins = st.number_input("Tempo em minutos", min_value=0)
            if st.button("Salvar"):
                # Adicionar os dados à tabela
                new_data = {"nome": nome, "tempo_em_mins": tempo_em_mins}
                df = df.append(new_data, ignore_index=True)
                df.to_excel("TWILIO-MODELO_MENSAGENS.xlsx", index=False)
                st.success("Dados adicionados com sucesso!")
=======
import requests
from flask import Flask, request, render_template, redirect, jsonify, url_for
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Carregar o arquivo Excel
excel_file = 'Projeto_Operacional.xlsx'

# Função para carregar os dados do Excel
def load_data():
    df_posicoes = pd.read_excel(excel_file, sheet_name='Posição de Veiculos', engine='openpyxl')
    df_movimentacoes = pd.read_excel(excel_file, sheet_name='Movimentação', engine='openpyxl')
    df_navios = pd.read_excel(excel_file, sheet_name='Line Up', engine='openpyxl')
    df_chegadas = pd.read_excel(excel_file, sheet_name='Chegadas', engine='openpyxl')
    df_celulas = pd.read_excel(excel_file, sheet_name='Células', engine='openpyxl')
    return df_posicoes, df_movimentacoes, df_navios, df_chegadas, df_celulas

# Função para salvar os dados no Excel
def save_data(df, sheet_name):
    with pd.ExcelWriter(excel_file, mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

# Listar todas as planilhas no arquivo
xls = pd.ExcelFile(excel_file)
print(xls.sheet_names)

@app.route('/')
def index():
    return render_template('login.html', message='')

@app.route('/auth/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Verificar se o usuário e a senha correspondem a alguma entrada no arquivo Excel
    df_movimentacoes = pd.read_excel(excel_file, sheet_name='Movimentação')
    user = df_movimentacoes[(df_movimentacoes['usuario'] == username) & (df_movimentacoes['senha'] == password)]

    if not user.empty:
        return render_template('insert.html') 
    else:
        return render_template('login.html', message='Credenciais inválidas.')

@app.route('/inserir_dados')
def inserir_dados():
    return render_template('insert.html')

@app.route('/inserir_dados/posicoes')
def inserir_dados_posicoes():
    return render_template('insert.html', modal='posicoes')

@app.route('/posicoes', methods=['POST'])
def save_posicoes():
    df_posicoes, _, _, _, _ = load_data()
    posicoes_data = {
        'dataHora': request.form.get('dataHora'),
        'ramal': request.form.get('ramal'),
        'ferrovia': request.form.get('ferrovia'),
        'quantidade': request.form.get('quantidade'),
        'tipo': request.form.get('tipo'),
        'terminal': request.form.get('terminal')
    }
    print("Dados capturados para envio (posições):", posicoes_data)
    # Adicionar os novos dados ao DataFrame
    df_posicoes = pd.concat([df_posicoes, pd.DataFrame([posicoes_data])], ignore_index=True)
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_posicoes, 'Posição de Veiculos')
    return render_template('insert.html', message="Dados de posições salvos com sucesso!", modal='posicoes')

@app.route('/movimentacoes', methods=['POST'])
def save_movimentacoes():
    _, df_movimentacoes, _, _, _ = load_data()
    
    data = {
        'data': request.form.get('data'),
        'produto': request.form.get('produto'),
        'empresa': request.form.get('empresa'),
        'toneladas_vagao': float(request.form.get('toneladas_vagao')),
        'toneladas_caminhao': float(request.form.get('toneladas_caminhao')),
        'quantidade_vagoes': int(request.form.get('quantidade_vagoes')),
        'quantidade_caminhoes': int(request.form.get('quantidade_caminhoes')),
        'tipo': request.form.get('tipo'),
        'terminal': request.form.get('terminal')
    }

    if data['tipo'] == "Saida":
        data['toneladas_vagao'] = -abs(data['toneladas_vagao'])
        data['toneladas_caminhao'] = -abs(data['toneladas_caminhao'])

    print("Dados capturados para envio (movimentações):", data)
    
    # Adicionar os novos dados ao DataFrame
    df_movimentacoes = pd.concat([df_movimentacoes, pd.DataFrame([data])], ignore_index=True)
    
    # Atualizar o valor total no DataFrame de acordo com o produto e a empresa selecionados
    df_movimentacoes['quantidade_total'] = df_movimentacoes.groupby(['produto', 'empresa'])[['toneladas_vagao', 'toneladas_caminhao']].transform('sum').sum(axis=1)
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_movimentacoes, 'Movimentação')
    
    return render_template('insert.html', message="Movimentação salva com sucesso!")


@app.route('/inserir_dados/navios')
def inserir_dados_navios():
    return render_template('insert.html', modal='navios')

@app.route('/navios', methods=['POST'])
def save_navios():
    _, _, df_navios, _, _ = load_data()  # Ajuste para desempacotar cinco valores
    navio_data = {
        'data': request.form.get('data'),
        'nome_navio': request.form.get('nome_navio'),
        'atracacao': request.form.get('atracacao'),
        'inicio': request.form.get('inicio'),
        'talhe': request.form.get('talhe'),
        'saida': request.form.get('saida'),
        'status': request.form.get('status'),
        'vessel': request.form.get('vessel'),
        'qtty': request.form.get('qtty'),
        'comm': request.form.get('comm'),
        'eta': request.form.get('eta'),
        'time': request.form.get('time'),
        'etb': request.form.get('etb'),
        'etc': request.form.get('etc'),
        'charter': request.form.get('charter'),
        'disport': request.form.get('disport'),
        'agency': request.form.get('agency'),
        'op': request.form.get('op'),
        'produto': request.form.get('produto'),
        'plana_de_carga': request.form.get('plana_de_carga'),
        'embarc_periodo_ant': request.form.get('embarc_periodo_ant'),
        'periodo': request.form.get('periodo'),
        'a_bordo': request.form.get('a_bordo'),
        'saldo': request.form.get('saldo')
    }
    print("Dados a serem enviados:", navio_data)
    # Adicionar os novos dados ao DataFrame
    df_navios = pd.concat([df_navios, pd.DataFrame([navio_data])], ignore_index=True)
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_navios, 'Line Up')
    return render_template('insert.html', message="Dados do navio salvos com sucesso!")

@app.route('/chegadas', methods=['GET'])
def fetch_chegadas():
    _, _, _, df_chegadas = load_data()
    # Converter o DataFrame para uma lista de dicionários
    chegadas_data = df_chegadas.to_dict(orient='records')
    return jsonify(chegadas_data)

@app.route('/inserir_dados_chegadas')
def inserir_dados_chegadas():
    return render_template('insert.html', modal='chegadas')

@app.route('/chegadas', methods=['POST'])
def save_chegada():
    _, _, _, df_chegadas, _ = load_data()  
    chegada = {
        'dataHora': request.form.get('dataHora'),
        'quantidade': request.form.get('quantidade'),
        'produto': request.form.get('produto'),
        'ferrovia': request.form.get('ferrovia'),
        'empresa': request.form.get('empresa')
    }
    print("Chegada a ser salva:", chegada)
    # Adicionar os novos dados ao DataFrame usando pd.concat em vez de append
    df_chegadas = pd.concat([df_chegadas, pd.DataFrame([chegada])], ignore_index=True)
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_chegadas, 'Chegadas')
    return render_template('insert.html', message="Chegada salva com sucesso!", modal='chegadas')


@app.route('/inserir_dados_celulas')
def inserir_dados_celulas():
    return render_template('insert.html', modal='celulas')

@app.route('/celulas', methods=['POST'])
def save_celulas():
    _, _, _, _, df_celulas = load_data()
    celula_data = {
        'capacidade': request.form.get('capacidade'),
        'celula': request.form.get('celula'),
        'terminal': request.form.get('terminal'),
        'produto': request.form.get('produto'),
        'entrada': float(request.form.get('entrada')),
        'cutoff_transf': request.form.get('cutoff_transf'),
        'saida': float(request.form.get('saida')),
        'data': request.form.get('data')
    }
    print("Dados da célula a serem salvos:", celula_data)
    
    # Adicionar os novos dados ao DataFrame
    df_celulas = pd.concat([df_celulas, pd.DataFrame([celula_data])], ignore_index=True)
    
    # Ordenar os dados por terminal, célula e data
    df_celulas = df_celulas.sort_values(by=['terminal', 'celula', 'data'])
    
    # Calcular o estoque anterior com base na data anterior
    df_celulas['estoque_anterior'] = df_celulas.groupby(['terminal', 'celula'])['estoque_final'].shift(1).fillna(0)
    
    # Calcular o estoque final com base no estoque anterior, entrada e saída, considerando o mesmo terminal
    df_celulas['estoque_final'] = df_celulas.apply(
        lambda row: row['estoque_anterior'] + row['entrada'] - row['saida'] if row['terminal'] == row['terminal'] else row['estoque_anterior'],
        axis=1
    )
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_celulas, 'Células')
    
    return render_template('insert.html', message="Dados da célula salvos com sucesso!", modal='celulas')
@app.route('/delete_celulas', methods=['POST'])
def delete_celulas():
    _, _, _, _, df_celulas = load_data()
    indices_to_delete = []
    for key in request.form:
        if key.startswith('delete_'):
            index = int(key.split('_')[1])
            indices_to_delete.append(index)
    
    # Ordenar os índices em ordem decrescente para evitar problemas ao remover itens
    indices_to_delete.sort(reverse=True)
    
    for index in indices_to_delete:
        df_celulas.drop(index, inplace=True)
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_celulas, 'Células')
    
    return redirect(url_for('dashboard'))


## Função para criar gráficos
def create_graphs(df):
    # Calcular a quantidade por produto (soma de Toneladas Vagão e Toneladas Caminhão)
    df['quantidade_total'] = df['toneladas_vagao'] + df['toneladas_caminhao']
    quantidade_por_produto = df.groupby('produto')['quantidade_total'].sum().reset_index()

    # Criar o gráfico interativo usando Plotly
    fig_bar = px.bar(quantidade_por_produto, x='produto', y='quantidade_total', title='Quantidade por Produto', labels={'quantidade_total': 'Quantidade Total (Toneladas)'})
    fig_bar.update_traces(marker=dict(color='rgba(100, 149, 237, 0.6)'), texttemplate='%{y}', textposition='outside')  # Cor azul clara
    fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=True,
                          font=dict(color='black'), title_font=dict(color='white'), legend_title_font=dict(color='black'))
    graph_bar_html = pio.to_html(fig_bar, full_html=False)

    # Calcular a quantidade de vagões e caminhões
    quantidade_vagoes = df['quantidade_vagoes'].sum()
    quantidade_caminhoes = df['quantidade_caminhoes'].sum()

    # Calcular o total por empresa e produto
    total_por_empresa_produto = df.groupby(['empresa', 'produto'])['quantidade_total'].sum().reset_index()

    # Criar o gráfico de barras horizontais usando Plotly no lugar do gráfico de pizza
    fig_horizontal_bar = px.bar(total_por_empresa_produto, x='quantidade_total', y='empresa', color='produto', orientation='h', title='Total por Empresa e Produto', labels={'quantidade_total': 'Quantidade Total (Toneladas)'})
    fig_horizontal_bar.update_traces(marker=dict(line=dict(color='rgba(100, 149, 237, 0.6)')), texttemplate='%{x}', textposition='outside')  # Cor azul clara
    fig_horizontal_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=True,
                                     font=dict(color='black'), title_font=dict(color='black'), legend_title_font=dict(color='black'))
    graph_horizontal_bar_html = pio.to_html(fig_horizontal_bar, full_html=False)

    return graph_bar_html, graph_horizontal_bar_html


# Função para criar gráficos de barras horizontais para células
def create_celula_graphs(df):
    fig_celulas = px.bar(df.copy(), x='estoque_final', y='celula', color='produto', orientation='h', title='Estoque Final por Célula e Produto', labels={'estoque_final': 'Estoque Final (Unidades)'})
    fig_celulas.update_traces(marker=dict(line=dict(color='rgba(100, 149, 237, 0.6)')), texttemplate='%{x}', textposition='outside')  # Cor azul clara
    fig_celulas.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    graph_celulas_html = pio.to_html(fig_celulas, full_html=False)
    
    return graph_celulas_html


@app.route('/dashboard')
def dashboard():
    df_posicoes, df_movimentacoes, df_navios, df_chegadas, df_celulas = load_data()
    
    # Verificar se a coluna 'terminal' existe no DataFrame de movimentações e células
    if 'terminal' not in df_movimentacoes.columns or 'terminal' not in df_celulas.columns:
        return "Coluna 'terminal' não encontrada no arquivo Excel.", 400
    
    # Separar os dados por terminal (TEAG e TEG)
    df_teag = df_movimentacoes.loc[df_movimentacoes['terminal'] == 'teag']
    df_teg = df_movimentacoes.loc[df_movimentacoes['terminal'] == 'teg']
    
    # Criar gráficos para TEAG
    graph_bar_teag_html, graph_horizontal_bar_teag_html = create_graphs(df_teag)
    
    # Criar gráficos para TEG
    graph_bar_teg_html, graph_horizontal_bar_horizontal_bar_teg_html = create_graphs(df_teg)
    
    # Criar gráficos de barras horizontais para células TEAG e TEG
    graph_celulas_teag_html = create_celula_graphs(df_celulas.loc[df_celulas['terminal'] == 'teag'])
    graph_celulas_teg_html = create_celula_graphs(df_celulas.loc[df_celulas['terminal'] == 'teg'])
    
    # Filtrar informações da planilha Line Up para TEAG e TEG
    df_navios_teag = df_navios[df_navios['op'] == 'TEAG']
    df_navios_teg = df_navios[df_navios['op'] == 'TEG']

    # Converter dados para dicionários
    navios_teag_data = df_navios_teag.to_dict(orient='records')
    navios_teg_data = df_navios_teg.to_dict(orient='records')

    # Renderizar o HTML com os gráficos, cards e informações dos navios
    return render_template('dashboard.html', 
                           quantidade_vagoes_teag=df_teag['quantidade_vagoes'].sum(), 
                           quantidade_caminhoes_teag=df_teag['quantidade_caminhoes'].sum(),
                           graph_bar_teag_html=graph_bar_teag_html,
                           graph_horizontal_bar_teag_html=graph_horizontal_bar_teag_html,
                           quantidade_vagoes_teg=df_teg['quantidade_vagoes'].sum(), 
                           quantidade_caminhoes_teg=df_teg['quantidade_caminhoes'].sum(),
                           graph_bar_teg_html=graph_bar_teg_html,
                           graph_horizontal_bar_teg_html=graph_horizontal_bar_horizontal_bar_teg_html,
                           graph_celulas_teag_html=graph_celulas_teag_html,
                           graph_celulas_teg_html=graph_celulas_teg_html,
                           navios_teag_data=navios_teag_data,
                           navios_teg_data=navios_teg_data)

@app.route('/dashboard_posicoes')
def dashboard_posicoes():
    df_posicoes, _, _, _, _ = load_data()
    posicoes_data = df_posicoes.to_dict(orient='records')
    return render_template('dashboard_posicoes.html', posicoes=posicoes_data)

@app.route('/edit_posicoes')
def edit_posicoes():
    df_posicoes, _, _, _, _ = load_data()
    posicoes_data = df_posicoes.to_dict(orient='records')
    return render_template('dashboard_posicoes.html', posicoes=posicoes_data, editable=True)

@app.route('/update_posicoes', methods=['POST'])
def update_posicoes():
    df_posicoes, _, _, _, _ = load_data()
    
    # Atualizar os dados no DataFrame
    for index in range(len(df_posicoes)):
        df_posicoes.at[index, 'dataHora'] = request.form.get(f'dataHora_{index}')
        df_posicoes.at[index, 'ramal'] = request.form.get(f'ramal_{index}')
        df_posicoes.at[index, 'ferrovia'] = request.form.get(f'ferrovia_{index}')
        df_posicoes.at[index, 'quantidade'] = request.form.get(f'quantidade_{index}')
        df_posicoes.at[index, 'tipo'] = request.form.get(f'tipo_{index}')
        df_posicoes.at[index, 'terminal'] = request.form.get(f'terminal_{index}')
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_posicoes, 'Posição de Veiculos')

    return redirect(url_for('dashboard_posicoes'))

@app.route('/dashboard_movimentacoes')
def dashboard_movimentacoes():
    _, df_movimentacoes, _, _, _ = load_data()
    movimentacoes_data = df_movimentacoes.to_dict(orient='records')
    return render_template('dashboard_movimentacoes.html', movimentacoes=movimentacoes_data)

@app.route('/edit_movimentacoes')
def edit_movimentacoes():
    _, df_movimentacoes, _, _, _ = load_data()
    movimentacoes_data = df_movimentacoes.to_dict(orient='records')
    return render_template('dashboard_movimentacoes.html', movimentacoes=movimentacoes_data, editable=True)

@app.route('/update_movimentacoes', methods=['POST'])
def update_movimentacoes():
    _, df_movimentacoes, _, _, _ = load_data()
    
    # Atualizar os dados no DataFrame
    for index in range(len(df_movimentacoes)):
        df_movimentacoes.at[index, 'data'] = request.form.get(f'data_{index}')
        df_movimentacoes.at[index, 'produto'] = request.form.get(f'produto_{index}')
        df_movimentacoes.at[index, 'empresa'] = request.form.get(f'empresa_{index}')
        df_movimentacoes.at[index, 'toneladas_vagao'] = request.form.get(f'toneladas_vagao_{index}')
        df_movimentacoes.at[index, 'toneladas_caminhao'] = request.form.get(f'toneladas_caminhao_{index}')
        df_movimentacoes.at[index, 'quantidade_vagoes'] = request.form.get(f'quantidade_vagoes_{index}')
        df_movimentacoes.at[index, 'quantidade_caminhoes'] = request.form.get(f'quantidade_caminhoes_{index}')
        df_movimentacoes.at[index, 'tipo'] = request.form.get(f'tipo_{index}')
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_movimentacoes, 'Movimentação')

    return redirect(url_for('dashboard_movimentacoes'))
@app.route('/delete_movimentacoes', methods=['POST'])
def delete_movimentacoes():
    _, df_movimentacoes, _, _, _ = load_data()
    indices_to_delete = []
    for key in request.form:
        if key.startswith('delete_'):
            index = int(key.split('_')[1])
            indices_to_delete.append(index)
    
    # Ordenar os índices em ordem decrescente para evitar problemas ao remover itens
    indices_to_delete.sort(reverse=True)
    
    for index in indices_to_delete:
        df_movimentacoes.drop(index, inplace=True)
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_movimentacoes, 'Movimentação')
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard_navios')
def dashboard_navios():
    _, _, df_navios, _, _ = load_data()  # Ajuste para desempacotar cinco valores
    navios_data = df_navios.to_dict(orient='records')

    # Consultar a API de clima para a previsão do tempo
    weather_forecast = {
        "temperature": "N/A",
        "condition": "N/A",
        "humidity": "N/A",
        "wind": "N/A"
    }
    forecast = []
    city = "são paulo"
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levantar exceção para códigos de status HTTP ruins
        weather_data = response.json()

        # Extrair as informações úteis sobre o clima atual
        current_condition = weather_data["current_condition"][0]
        weather_forecast = {
            "temperature": current_condition.get("temp_C", "N/A"),
            "condition": current_condition["weatherDesc"][0].get("value", "N/A"),
            "humidity": current_condition.get("humidity", "N/A"),
            "wind": current_condition.get("windspeedKmph", "N/A")
        }

        # Previsões para os próximos dias
        forecast_days = weather_data.get("weather", [])
        for day in forecast_days:
            day_forecast = {
                "date": day.get("date", "N/A"),
                "temperature_max": day.get("tempMaxC", "N/A"),
                "temperature_min": day.get("tempMinC", "N/A"),
                "condition": day["hourly"][0]["weatherDesc"][0].get("value", "N/A")
            }
            forecast.append(day_forecast)

    except (requests.RequestException, KeyError, IndexError) as e:
        # Registro de erro opcional
        print(f"Erro ao consultar a API de clima: {e}")

    return render_template('dashboard_navios.html', 
                           navios=navios_data, 
                           editable=False,
                           weather_forecast=weather_forecast,
                           forecast=forecast)


@app.route('/edit_navios')
def edit_navios():
    # Carregar os dados dos navios
    _, _, df_navios, _, _ = load_data()
    navios_data = df_navios.to_dict(orient='records')

    # Inicializar a previsão do tempo padrão
    weather_forecast = {
        "temperature": "N/A",
        "condition": "N/A",
        "humidity": "N/A",
        "wind": "N/A"
    }
    forecast = []

    # Consultar a API de clima para a previsão do tempo
    city = "são paulo"
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levantar exceção para códigos de status HTTP ruins
        weather_data = response.json()

        # Extrair as informações úteis sobre o clima atual
        current_condition = weather_data["current_condition"][0]
        weather_forecast = {
            "temperature": current_condition.get("temp_C", "N/A"),
            "condition": current_condition["weatherDesc"][0].get("value", "N/A"),
            "humidity": current_condition.get("humidity", "N/A"),
            "wind": current_condition.get("windspeedKmph", "N/A")
        }

        # Previsões para os próximos dias
        forecast_days = weather_data.get("weather", [])
        for day in forecast_days:
            day_forecast = {
                "date": day.get("date", "N/A"),
                "temperature_max": day.get("tempMaxC", "N/A"),
                "temperature_min": day.get("tempMinC", "N/A"),
                "condition": day["hourly"][0]["weatherDesc"][0].get("value", "N/A")
            }
            forecast.append(day_forecast)

    except (requests.RequestException, KeyError, IndexError) as e:
        # Registro de erro opcional
        print(f"Erro ao consultar a API de clima: {e}")

    # Impressão de debug
    print("navios_data:", navios_data)
    print("weather_forecast:", weather_forecast)
    print("forecast:", forecast)

    return render_template('dashboard_navios.html', 
                           navios=navios_data, 
                           editable=True, 
                           weather_forecast=weather_forecast,
                           forecast=forecast)




@app.route('/delete_navios', methods=['POST'])
def delete_navios():
    _, _, df_navios, _, _ = load_data()
    indices_to_delete = []
    for key in request.form:
        if key.startswith('delete_'):
            index = int(key.split('_')[1])
            indices_to_delete.append(index)
    
    # Ordenar os índices em ordem decrescente para evitar problemas ao remover itens
    indices_to_delete.sort(reverse=True)
    
    for index in indices_to_delete:
        df_navios.drop(index, inplace=True)
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_navios, 'Line Up')
    
    return redirect(url_for('dashboard'))

@app.route('/update_navios', methods=['POST'])
def update_navios():
    _, _, df_navios, _, _ = load_data()
    
    # Atualizar os dados no DataFrame
    for index in range(len(df_navios)):
        df_navios.at[index, 'data'] = request.form.get(f'data_{index}')
        df_navios.at[index, 'nome_navio'] = request.form.get(f'nome_navio_{index}')
        df_navios.at[index, 'atracacao'] = request.form.get(f'atracacao_{index}')
        df_navios.at[index, 'inicio'] = request.form.get(f'inicio_{index}')
        df_navios.at[index, 'talhe'] = request.form.get(f'talhe_{index}')
        df_navios.at[index, 'saida'] = request.form.get(f'saida_{index}')
        df_navios.at[index, 'status'] = request.form.get(f'status_{index}')
        df_navios.at[index, 'vessel'] = request.form.get(f'vessel_{index}')
        df_navios.at[index, 'qtty'] = request.form.get(f'qtty_{index}')
        df_navios.at[index, 'comm'] = request.form.get(f'comm_{index}')
        df_navios.at[index, 'eta'] = request.form.get(f'eta_{index}')
        df_navios.at[index, 'time'] = request.form.get(f'time_{index}')
        df_navios.at[index, 'etb'] = request.form.get(f'etb_{index}')
        df_navios.at[index, 'etc'] = request.form.get(f'etc_{index}')
        df_navios.at[index, 'charter'] = request.form.get(f'charter_{index}')
        df_navios.at[index, 'disport'] = request.form.get(f'disport_{index}')
        df_navios.at[index, 'agency'] = request.form.get(f'agency_{index}')
        df_navios.at[index, 'op'] = request.form.get(f'op_{index}')
        df_navios.at[index, 'produto'] = request.form.get(f'produto_{index}')
        df_navios.at[index, 'plana_de_carga'] = request.form.get(f'plana_de_carga_{index}')
        df_navios.at[index, 'embarc_periodo_ant'] = request.form.get(f'embarc_periodo_ant_{index}')
        df_navios.at[index, 'periodo'] = request.form.get(f'periodo_{index}')
        df_navios.at[index, 'a_bordo'] = request.form.get(f'a_bordo_{index}')
        df_navios.at[index, 'saldo'] = request.form.get(f'saldo_{index}')
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_navios, 'Line Up')

    return redirect(url_for('dashboard_navios'))
@app.route('/dashboard_celulas')
def dashboard_celulas():
    _, _, _, _, df_celulas = load_data()
    celulas_data = df_celulas.to_dict(orient='records')
    
    # Manter a capacidade da primeira linha de cada célula
    df_celulas = df_celulas.sort_values('data').groupby('celula').first().reset_index()

    # Remover a vírgula e converter para float na coluna 'capacidade'
    df_celulas['capacidade'] = df_celulas['capacidade'].astype(str).str.replace(',', '').astype(float)

    # Calcular a porcentagem usada da capacidade
    df_celulas['percentual_usado'] = (df_celulas['estoque_final'] / df_celulas['capacidade']) * 100

    # Calcular a porcentagem de espaço disponível
    df_celulas['percentual_disponivel'] = 100 - df_celulas['percentual_usado']

    # Criar gráfico com Plotly, adicionando rótulos de texto
    fig = px.bar(df_celulas, x='celula', y='percentual_usado', title='Porcentagem Usada da Capacidade por Célula', 
                 labels={'percentual_usado':'Porcentagem Usada (%)', 'celula':'Célula'}, text='percentual_usado',
                 opacity=0.7, color_discrete_sequence=px.colors.qualitative.Pastel)

    # Atualizar os rótulos de texto para exibir a capacidade e a porcentagem de espaço disponível
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    for i, row in df_celulas.iterrows():
        fig.add_annotation(
            x=row['celula'],
            y=row['percentual_usado'],
            text=f"Capacidade: {row['capacidade']}<br>Disponível: {row['percentual_disponivel']:.2f}%",
            showarrow=False,
            yshift=-30  # Ajustar a posição do texto
        )
    
    # Salvar o gráfico como HTML
    pio.write_html(fig, file='static/plotly_graph.html', auto_open=False)

    return render_template('dashboard_celulas.html', celulas=celulas_data)


@app.route('/edit_celulas')
def edit_celulas():
    _, _, _, _, df_celulas = load_data()
    
    # Ordenar os dados por terminal, célula e data
    df_celulas = df_celulas.sort_values(by=['terminal', 'celula', 'data'])
    
    # Calcular o estoque anterior com base na data anterior
    df_celulas['estoque_anterior'] = df_celulas.groupby(['terminal', 'celula'])['estoque_final'].shift(1).fillna(0)
    
    # Calcular o estoque final com base no estoque anterior, entrada e saída
    df_celulas['estoque_final'] = df_celulas.apply(
        lambda row: row['estoque_anterior'] + row['entrada'] - row['saida'] if row['estoque_anterior'] != 0 else row['entrada'] - row['saida'],
        axis=1
    )

    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_celulas, 'Células')
    
    celulas_data = df_celulas.to_dict(orient='records')
    
    return render_template('dashboard_celulas.html', celulas=celulas_data, editable=True)


@app.route('/update_celulas', methods=['POST'])
def update_celulas():
    _, _, _, _, df_celulas = load_data()
    
    # Atualizar os dados no DataFrame
    for index in range(len(df_celulas)):
        df_celulas.at[index, 'data'] = request.form.get(f'data_{index}')
        df_celulas.at[index, 'capacidade'] = request.form.get(f'capacidade_{index}')
        df_celulas.at[index, 'celula'] = request.form.get(f'celula_{index}')
        df_celulas.at[index, 'terminal'] = request.form.get(f'terminal_{index}')
        df_celulas.at[index, 'produto'] = request.form.get(f'produto_{index}')
        df_celulas.at[index, 'estoque_anterior'] = request.form.get(f'estoque_anterior_{index}')
        df_celulas.at[index, 'entrada'] = request.form.get(f'entrada_{index}')
        df_celulas.at[index, 'cutoff_transf'] = request.form.get(f'cutoff_transf_{index}')
        df_celulas.at[index, 'saida'] = request.form.get(f'saida_{index}')
        df_celulas.at[index, 'estoque_final'] = request.form.get(f'estoque_final_{index}')
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_celulas, 'Células')

    return redirect(url_for('dashboard_celulas'))

@app.route('/dashboard_chegadas')
def dashboard_chegadas():
    _, _, _, df_chegadas, _ = load_data()
    chegadas_data = df_chegadas.to_dict(orient='records')
    return render_template('dashboard_chegadas.html', chegadas=chegadas_data, editable=False)

@app.route('/edit_chegadas')
def edit_chegadas():
    _, _, _, df_chegadas, _ = load_data()
    chegadas_data = df_chegadas.to_dict(orient='records')
    return render_template('dashboard_chegadas.html', chegadas=chegadas_data, editable=True)

@app.route('/update_chegadas', methods=['POST'])
def update_chegadas():
    _, _, _, df_chegadas, _ = load_data()
    
    # Atualizar os dados no DataFrame
    for index in range(len(df_chegadas)):
        df_chegadas.at[index, 'dataHora'] = request.form.get(f'dataHora_{index}')
        df_chegadas.at[index, 'quantidade'] = request.form.get(f'quantidade_{index}')
        df_chegadas.at[index, 'produto'] = request.form.get(f'produto_{index}')
        df_chegadas.at[index, 'ferrovia'] = request.form.get(f'ferrovia_{index}')
        df_chegadas.at[index, 'empresa'] = request.form.get(f'empresa_{index}')
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_chegadas, 'Chegadas')

    return redirect(url_for('dashboard_chegadas'))
@app.route('/delete_chegadas', methods=['POST'])
def delete_chegadas():
    _, _, _, df_chegadas, _ = load_data()
    indices_to_delete = []
    for key in request.form:
        if key.startswith('delete_'):
            index = int(key.split('_')[1])
            indices_to_delete.append(index)
    
    # Ordenar os índices em ordem decrescente para evitar problemas ao remover itens
    indices_to_delete.sort(reverse=True)
    
    for index in indices_to_delete:
        df_chegadas.drop(index, inplace=True)
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_chegadas, 'Chegadas')
    
    return redirect(url_for('dashboard'))

@app.route('/update_posicao/<int:index>', methods=['POST'])
def update_posicao(index):
    df_posicoes, _, _, _, _ = load_data()
    
    # Atualizar os dados no DataFrame
    df_posicoes.at[index, 'dataHora'] = request.form.get('dataHora')
    df_posicoes.at[index, 'ramal'] = request.form.get('ramal')
    df_posicoes.at[index, 'ferrovia'] = request.form.get('ferrovia')
    df_posicoes.at[index, 'quantidade'] = request.form.get('quantidade')
    df_posicoes.at[index, 'tipo'] = request.form.get('tipo')
    df_posicoes.at[index, 'terminal'] = request.form.get('terminal')
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_posicoes, 'Posição de Veiculos')
    
    return render_template('insert.html', message="Dados de posições atualizados com sucesso!", modal='posicoes')  
@app.route('/delete_posicoes', methods=['POST'])
def delete_posicoes():
    df_posicoes, _, _, _, _ = load_data()
    indices_to_delete = []
    for key in request.form:
        if key.startswith('delete_'):
            index = int(key.split('_')[1])
            indices_to_delete.append(index)
    
    # Ordenar os índices em ordem decrescente para evitar problemas ao remover itens
    indices_to_delete.sort(reverse=True)
    
    for index in indices_to_delete:
        df_posicoes.drop(index, inplace=True)
    
    # Salvar o DataFrame atualizado no arquivo Excel
    save_data(df_posicoes, 'Posição de Veiculos')
    
    return redirect(url_for('dashboard'))
@app.route('/conferente_fiscal')
def conferente_fiscal():
    return render_template('conferente_fiscal.html')

@app.route('/confiabilidade')
def confiabilidade():
    return render_template('confiabilidade.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
>>>>>>> b8691f88 (atualização)
