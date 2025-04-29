from utils.processamento import carregar_imagens, criar_dataframe, salvar_csv

# Caminho da pasta com as imagens organizadas por classe
pasta_imagens = 'data/'

# Extrair os dados
caracteristicas, rotulos = carregar_imagens(pasta_imagens)

# Criar o DataFrame
df = criar_dataframe(caracteristicas, rotulos)

# Salvar como CSV (com o mesmo nome que o do professor, se quiser)
salvar_csv(df, 'personagens.csv')
