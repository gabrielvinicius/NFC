# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from py122u import nfc


def connect_reader():
    try:
        reader.connect()
        messagebox.showinfo("Conectado", "Leitor NFC conectado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao leitor NFC: {str(e)}")


def read_tag():
    try:
        position = int(entry_position.get(), 16)
        data = read_32_bits(reader, position)
        data_str = format(data, '08X')  # Formata para 8 dígitos hexadecimais
        entry_number_input.delete(0, tk.END)
        entry_number_input.insert(0, data_str[:8])  # Retorna apenas os 8 primeiros dígitos
        messagebox.showinfo("Leitura Completa", "Dados lidos com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro de Leitura", f"Não foi possível ler a tag NFC: {str(e)}")


# Função para escrever um número na tag NFC (32 bits)
def write_number():
    try:
        position = int(entry_position.get(), 16)
        number_to_write = int(entry_number_input.get(), 16)
        write_32_bits(reader, position, number_to_write)
        messagebox.showinfo("Escrita Completa", "Número gravado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro de Escrita", f"Não foi possível escrever na tag NFC: {str(e)}")


# Função para escrever 32 bits (4 bytes) na tag NFC
def write_32_bits(r, position, data):
    bytes_data = data.to_bytes(4, byteorder='big')  # Converte para 4 bytes (32 bits)
    r.update_binary_blocks(position, 4, bytes_data)


# Função para ler 32 bits (4 bytes) da tag NFC
def read_32_bits(r, position):
    bytes_data = r.read_binary_blocks(position, 4)
    data = int.from_bytes(bytes_data, byteorder='big')  # Converte os 4 bytes em um número de 32 bits
    return data


# Configuração inicial da interface e leitor
reader = nfc.Reader()

# Interface Gráfica
root = tk.Tk()
root.title("Leitor NFC - ACR122U")

# Campo para Posição
tk.Label(root, text="Posição (Hex):").grid(row=0, column=0, padx=10, pady=10)
entry_position = tk.Entry(root)
entry_position.grid(row=0, column=1, padx=10, pady=10)
entry_position.insert(0, "0x01")

# Campo para Dados (número)
tk.Label(root, text="Número a Gravar (8 dígitos Hexadecimais):").grid(row=1, column=0, padx=10, pady=10)
entry_number_input = tk.Entry(root)
entry_number_input.grid(row=1, column=1, padx=10, pady=10)

# Botão para Conectar Leitor
btn_connect = tk.Button(root, text="Conectar Leitor", command=connect_reader)
btn_connect.grid(row=2, column=0, padx=10, pady=10)

# Botão para Ler Tag
btn_read = tk.Button(root, text="Ler Tag", command=read_tag)
btn_read.grid(row=2, column=1, padx=10, pady=10)

# Botão para Escrever Número
btn_write = tk.Button(root, text="Gravar Número", command=write_number)
btn_write.grid(row=3, column=1, padx=10, pady=10)

# Iniciar a Interface Gráfica
root.mainloop()
