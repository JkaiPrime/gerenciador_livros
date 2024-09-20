
# Gerenciado de Livros

Este código implementa um sistema completo de gerenciamento de livraria utilizando o banco de dados SQLite para armazenar informações sobre os livros e manipulação de arquivos para exportar, importar e fazer backup dos dados. Ele inclui funcionalidades de CRUD (Criar, Ler, Atualizar e Deletar), permitindo que o usuário adicione livros, visualize todos os registros, atualize preços e remova livros do banco de dados.

Além disso, o sistema suporta a exportação de dados em formato CSV, a importação de informações de livros a partir de arquivos CSV, e a criação automática de backups antes de cada modificação significativa no banco de dados. O código também organiza os backups, mantendo apenas os 5 mais recentes e excluindo os mais antigos. A interface é simples, com um menu interativo que guia o usuário pelas diferentes funcionalidades do sistema.



## Authors

- [@Jkai](https://github.com/JkaiPrime)
- [@Renato](https://github.com/Renatoleall)


## Deployment

To deploy this project run

Windows
```bash
  python main.py
```

Linux
```bash
  python3 main.py
```
