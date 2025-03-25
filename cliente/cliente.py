import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from PIL import Image, ImageTk
import io

# Função para carregar a imagem
def carregar_imagem():
    caminho_imagem = filedialog.askopenfilename(filetypes=[("print", ".png")])
    if caminho_imagem:
        img = Image.open(caminho_imagem)
        img.thumbnail((200, 200))  # Redimensiona a imagem para exibir na interface
        img_tk = ImageTk.PhotoImage(img)

        # Atualiza o rótulo com a imagem original
        label_imagem_original.config(image=img_tk)
        label_imagem_original.image = img_tk  # Mantém a referência da imagem
        return caminho_imagem
    return None

# Função para enviar a imagem para o servidor
def enviar_imagem():
    imagem_path = carregar_imagem()
    if imagem_path:
        try:
            with open(imagem_path, 'rb') as f:
                imagem_bytes = f.read()

            url = 'http://localhost:5000/processar_imagem'  # Endereço do servidor Flask
            files = {'file': (imagem_path, imagem_bytes, 'image/jpeg')}
            response = requests.post(url, files=files)

            if response.status_code == 200:
                # Recebe a imagem processada do servidor
                imagem_processada = Image.open(io.BytesIO(response.content))
                imagem_processada.thumbnail((200, 200))  # Redimensiona para exibir na interface
                img_tk = ImageTk.PhotoImage(imagem_processada)

                # Atualiza a imagem modificada na interface
                label_imagem_modificada.config(image=img_tk)
                label_imagem_modificada.image = img_tk  # Mantém a referência da imagem
            else:
                messagebox.showerror("Erro", "Erro ao processar a imagem no servidor.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar imagem: {e}")
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione uma imagem para enviar.")

# Criando a interface gráfica
root = tk.Tk()
root.title("Cliente - Envio de Imagem")

# Botões e labels
btn_enviar = tk.Button(root, text="Enviar Imagem", command=enviar_imagem)
btn_enviar.pack(pady=10)

label_imagem_original = tk.Label(root)
label_imagem_original.pack(pady=10)

label_imagem_modificada = tk.Label(root)
label_imagem_modificada.pack(pady=10)

root.mainloop()
