# Cadastro de Alunos para a Escola Técnica de Saúde da UFPB
Pablo Gomes de Miranda

Aplicativo em Python desenvolvido com metodologia RAD produzido para a disciplina "Desenvolvimento Rápido de Aplicações em Python" como forma de obter nota na disciplina já citada para a graduação de Ciência de Dados da Estácio de Sá.

## Descrição 
1. O projeto contém os seguintes componentes: app.py com a interface gráfica, backend.py que faz a conexão da interface gráfica com o banco de dados, docker-compose.yml que levanta um banco de dados Postgres para ser usado na fase de prototipagem, além de elementos comuns em projetos Python.

2. O docker-compose.yml roda um contêiner com um banco de dados em Postgres, depois da fase de prototipagem, as credenciais podem ser trocadas diretamente em um arquivo env ou no backend.py.

3. O aplicativo realiza operações de CRUD, com a finalidade de realizar o cadastro de alunos da Escola Técnica de Saúde da UFPB para cadastrar alunos interessados em realizar uma especialização. Os registros podem ser exportados em .xlsx ou .csv para relatórios posteriores.