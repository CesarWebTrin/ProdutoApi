from flask import Flask, request, jsonify
import sqlite3

app = Flask('api')

# Função para conectar ao banco de dados SQLite
def conectar_bd():
    return sqlite3.connect('DATA_IMPACTA.db')

# Rota para inserir um novo produto
@app.route('/produtos', methods=['POST'])
def inserir_produto():
    try:
        conexao = conectar_bd()
        cursor = conexao.cursor()
        data = request.get_json()

        cursor.execute("INSERT INTO TB_PRODUTO (Codigo, Nome) VALUES (?, ?)", (data['Codigo'], data['Nome']))
        conexao.commit()
        conexao.close()
        return jsonify({"message": "Produto inserido com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para buscar todos os produtos
@app.route('/produtos', methods=['GET'])
def buscar_produtos():
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM TB_PRODUTO")
    produtos = cursor.fetchall()
    conexao.close()
    return jsonify({"produtos": produtos})

# Rota para buscar um produto específico por Código
@app.route('/produtos/<int:codigo>', methods=['GET'])
def buscar_produto(codigo):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM TB_PRODUTO WHERE Codigo = ?", (codigo,))
    produto = cursor.fetchone()
    conexao.close()
    if produto:
        return jsonify({"produto": produto})
    else:
        return jsonify({"message": "Produto não encontrado"}), 404

# Rota para inserir um componente em um produto específico por Código
@app.route('/produtos/<int:codigo>/componentes', methods=['POST'])
def inserir_componente(codigo):
    try:
        conexao = conectar_bd()
        cursor = conexao.cursor()
        data = request.get_json()

        cursor.execute("INSERT INTO TB_COMPONENTE (Codigo, Indice, SKU, Descricao, Preco, Quantidade) VALUES (?, ?, ?, ?, ?, ?)",
                       (codigo, data['Indice'], data['SKU'], data['Descricao'], data['Preco'], data['Quantidade']))
        conexao.commit()
        conexao.close()
        return jsonify({"message": "Componente inserido com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para buscar um componente de um produto pelo Índice
@app.route('/componentes/<int:codigo>/<int:indice>', methods=['GET'])
def buscar_componente_por_indice(codigo, indice):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM TB_COMPONENTE WHERE Codigo = ? AND Indice = ?", (codigo, indice))
    componente = cursor.fetchone()
    conexao.close()
    if componente:
        return jsonify({"componente": componente})
    else:
        return jsonify({"message": "Componente não encontrado"}), 404

# Rota para buscar todos os componentes de um produto pelo código
@app.route('/api/v1/produto/<int:codigo>/componente', methods=['GET'])
def buscar_componentes_por_codigo(codigo):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM TB_COMPONENTE WHERE Codigo = ?", (codigo,))
    componentes = cursor.fetchall()
    conexao.close()
    return jsonify({"componentes": componentes})

# Rota para buscar um componente de um produto pela descrição
@app.route('/api/v1/produto/componente', methods=['GET'])
def buscar_componente_por_descricao():
    descricao = request.args.get('descricao')
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM TB_COMPONENTE WHERE Descricao = ?", (descricao,))
    componente = cursor.fetchone()
    conexao.close()
    if componente:
        return jsonify({"componente": componente})
    else:
        return jsonify({"message": "Componente não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)