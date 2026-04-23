import tkinter as tk
from tkinter import messagebox
from utils import ARQ_DADOS, BG, CARD, TXT, carregar_json, salvar_json


def abrir_sistema(usuario_logado, callback_logout):
    janela = tk.Tk()
    janela.title("Sistema de Praças")
    janela.state("zoomed")
    janela.config(bg=BG)

    pracas = carregar_json(ARQ_DADOS)
    tipo_usuario = usuario_logado["tipo"]

    def logout():
        janela.destroy()
        callback_logout()

    topo = tk.Frame(janela, bg=BG)
    topo.pack(fill="x", pady=10)

    tk.Label(
        topo,
        text=f"🌳 Sistema ({tipo_usuario})",
        fg=TXT,
        bg=BG,
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=10)

    tk.Button(
        topo,
        text="Logout",
        bg="red",
        fg="white",
        command=logout
    ).pack(side="right", padx=10)

    container = tk.Frame(janela, bg=BG)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scroll_frame = tk.Frame(canvas, bg=BG)
    canvas.create_window((0, 0), window=scroll_frame, anchor="n")

    def atualizar_scroll(_evento=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scroll_frame.bind("<Configure>", atualizar_scroll)

    canvas.bind_all(
        "<MouseWheel>",
        lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
    )

    def listar():
        for w in scroll_frame.winfo_children():
            w.destroy()

        if tipo_usuario != "visualizador":
            frame_add = tk.Frame(scroll_frame, bg=BG)
            frame_add.pack(pady=20)

            entrada_nome = tk.Entry(frame_add, width=25, justify="center")
            entrada_nome.pack(side=tk.LEFT, padx=5)

            entrada_endereco = tk.Entry(frame_add, width=25, justify="center")
            entrada_endereco.pack(side=tk.LEFT, padx=5)

            def adicionar():
                nome = entrada_nome.get().strip()
                endereco = entrada_endereco.get().strip()

                if not nome or not endereco:
                    messagebox.showwarning("Aviso", "Preencha nome e endereço.")
                    return

                pracas.append({
                    "nome": nome,
                    "endereco": endereco
                })
                salvar_json(ARQ_DADOS, pracas)
                listar()

            tk.Button(
                frame_add,
                text="Adicionar",
                bg="#4CAF50",
                fg="white",
                command=adicionar
            ).pack(side=tk.LEFT, padx=5)

        for i, p in enumerate(pracas):
            card = tk.Frame(scroll_frame, bg=CARD, padx=15, pady=10)
            card.pack(fill="x", padx=200, pady=5)

            tk.Label(
                card,
                text=p["nome"],
                fg=TXT,
                bg=CARD,
                font=("Arial", 13, "bold")
            ).pack(anchor="w")

            tk.Label(
                card,
                text=p["endereco"],
                fg=TXT,
                bg=CARD
            ).pack(anchor="w")

            if tipo_usuario != "visualizador":
                def remover(indice=i):
                    pracas.pop(indice)
                    salvar_json(ARQ_DADOS, pracas)
                    listar()

                tk.Button(
                    card,
                    text="Remover",
                    bg="red",
                    fg="white",
                    command=remover
                ).pack(anchor="e")

        atualizar_scroll()

    listar()
    janela.mainloop()