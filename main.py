import sqlite3
import csv
import os
from pathlib import Path
import shutil
from datetime import datetime

# Configurações
DB_NAME = 'livraria.db'
BACKUP_DIR = Path('backups')
CSV_DIR = Path('csv_exports')

# Criação do banco de dados
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao INTEGER NOT NULL,
        preco REAL NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Função para fazer backup do banco de dados
def backup_db():
    if not BACKUP_DIR.exists():
        os.makedirs(BACKUP_DIR)
    backup_file = BACKUP_DIR / f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
    shutil.copy(DB_NAME, backup_file)
    clean_old_backups()

def clean_old_backups():
    backups = sorted(BACKUP_DIR.glob('backup_*.db'), key=os.path.getmtime)
    while len(backups) > 5:
        os.remove(backups.pop(0))

# CRUD Operations
def add_book(titulo, autor, ano_publicacao, preco):
    backup_db()  # Faz backup antes de modificar
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livros (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)',
                   (titulo, autor, ano_publicacao, preco))
    conn.commit()
    conn.close()

def display_books():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros')
    for row in cursor.fetchall():
        print(row)
    conn.close()

def update_book_price(book_id, new_price):
    backup_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE livros SET preco = ? WHERE id = ?', (new_price, book_id))
    conn.commit()
    conn.close()

def remove_book(book_id):
    backup_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livros WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

def search_books_by_author(author):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros WHERE autor = ?', (author,))
    for row in cursor.fetchall():
        print(row)
    conn.close()

# Exportar e importar CSV
def export_to_csv(filename='livros.csv'):
    if not CSV_DIR.exists():
        os.makedirs(CSV_DIR)
    with open(CSV_DIR / filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM livros')
        writer.writerow(['ID', 'Título', 'Autor', 'Ano de Publicação', 'Preço'])
        writer.writerows(cursor.fetchall())
        conn.close()

def import_from_csv(filename):
    backup_db()
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Pular o cabeçalho
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        for row in reader:
            cursor.execute('INSERT INTO livros (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)',
                           (row[1], row[2], int(row[3]), float(row[4])))
        conn.commit()
        conn.close()

# Menu do sistema
def menu():
    init_db()
    while True:
        print("\nMenu:")
        print("1. Adicionar novo livro")
        print("2. Exibir todos os livros")
        print("3. Atualizar preço de um livro")
        print("4. Remover um livro")
        print("5. Buscar livros por autor")
        print("6. Exportar dados para CSV")
        print("7. Importar dados de CSV")
        print("8. Fazer backup do banco de dados")
        print("9. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            titulo = input("Título: ")
            autor = input("Autor: ")
            ano_publicacao = int(input("Ano de Publicação: "))
            preco = float(input("Preço: "))
            add_book(titulo, autor, ano_publicacao, preco)

        elif choice == '2':
            display_books()

        elif choice == '3':
            book_id = int(input("ID do livro: "))
            new_price = float(input("Novo preço: "))
            update_book_price(book_id, new_price)

        elif choice == '4':
            book_id = int(input("ID do livro: "))
            remove_book(book_id)

        elif choice == '5':
            autor = input("Autor: ")
            search_books_by_author(autor)

        elif choice == '6':
            export_to_csv()

        elif choice == '7':
            filename = input("Nome do arquivo CSV: ")
            import_from_csv(filename)

        elif choice == '8':
            backup_db()

        elif choice == '9':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
