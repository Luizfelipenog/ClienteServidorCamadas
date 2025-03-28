import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from PIL import Image, ImageTk
import io

def carregar_imagem():
    caminho_imagem = filedialog.askopenfilename(filetypes=[("print", ".png")])
    if caminho_imagem:
        img = Image.open(caminho_imagem)
        img.thumbnail((300, 300))  
        img_tk = ImageTk.PhotoImage(img)

        label_imagem_original.config(image=img_tk)
        label_imagem_original.image = img_tk  
        return caminho_imagem
    return None

def exibir_botao_enviar():
    global imagem_path
    imagem_path = carregar_imagem()
    if imagem_path:
        btn_enviar_imagem.pack(pady=20)

def enviar_imagem():
    if imagem_path:
        try:
            with open(imagem_path, 'rb') as f:
                imagem_bytes = f.read()
          #  url = 'http://10.180.45.144:5000/processar_imagem'
            url = 'http://10.180.41.198:5000/processar_imagem' 
            files = {'file': (imagem_path, imagem_bytes, 'image/jpeg')}
            response = requests.post(url, files=files)

            if response.status_code == 200:
                imagem_processada = Image.open(io.BytesIO(response.content))
                imagem_processada.thumbnail((300, 300))  

                img_tk = ImageTk.PhotoImage(imagem_processada)

                label_imagem_modificada.config(image=img_tk)
                label_imagem_modificada.image = img_tk  
            else:
                messagebox.showerror("Erro", "Erro ao processar a imagem no servidor.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar imagem: {e}")
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione uma imagem para enviar.")

def on_enter(e):
    btn_enviar_imagem.config(bg="#0066cc", fg="white")

def on_leave(e):
    btn_enviar_imagem.config(bg="#008CFF", fg="black")

root = tk.Tk()
root.title("Área inicial")
root.geometry("800x600")
root.configure(bg="#B0E0E6") 

btn_escolher_imagem = tk.Button(root, text="📁 Escolher Imagem", command=exibir_botao_enviar,
                                font=("Arial", 12, "bold"), bg="#008CFF", fg="black",
                                relief="flat", padx=10, pady=5, borderwidth=3)
btn_escolher_imagem.pack(pady=20)
btn_escolher_imagem.bind("<Enter>", on_enter)
btn_escolher_imagem.bind("<Leave>", on_leave)

btn_enviar_imagem = tk.Button(root, text="Enviar Imagem", command=enviar_imagem,
                              font=("Arial", 12, "bold"), bg="#008CFF", fg="black",
                              relief="flat", padx=10, pady=5, borderwidth=3)
btn_enviar_imagem.pack_forget()  
btn_enviar_imagem.bind("<Enter>", on_enter)
btn_enviar_imagem.bind("<Leave>", on_leave)

frame_imagens = tk.Frame(root, bg="#B0E0E6")
frame_imagens.pack(pady=20)

label_imagem_original = tk.Label(frame_imagens, text="Original", font=("Arial", 12, "bold"), bg="#B0E0E6")
label_imagem_original.grid(row=0, column=0, padx=20)

label_seta = tk.Label(frame_imagens, text="→", font=("Arial", 20, "bold"), bg="#B0E0E6")
label_seta.grid(row=0, column=1, padx=10)

label_imagem_modificada = tk.Label(frame_imagens, text="Com filtro", font=("Arial", 12, "bold"), bg="#B0E0E6")
label_imagem_modificada.grid(row=0, column=2, padx=20)

root.mainloop()
