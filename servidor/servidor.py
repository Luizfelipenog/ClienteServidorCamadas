from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageFilter
import io
import os

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

        # Caminho para salvar a imagem processada
        imagem_salva_path = os.path.join(OUTPUT_DIR, 'imagem_processada.png')

        # Salva a imagem no diretório de saída
        img.save(imagem_salva_path, 'PNG')

        # Retorna uma mensagem de sucesso com o caminho do arquivo
        print(f"Imagem processada com sucesso! Imagem salva em: {imagem_salva_path}")

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
