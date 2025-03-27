# Cliente-Servidor de Processamento de Imagens

Este projeto implementa um sistema **cliente-servidor** onde o **cliente** envia imagens para o **servidor**, que as processa com filtros de imagem e salva os metadados (como nome da imagem, filtro aplicado e data/hora) em um banco de dados **SQLite**. O servidor é implementado utilizando o framework **Flask**, e a comunicação entre o cliente e o servidor é feita via **HTTP**.

## Funcionalidades

- **Recebimento de Imagem**: O servidor recebe uma imagem enviada pelo cliente via **HTTP POST**.
- **Processamento de Imagem**: O servidor aplica um filtro na imagem recebida. O filtro aplicado pode ser um dos seguintes:
  - **blur**: Aplica um desfoque à imagem.
  - **edge_enhance**: Aplica um filtro para realçar as bordas.
  - **pixelate**: Aplica um efeito de pixelização na imagem.
- **Armazenamento de Metadados**: O servidor armazena os metadados da imagem processada (nome da imagem, filtro aplicado, e data/hora do processamento) em um banco de dados **SQLite**.
- **Retorno da Imagem Processada**: O servidor retorna a imagem processada para o cliente como resposta, no formato **PNG**.

## Tecnologias Utilizadas

- **Flask**: Framework web para construir a API do servidor.
- **Pillow**: Biblioteca para processamento de imagens.
- **SQLite**: Banco de dados utilizado para armazenar os metadados das imagens processadas.

## Como Rodar o Projeto

Este projeto consiste em duas partes: o servidor e o cliente. O servidor recebe e processa imagens, enquanto o cliente envia as imagens para o servidor.

### 1. No Servidor

1. **Certifique-se de que o Python está instalado**:
   - O projeto foi desenvolvido em Python, então é necessário ter o Python instalado na sua máquina. Você pode baixar o Python [aqui](https://www.python.org/downloads/).

2. **Instale as dependências necessárias**:
   - O servidor utiliza as bibliotecas **Flask** (para o servidor web) e **Pillow** (para o processamento de imagens). Para instalar as dependências, execute o seguinte comando no terminal:
     ```bash
     pip install Flask Pillow sqlite3
     ```

3. **Execute o servidor Flask**:
   - O servidor é executado em uma máquina com **IP público** ou **rede local**. Para iniciar o servidor, execute o seguinte comando no terminal:
     ```bash
     python servidor.py
     ```
   - O servidor ficará disponível na URL `http://0.0.0.0:5000`, onde:
     - **0.0.0.0** significa que o servidor escutará em todos os endereços IP da máquina.
     - **5000** é a porta onde o servidor estará aguardando requisições.

4. **Banco de Dados SQLite**:
   - O banco de dados **SQLite** será criado automaticamente na execução do servidor. Ele será usado para armazenar os metadados das imagens processadas (nome da imagem, filtro aplicado, e data/hora).

### 2. No Cliente

1. **Execute o cliente.py**:
   - O cliente envia as imagens para o servidor via HTTP. Para rodar o cliente, execute o seguinte código:
     ```python

     ```
     - Substitua `<IP_PUBLICO_DO_SERVIDOR>` pelo IP público do servidor ou pelo IP da máquina na mesma rede local.
     - O cliente enviará uma imagem (`imagem.jpg`) para o servidor processá-la.

2. **Enviar Imagens**:
   - O cliente pode enviar uma imagem para o servidor, que será processada e, em seguida, a imagem processada será retornada como resposta.



### Escolher a Imagem
![image](https://github.com/user-attachments/assets/260c3d51-3c83-4cc2-8968-f102569e7e16)

### Selecionar
![image](https://github.com/user-attachments/assets/5fd01f8a-259a-4bc4-9990-992e28b85f40)

### Enviar Imagem
![image](https://github.com/user-attachments/assets/57679dd4-55e9-4072-be1d-8a705db717fe)

### Imagem Processada
![image](https://github.com/user-attachments/assets/5139a2e8-bd3b-4208-8f04-0869f173cf32)

   

