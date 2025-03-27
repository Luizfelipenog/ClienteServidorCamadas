from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageFilter
import io
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Diretório para salvar as imagens processadas
OUTPUT_DIR = 'imagens_processadas'

# Certifique-se de que o diretório de saída exista
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Função para aplicar filtros
def aplicar_filtro(img, tipo_filtro):
    try:
        if tipo_filtro == "blur":
            return img.filter(ImageFilter.BLUR)
        elif tipo_filtro == "edge_enhance":
            return img.filter(ImageFilter.EDGE_ENHANCE)
        elif tipo_filtro == "pixelate":
            # Reduz a imagem para um tamanho pequeno e aumenta novamente para simular pixelização
            img_small = img.resize((32, 32), Image.NEAREST)  # Reduzir para 32x32
            return img_small.resize(img.size, Image.NEAREST)  # Aumenta de volta ao tamanho original
        else:
            return img  # Caso o filtro não seja reconhecido, retorna a imagem original
    except Exception as e:
        print(f"Erro ao aplicar o filtro: {e}")
        raise

# Função para salvar metadados no banco de dados SQLite
def salvar_metadados(nome_imagem, filtro, datahora):
    try:
        # Conecta ao banco de dados SQLite
        conn = sqlite3.connect('metadados_imagens.db')
        c = conn.cursor()

        # Cria a tabela se não existir
        c.execute('''
            CREATE TABLE IF NOT EXISTS metadados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_imagem TEXT,
                filtro_aplicado TEXT,
                datahora TEXT
            )
        ''')

        # Insere os metadados na tabela
        c.execute('''
            INSERT INTO metadados (nome_imagem, filtro_aplicado, datahora)
            VALUES (?, ?, ?)
        ''', (nome_imagem, filtro, datahora))

        # Salva (commita) as alterações e fecha a conexão
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Erro ao salvar metadados: {e}")

# Função para buscar os metadados do banco de dados
@app.route('/metadados', methods=['GET'])
def get_metadados():
    try:
        # Conecta ao banco de dados SQLite
        conn = sqlite3.connect('metadados_imagens.db')
        c = conn.cursor()

        # Consulta todos os metadados
        c.execute('SELECT * FROM metadados')
        metadados = c.fetchall()

        # Fecha a conexão
        conn.close()

        # Se não houver metadados, retorna uma mensagem informando
        if not metadados:
            return jsonify({"message": "Nenhum metadado encontrado."}), 404

        # Converte os dados em um formato legível (lista de dicionários)
        metadados_lista = []
        for row in metadados:
            metadados_lista.append({
                'id': row[0],
                'nome_imagem': row[1],
                'filtro_aplicado': row[2],
                'datahora': row[3]
            })

        # Retorna os metadados como resposta JSON
        return jsonify(metadados_lista), 200

    except Exception as e:
        # Se ocorrer algum erro, retorna um erro genérico com a mensagem de erro
        print(f"Erro ao buscar metadados: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/processar_imagem', methods=['POST'])
def processar_imagem():
    try:
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return "Nenhum arquivo enviado", 400
        
        # Recebe o arquivo de imagem
        imagem = request.files['file']
        
        # Abre a imagem usando PIL
        img = Image.open(imagem.stream)
        filtro = request.form.get('filtro', 'blur')  # Pega o filtro, se não for informado, aplica blur

        # Aplica o filtro selecionado
        img = aplicar_filtro(img, filtro)

        # Nome da imagem (pode usar o nome original ou gerar um nome único)
        nome_imagem = f"imagem_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        
        # Caminho para salvar a imagem processada
        imagem_salva_path = os.path.join(OUTPUT_DIR, nome_imagem)

        # Salva a imagem no diretório de saída
        img.save(imagem_salva_path, 'PNG')

        # Salvar metadados no banco de dados
        salvar_metadados(nome_imagem, filtro, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # Converte a imagem modificada para um formato de resposta (PNG)
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')  # Salva como PNG
        img_io.seek(0)  # Retorna ao início do arquivo em memória

        # Envia a imagem modificada de volta para o cliente
        return send_file(img_io, mimetype='image/png')  # Mimetype para PNG

    except Exception as e:
        # Se ocorrer algum erro, retorna um erro genérico com a mensagem de erro
        print(f"Erro ao processar a imagem: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Inicia o servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
