import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Função para carregar a imagem
def carregar_imagem():
    caminho_imagem = filedialog.askopenfilename(filetypes=[("Arquivos de imagem", "*.jpg;*.jpeg;*.png")])
    if caminho_imagem:
        img = Image.open(caminho_imagem)
        img.thumbnail((200, 200))  # Redimensiona a imagem para exibir na interface
        img_tk = ImageTk.PhotoImage(img)

        # Atualiza o rótulo com a imagem carregada
        label_imagem_original.config(image=img_tk)
        label_imagem_original.image = img_tk
        return caminho_imagem
    return None

# Criando a interface gráfica
root = tk.Tk()
root.title("Visualizador de Imagem")

# Botão para carregar a imagem
btn_carregar = tk.Button(root, text="Carregar Imagem", command=carregar_imagem)
btn_carregar.pack(pady=10)

# Rótulo para exibir a imagem carregada
label_imagem_original = tk.Label(root)
label_imagem_original.pack(pady=10)

# Inicia o loop principal da interface gráfica
root.mainloop()
