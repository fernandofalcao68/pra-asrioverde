import tkinter as tk
from tkinter import messagebox
from utils import ARQ_USUARIOS, BG, CARD, TXT, carregar_json, salvar_json
from sistema import abrir_sistema


def iniciar_login():
    login_janela = tk.Tk()
    login_janela.title("Login")
    login_janela.geometry("320x260")
    login_janela.config(bg=BG)

    frame = tk.Frame(login_janela, bg=CARD, padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame,
        text="🌳 Sistema de Praças",
        fg=TXT,
        bg=CARD,
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    entrada_user = tk.Entry(frame, justify="center")
    entrada_user.pack(pady=5)

    entrada_senha = tk.Entry(frame, show="*", justify="center")
    entrada_senha.pack(pady=5)

    def verificar_login():
        usuarios = carregar_json(ARQ_USUARIOS)
        usuario = entrada_user.get().strip()
        senha = entrada_senha.get().strip()

        for u in usuarios:
            if u["usuario"] == usuario and u["senha"] == senha:
                login_janela.destroy()
                abrir_sistema(u, iniciar_login)
                return

        messagebox.showerror("Erro", "Login inválido")

    def abrir_cadastro():
        cadastro = tk.Toplevel()
        cadastro.title("Cadastro")
        cadastro.geometry("320x240")
        cadastro.config(bg=BG)

        frame_cadastro = tk.Frame(cadastro, bg=CARD, padx=20, pady=20)
        frame_cadastro.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame_cadastro,
            text="Cadastro",
            fg=TXT,
            bg=CARD,
            font=("Arial", 14, "bold")
        ).pack(pady=5)

        user = tk.Entry(frame_cadastro, justify="center")
        user.pack(pady=5)

        senha = tk.Entry(frame_cadastro, show="*", justify="center")
        senha.pack(pady=5)

        def salvar():
            usuarios = carregar_json(ARQ_USUARIOS)
            novo_usuario = user.get().strip()
            nova_senha = senha.get().strip()

            if not novo_usuario or not nova_senha:
                messagebox.showwarning("Aviso", "Preencha usuário e senha.")
                return

            for u in usuarios:
                if u["usuario"] == novo_usuario:
                    messagebox.showwarning("Erro", "Usuário já existe.")
                    return

            usuarios.append({
                "usuario": novo_usuario,
                "senha": nova_senha,
                "tipo": "visualizador"
            })

            salvar_json(ARQ_USUARIOS, usuarios)
            messagebox.showinfo("Sucesso", "Usuário criado como visualizador.")
            cadastro.destroy()

        tk.Button(
            frame_cadastro,
            text="Cadastrar",
            bg="#4CAF50",
            fg="white",
            command=salvar
        ).pack(pady=10)

    tk.Button(
        frame,
        text="Entrar",
        bg="#4CAF50",
        fg="white",
        command=verificar_login
    ).pack(pady=5)

    tk.Button(
        frame,
        text="Cadastrar",
        bg="#333333",
        fg="white",
        command=abrir_cadastro
    ).pack()

    login_janela.mainloop()