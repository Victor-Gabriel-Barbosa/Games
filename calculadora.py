import tkinter as tk
from tkinter import messagebox, ttk
import math
import datetime
from decimal import Decimal, ROUND_HALF_UP

class CalculadoraCompleta:
    def __init__(self, master):
        self.master = master
        master.title("Calculadora Completa")
        master.configure(bg="#f0f0f0")
        
        # Variável para armazenar a expressão atual
        self.expressao = ""
        self.resultado_anterior = 0
        self.modo_rad = True  # True para radianos, False para graus
        
        # Criar abas para as calculadoras
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba básica
        self.aba_basica = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_basica, text="Básica")
        
        # Aba científica
        self.aba_cientifica = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_cientifica, text="Científica")
        
        # Aba financeira
        self.aba_financeira = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_financeira, text="Financeira")
        
        # Configurar cada aba
        self.configurar_aba_basica()
        self.configurar_aba_cientifica()
        self.configurar_aba_financeira()
        
        # Configurar histórico
        self.historico = []
        self.criar_historico()
        
        # Adicionar suporte para teclado
        master.bind("<Key>", self.teclado_pressionado)
    
    def configurar_aba_basica(self):
        # Frame para o display
        frame_display = ttk.Frame(self.aba_basica)
        frame_display.pack(fill=tk.X, padx=5, pady=5)
        
        # Campo de exibição
        self.display = tk.Entry(frame_display, width=25, font=('Arial', 16), bd=5, justify=tk.RIGHT)
        self.display.pack(fill=tk.X, padx=5, pady=5)
        self.display.insert(0, "0")
        self.display.config(state="readonly")
        
        # Frame para botões
        frame_botoes = ttk.Frame(self.aba_basica)
        frame_botoes.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configurar grid para botões
        for i in range(6):
            frame_botoes.rowconfigure(i, weight=1)
        for i in range(4):
            frame_botoes.columnconfigure(i, weight=1)
        
        # Definir botões - [texto, linha, coluna, cor]
        botoes = [
            ["C", 0, 0, "#ff6666"], ["(", 0, 1, "#b3b3b3"], [")", 0, 2, "#b3b3b3"], ["/", 0, 3, "#ffcc00"],
            ["7", 1, 0, "#ffffff"], ["8", 1, 1, "#ffffff"], ["9", 1, 2, "#ffffff"], ["*", 1, 3, "#ffcc00"],
            ["4", 2, 0, "#ffffff"], ["5", 2, 1, "#ffffff"], ["6", 2, 2, "#ffffff"], ["-", 2, 3, "#ffcc00"],
            ["1", 3, 0, "#ffffff"], ["2", 3, 1, "#ffffff"], ["3", 3, 2, "#ffffff"], ["+", 3, 3, "#ffcc00"],
            ["0", 4, 0, "#ffffff"], [".", 4, 1, "#ffffff"], ["⌫", 4, 2, "#b3b3b3"], ["=", 4, 3, "#66cc66"],
            ["MC", 5, 0, "#d9d9d9"], ["MR", 5, 1, "#d9d9d9"], ["M+", 5, 2, "#d9d9d9"], ["M-", 5, 3, "#d9d9d9"]
        ]
        
        # Criar os botões
        for texto, linha, coluna, cor in botoes:
            comando = lambda x=texto: self.clicar_botao(x)
            botao = tk.Button(frame_botoes, text=texto, width=5, height=2, 
                            font=('Arial', 12, 'bold'), bg=cor, 
                            command=comando)
            botao.grid(row=linha, column=coluna, padx=5, pady=5, sticky="nsew")
    
    def configurar_aba_cientifica(self):
        # Frame para o display
        frame_display = ttk.Frame(self.aba_cientifica)
        frame_display.pack(fill=tk.X, padx=5, pady=5)
        
        # Campo de exibição (o mesmo que na aba básica)
        self.display_cient = tk.Entry(frame_display, width=25, font=('Arial', 16), bd=5, justify=tk.RIGHT)
        self.display_cient.pack(fill=tk.X, padx=5, pady=5)
        self.display_cient.insert(0, "0")
        self.display_cient.config(state="readonly")
        
        # Criar frame para modo radianos/graus
        frame_modo = ttk.Frame(frame_display)
        frame_modo.pack(fill=tk.X, padx=5)
        
        # Botão de alternar modo
        self.btn_modo = tk.Button(frame_modo, text="RAD", width=8, 
                                font=('Arial', 10), bg="#d9d9d9",
                                command=self.alternar_modo)
        self.btn_modo.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Frame para botões científicos
        frame_botoes = ttk.Frame(self.aba_cientifica)
        frame_botoes.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configurar grid para botões
        for i in range(8):
            frame_botoes.rowconfigure(i, weight=1)
        for i in range(5):
            frame_botoes.columnconfigure(i, weight=1)
        
        # Definir botões científicos - [texto, linha, coluna, cor]
        botoes = [
            ["2nd", 0, 0, "#b3b3b3"], ["π", 0, 1, "#b3b3b3"], ["e", 0, 2, "#b3b3b3"], 
            ["C", 0, 3, "#ff6666"], ["⌫", 0, 4, "#b3b3b3"],
            
            ["x²", 1, 0, "#b3b3b3"], ["x³", 1, 1, "#b3b3b3"], ["xʸ", 1, 2, "#b3b3b3"], 
            ["(", 1, 3, "#b3b3b3"], [")", 1, 4, "#b3b3b3"],
            
            ["√x", 2, 0, "#b3b3b3"], ["∛x", 2, 1, "#b3b3b3"], ["ʸ√x", 2, 2, "#b3b3b3"], 
            ["ln", 2, 3, "#b3b3b3"], ["log", 2, 4, "#b3b3b3"],
            
            ["sin", 3, 0, "#b3b3b3"], ["cos", 3, 1, "#b3b3b3"], ["tan", 3, 2, "#b3b3b3"], 
            ["!", 3, 3, "#b3b3b3"], ["1/x", 3, 4, "#b3b3b3"],
            
            ["asin", 4, 0, "#b3b3b3"], ["acos", 4, 1, "#b3b3b3"], ["atan", 4, 2, "#b3b3b3"], 
            ["7", 4, 3, "#ffffff"], ["8", 4, 4, "#ffffff"],
            
            ["sinh", 5, 0, "#b3b3b3"], ["cosh", 5, 1, "#b3b3b3"], ["tanh", 5, 2, "#b3b3b3"], 
            ["4", 5, 3, "#ffffff"], ["5", 5, 4, "#ffffff"],
            
            ["mod", 6, 0, "#b3b3b3"], ["exp", 6, 1, "#b3b3b3"], ["|x|", 6, 2, "#b3b3b3"], 
            ["1", 6, 3, "#ffffff"], ["2", 6, 4, "#ffffff"],
            
            ["deg", 7, 0, "#b3b3b3"], ["rad", 7, 1, "#b3b3b3"], ["+/-", 7, 2, "#b3b3b3"], 
            ["0", 7, 3, "#ffffff"], [".", 7, 4, "#ffffff"],
        ]
        
        # Criar os botões
        self.botoes_cient = {}
        for texto, linha, coluna, cor in botoes:
            comando = lambda x=texto: self.clicar_botao_cientifico(x)
            botao = tk.Button(frame_botoes, text=texto, width=5, height=2, 
                            font=('Arial', 10, 'bold'), bg=cor, 
                            command=comando)
            botao.grid(row=linha, column=coluna, padx=3, pady=3, sticky="nsew")
            self.botoes_cient[texto] = botao
        
        # Adicionar botões de operadores
        operadores = [
            ["/", 1, 0], ["*", 2, 0], ["-", 3, 0], ["+", 4, 0], ["=", 5, 0]
        ]
        
        frame_ops = ttk.Frame(frame_botoes)
        frame_ops.grid(row=1, column=5, rowspan=5, padx=3, pady=3, sticky="nsew")
        
        for texto, linha, coluna in operadores:
            comando = lambda x=texto: self.clicar_botao_cientifico(x)
            cor = "#ffcc00" if texto != "=" else "#66cc66"
            botao = tk.Button(frame_ops, text=texto, width=5, height=2, 
                           font=('Arial', 12, 'bold'), bg=cor, 
                           command=comando)
            botao.grid(row=linha, column=coluna, padx=3, pady=3, sticky="nsew")
            
    def configurar_aba_financeira(self):
        # Frame principal para a calculadora financeira
        self.frame_fin = ttk.Frame(self.aba_financeira)
        self.frame_fin.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para seleção de calculadora financeira
        frame_selecao = ttk.Frame(self.frame_fin)
        frame_selecao.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(frame_selecao, text="Calculadora:", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        
        # Opções de calculadoras financeiras
        self.opcoes_calculadoras = [
            "Juros Compostos",
            "Valor Presente",
            "Valor Futuro",
            "Empréstimo/Financiamento",
            "Amortização",
            "Investimento Regular",
            "Retorno de Investimento (ROI)"
        ]
        
        self.calculadora_selecionada = tk.StringVar()
        self.calculadora_selecionada.set(self.opcoes_calculadoras[0])
        
        # ComboBox para seleção da calculadora
        self.combo_calculadoras = ttk.Combobox(frame_selecao, 
                                              textvariable=self.calculadora_selecionada,
                                              values=self.opcoes_calculadoras,
                                              state="readonly",
                                              font=('Arial', 12),
                                              width=25)
        self.combo_calculadoras.pack(side=tk.LEFT, padx=5, pady=5)
        self.combo_calculadoras.bind("<<ComboboxSelected>>", self.mudar_calculadora_financeira)
        
        # Frame para os campos de entrada
        self.frame_campos = ttk.Frame(self.frame_fin)
        self.frame_campos.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para resultados
        self.frame_resultados = ttk.Frame(self.frame_fin)
        self.frame_resultados.pack(fill=tk.X, padx=5, pady=5)
        
        # Adicionar campos para a calculadora de Juros Compostos (padrão)
        self.configurar_juros_compostos()
        
    def mudar_calculadora_financeira(self, event=None):
        # Limpar o frame de campos e resultados
        for widget in self.frame_campos.winfo_children():
            widget.destroy()
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()
        
        # Configurar os campos para a calculadora selecionada
        calculadora = self.calculadora_selecionada.get()
        
        if calculadora == "Juros Compostos":
            self.configurar_juros_compostos()
        elif calculadora == "Valor Presente":
            self.configurar_valor_presente()
        elif calculadora == "Valor Futuro":
            self.configurar_valor_futuro()
        elif calculadora == "Empréstimo/Financiamento":
            self.configurar_emprestimo()
        elif calculadora == "Amortização":
            self.configurar_amortizacao()
        elif calculadora == "Investimento Regular":
            self.configurar_investimento_regular()
        elif calculadora == "Retorno de Investimento (ROI)":
            self.configurar_roi()
            
    def configurar_juros_compostos(self):
        # Configuração da calculadora de juros compostos
        # Cria os campos necessários
        ttk.Label(self.frame_campos, text="Principal (Capital Inicial):", font=('Arial', 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.principal_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.principal_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Taxa de Juros (% ao ano):", font=('Arial', 11)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.taxa_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.taxa_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Tempo (anos):", font=('Arial', 11)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.tempo_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.tempo_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Frequência de capitalização:", font=('Arial', 11)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.frequencia_var = tk.StringVar()
        frequencias = ["Anual", "Semestral", "Trimestral", "Mensal", "Diária", "Contínua"]
        self.frequencia_combo = ttk.Combobox(self.frame_campos, textvariable=self.frequencia_var, values=frequencias, state="readonly", width=13, font=('Arial', 11))
        self.frequencia_combo.grid(row=3, column=1, padx=5, pady=5)
        self.frequencia_combo.current(0)
        
        # Botão para calcular
        ttk.Button(self.frame_campos, text="Calcular", 
                  command=self.calcular_juros_compostos,
                  style="Accentbutton.TButton").grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        
        # Estilo para o botão de calcular
        style = ttk.Style()
        style.configure("Accentbutton.TButton", font=('Arial', 12, 'bold'), foreground='white', background='#4CAF50')
        
        # Resultados
        ttk.Label(self.frame_resultados, text="Montante Final:", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.montante_label = ttk.Label(self.frame_resultados, text="R$ 0,00", font=('Arial', 12))
        self.montante_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.frame_resultados, text="Juros Ganhos:", font=('Arial', 12, 'bold')).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.juros_label = ttk.Label(self.frame_resultados, text="R$ 0,00", font=('Arial', 12))
        self.juros_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
    def calcular_juros_compostos(self):
        try:
            # Obter valores dos campos
            principal = float(self.principal_entry.get().replace(',', '.'))
            taxa = float(self.taxa_entry.get().replace(',', '.')) / 100  # Converter para decimal
            tempo = float(self.tempo_entry.get().replace(',', '.'))
            frequencia = self.frequencia_var.get()
            
            # Determinar o número de períodos de capitalização
            if frequencia == "Anual":
                n = 1
            elif frequencia == "Semestral":
                n = 2
            elif frequencia == "Trimestral":
                n = 4
            elif frequencia == "Mensal":
                n = 12
            elif frequencia == "Diária":
                n = 365
            
            # Calcular montante
            if frequencia == "Contínua":
                montante = principal * math.exp(taxa * tempo)
            else:
                montante = principal * ((1 + (taxa / n)) ** (n * tempo))
            
            juros = montante - principal
            
            # Atualizar os rótulos de resultados
            self.montante_label.config(text=f"R$ {montante:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            self.juros_label.config(text=f"R$ {juros:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            
            # Adicionar ao histórico
            entrada = f"Juros Compostos: P={principal:.2f}, i={taxa*100:.2f}%, t={tempo:.2f}, n={frequencia} -> Montante={montante:.2f}"
            self.historico.append(entrada)
            self.lista_historico.insert(0, entrada)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def configurar_valor_presente(self):
        # Configuração da calculadora de valor presente
        ttk.Label(self.frame_campos, text="Valor Futuro (VF):", font=('Arial', 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.vf_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.vf_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Taxa de Juros (% ao ano):", font=('Arial', 11)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.taxa_vp_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.taxa_vp_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Tempo (anos):", font=('Arial', 11)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.tempo_vp_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.tempo_vp_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Botão para calcular
        ttk.Button(self.frame_campos, text="Calcular", 
                  command=self.calcular_valor_presente,
                  style="Accentbutton.TButton").grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        # Resultados
        ttk.Label(self.frame_resultados, text="Valor Presente:", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.vp_result_label = ttk.Label(self.frame_resultados, text="R$ 0,00", font=('Arial', 12))
        self.vp_result_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
    def calcular_valor_presente(self):
        try:
            # Obter valores dos campos
            vf = float(self.vf_entry.get().replace(',', '.'))
            taxa = float(self.taxa_vp_entry.get().replace(',', '.')) / 100  # Converter para decimal
            tempo = float(self.tempo_vp_entry.get().replace(',', '.'))
            
            # Calcular valor presente
            vp = vf / ((1 + taxa) ** tempo)
            
            # Atualizar o rótulo de resultado
            self.vp_result_label.config(text=f"R$ {vp:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            
            # Adicionar ao histórico
            entrada = f"Valor Presente: VF={vf:.2f}, i={taxa*100:.2f}%, t={tempo:.2f} -> VP={vp:.2f}"
            self.historico.append(entrada)
            self.lista_historico.insert(0, entrada)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def configurar_valor_futuro(self):
        # Configuração da calculadora de valor futuro
        ttk.Label(self.frame_campos, text="Valor Presente (VP):", font=('Arial', 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.vp_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.vp_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Taxa de Juros (% ao ano):", font=('Arial', 11)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.taxa_vf_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.taxa_vf_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Tempo (anos):", font=('Arial', 11)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.tempo_vf_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.tempo_vf_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Botão para calcular
        ttk.Button(self.frame_campos, text="Calcular", 
                  command=self.calcular_valor_futuro,
                  style="Accentbutton.TButton").grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        # Resultados
        ttk.Label(self.frame_resultados, text="Valor Futuro:", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.vf_result_label = ttk.Label(self.frame_resultados, text="R$ 0,00", font=('Arial', 12))
        self.vf_result_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
    def calcular_valor_futuro(self):
        try:
            # Obter valores dos campos
            vp = float(self.vp_entry.get().replace(',', '.'))
            taxa = float(self.taxa_vf_entry.get().replace(',', '.')) / 100  # Converter para decimal
            tempo = float(self.tempo_vf_entry.get().replace(',', '.'))
            
            # Calcular valor futuro
            vf = vp * ((1 + taxa) ** tempo)
            
            # Atualizar o rótulo de resultado
            self.vf_result_label.config(text=f"R$ {vf:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            
            # Adicionar ao histórico
            entrada = f"Valor Futuro: VP={vp:.2f}, i={taxa*100:.2f}%, t={tempo:.2f} -> VF={vf:.2f}"
            self.historico.append(entrada)
            self.lista_historico.insert(0, entrada)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def configurar_emprestimo(self):
        # Configuração da calculadora de empréstimo
        ttk.Label(self.frame_campos, text="Valor do Empréstimo:", font=('Arial', 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.emprestimo_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.emprestimo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Taxa de Juros (% ao ano):", font=('Arial', 11)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.taxa_emp_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.taxa_emp_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Prazo (meses):", font=('Arial', 11)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.prazo_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.prazo_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Botão para calcular
        ttk.Button(self.frame_campos, text="Calcular", 
                  command=self.calcular_emprestimo,
                  style="Accentbutton.TButton").grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        # Resultados
        ttk.Label(self.frame_resultados, text="Pagamento Mensal:", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.mensalidade_label = ttk.Label(self.frame_resultados, text="R$ 0,00", font=('Arial', 12))
        self.mensalidade_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.frame_resultados, text="Total de Juros:", font=('Arial', 12, 'bold')).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.total_juros_label = ttk.Label(self.frame_resultados, text="R$ 0,00", font=('Arial', 12))
        self.total_juros_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.frame_resultados, text="Total Pago:", font=('Arial', 12, 'bold')).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.total_pago_label = ttk.Label(self.frame_resultados, text="R$ 0,00", font=('Arial', 12))
        self.total_pago_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
    def calcular_emprestimo(self):
        try:
            # Obter valores dos campos
            emprestimo = float(self.emprestimo_entry.get().replace(',', '.'))
            taxa_anual = float(self.taxa_emp_entry.get().replace(',', '.')) / 100  # Converter para decimal
            prazo = int(self.prazo_entry.get().replace(',', '.'))
            
            # Converter taxa anual para mensal
            taxa_mensal = taxa_anual / 12
            
            # Calcular pagamento mensal (PMT)
            if taxa_mensal == 0:
                mensalidade = emprestimo / prazo
            else:
                mensalidade = emprestimo * (taxa_mensal * (1 + taxa_mensal) ** prazo) / ((1 + taxa_mensal) ** prazo - 1)
            
            total_pago = mensalidade * prazo
            total_juros = total_pago - emprestimo
            
            # Atualizar os rótulos de resultados
            self.mensalidade_label.config(text=f"R$ {mensalidade:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            self.total_juros_label.config(text=f"R$ {total_juros:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            self.total_pago_label.config(text=f"R$ {total_pago:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            
            # Adicionar ao histórico
            entrada = f"Empréstimo: Valor={emprestimo:.2f}, i={taxa_anual*100:.2f}%, Prazo={prazo} meses -> PMT={mensalidade:.2f}"
            self.historico.append(entrada)
            self.lista_historico.insert(0, entrada)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def configurar_amortizacao(self):
        # Configuração da calculadora de amortização
        ttk.Label(self.frame_campos, text="Valor do Empréstimo:", font=('Arial', 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.emprestimo_amort_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.emprestimo_amort_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Taxa de Juros (% ao ano):", font=('Arial', 11)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.taxa_amort_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.taxa_amort_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Prazo (meses):", font=('Arial', 11)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.prazo_amort_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.prazo_amort_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Sistema de Amortização:", font=('Arial', 11)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.sistema_var = tk.StringVar()
        sistemas = ["SAC - Sistema de Amortização Constante", "Price - Prestações Fixas"]
        self.sistema_combo = ttk.Combobox(self.frame_campos, textvariable=self.sistema_var, values=sistemas, state="readonly", width=30, font=('Arial', 11))
        self.sistema_combo.grid(row=3, column=1, padx=5, pady=5)
        self.sistema_combo.current(0)
        
        # Botão para calcular
        ttk.Button(self.frame_campos, text="Gerar Tabela de Amortização", 
                  command=self.calcular_amortizacao,
                  style="Accentbutton.TButton").grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        
        # Frame para a tabela de amortização
        self.frame_tabela = ttk.Frame(self.frame_resultados)
        self.frame_tabela.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def calcular_amortizacao(self):
        try:
            # Limpar o frame da tabela
            for widget in self.frame_tabela.winfo_children():
                widget.destroy()
            
            # Obter valores dos campos
            emprestimo = float(self.emprestimo_amort_entry.get().replace(',', '.'))
            taxa_anual = float(self.taxa_amort_entry.get().replace(',', '.')) / 100  # Converter para decimal
            prazo = int(self.prazo_amort_entry.get().replace(',', '.'))
            sistema = self.sistema_var.get()
            
            # Converter taxa anual para mensal
            taxa_mensal = taxa_anual / 12
            
            # Criar treeview para a tabela
            colunas = ('mes', 'prestacao', 'juros', 'amortizacao', 'saldo')
            tabela = ttk.Treeview(self.frame_tabela, columns=colunas, show='headings')
            
            # Configurar colunas
            tabela.heading('mes', text='Mês')
            tabela.heading('prestacao', text='Prestação')
            tabela.heading('juros', text='Juros')
            tabela.heading('amortizacao', text='Amortização')
            tabela.heading('saldo', text='Saldo Devedor')
            
            tabela.column('mes', width=50, anchor=tk.CENTER)
            tabela.column('prestacao', width=100, anchor=tk.E)
            tabela.column('juros', width=100, anchor=tk.E)
            tabela.column('amortizacao', width=100, anchor=tk.E)
            tabela.column('saldo', width=120, anchor=tk.E)
            
            tabela.pack(fill=tk.BOTH, expand=True)
            
            # Adicionar scrollbar
            scrollbar = ttk.Scrollbar(self.frame_tabela, orient=tk.VERTICAL, command=tabela.yview)
            tabela.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Calcular a tabela de amortização
            saldo = emprestimo
            total_juros = 0
            total_pago = 0
            
            # Linha 0 (inicial)
            tabela.insert('', 'end', values=(0, "-", "-", "-", f"R$ {saldo:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')))
            
            if sistema == "SAC - Sistema de Amortização Constante":
                # Cálculo pelo sistema SAC
                amortizacao = emprestimo / prazo
                
                for mes in range(1, prazo + 1):
                    juros = saldo * taxa_mensal
                    prestacao = amortizacao + juros
                    saldo -= amortizacao
                    
                    total_juros += juros
                    total_pago += prestacao
                    
                    tabela.insert('', 'end', values=(
                        mes,
                        f"R$ {prestacao:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                        f"R$ {juros:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                        f"R$ {amortizacao:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                        f"R$ {saldo:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                    ))
            else:
                # Cálculo pelo sistema Price
                prestacao = emprestimo * (taxa_mensal * (1 + taxa_mensal) ** prazo) / ((1 + taxa_mensal) ** prazo - 1)
                
                for mes in range(1, prazo + 1):
                    juros = saldo * taxa_mensal
                    amortizacao = prestacao - juros
                    saldo -= amortizacao
                    
                    total_juros += juros
                    total_pago += prestacao
                    
                    # Corrigir possíveis erros de arredondamento no último mês
                    if mes == prazo:
                        amortizacao += saldo
                        saldo = 0
                    
                    tabela.insert('', 'end', values=(
                        mes,
                        f"R$ {prestacao:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                        f"R$ {juros:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                        f"R$ {amortizacao:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                        f"R$ {max(0, saldo):,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                    ))
            
            # Adicionar linha de totais
            tabela.insert('', 'end', values=(
                "TOTAL",
                f"R$ {total_pago:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                f"R$ {total_juros:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                f"R$ {emprestimo:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                "-"
            ))
            
            # Adicionar ao histórico
            entrada = f"Amortização: Valor={emprestimo:.2f}, i={taxa_anual*100:.2f}%, Prazo={prazo} meses, Sistema={sistema}"
            self.historico.append(entrada)
            self.lista_historico.insert(0, entrada)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            
    def configurar_investimento_regular(self):
        # Configuração da calculadora de investimento regular
        ttk.Label(self.frame_campos, text="Depósito Mensal:", font=('Arial', 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.deposito_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.deposito_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Taxa de Juros (% ao ano):", font=('Arial', 11)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.taxa_inv_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.taxa_inv_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Tempo (anos):", font=('Arial', 11)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.tempo_inv_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.tempo_inv_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Depósito Inicial (opcional):", font=('Arial', 11)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.inicial_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.inicial_entry.grid(row=3, column=1, padx=5, pady=5)
        self.inicial_entry.insert(0, "0")
        
        # Botão para calcular
        ttk.Button(self.frame_campos, text="Calcular", 
                  command=self.calcular_investimento_regular,
                  style="Accentbutton.TButton").grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        
        # Resultados
        ttk.Label(self.frame_resultados, text="Valor Total Acumulado:", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.montante_inv_label = ttk.Label(self.frame_resultados, text="R$ 0,00", font=('Arial', 12))
        self.montante_inv_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.frame_resultados, text="Total Investido:", font=('Arial', 12, 'bold')).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.total_inv_label = ttk.Label(self.frame_resultados, text="R$ 0,00", font=('Arial', 12))
        self.total_inv_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.frame_resultados, text="Juros Ganhos:", font=('Arial', 12, 'bold')).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.juros_inv_label = ttk.Label(self.frame_resultados, text="R$ 0,00", font=('Arial', 12))
        self.juros_inv_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
    def calcular_investimento_regular(self):
        try:
            # Obter valores dos campos
            deposito = float(self.deposito_entry.get().replace(',', '.'))
            taxa_anual = float(self.taxa_inv_entry.get().replace(',', '.')) / 100  # Converter para decimal
            tempo_anos = float(self.tempo_inv_entry.get().replace(',', '.'))
            inicial = float(self.inicial_entry.get().replace(',', '.') or "0")
            
            # Converter taxa anual para mensal
            taxa_mensal = taxa_anual / 12
            tempo_meses = int(tempo_anos * 12)
            
            # Calcular o montante acumulado com depósitos mensais
            montante = inicial
            for _ in range(tempo_meses):
                montante = montante * (1 + taxa_mensal) + deposito
            
            total_investido = inicial + (deposito * tempo_meses)
            juros_ganhos = montante - total_investido
            
            # Atualizar os rótulos de resultados
            self.montante_inv_label.config(text=f"R$ {montante:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            self.total_inv_label.config(text=f"R$ {total_investido:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            self.juros_inv_label.config(text=f"R$ {juros_ganhos:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            
            # Adicionar ao histórico
            entrada = f"Investimento Regular: Depósito={deposito:.2f}, i={taxa_anual*100:.2f}%, t={tempo_anos:.2f} anos -> Montante={montante:.2f}"
            self.historico.append(entrada)
            self.lista_historico.insert(0, entrada)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            
    def configurar_roi(self):
        # Configuração da calculadora de ROI
        ttk.Label(self.frame_campos, text="Investimento Inicial:", font=('Arial', 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.investimento_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.investimento_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Retorno Total:", font=('Arial', 11)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.retorno_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.retorno_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_campos, text="Período (anos):", font=('Arial', 11)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.periodo_entry = ttk.Entry(self.frame_campos, width=15, font=('Arial', 11))
        self.periodo_entry.grid(row=2, column=1, padx=5, pady=5)
        self.periodo_entry.insert(0, "1")
        
        # Botão para calcular
        ttk.Button(self.frame_campos, text="Calcular", 
                  command=self.calcular_roi,
                  style="Accentbutton.TButton").grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        # Resultados
        ttk.Label(self.frame_resultados, text="ROI Total:", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.roi_total_label = ttk.Label(self.frame_resultados, text="0,00%", font=('Arial', 12))
        self.roi_total_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.frame_resultados, text="ROI Anualizado:", font=('Arial', 12, 'bold')).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.roi_anual_label = ttk.Label(self.frame_resultados, text="0,00%", font=('Arial', 12))
        self.roi_anual_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.frame_resultados, text="Lucro Líquido:", font=('Arial', 12, 'bold')).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.lucro_label = ttk.Label(self.frame_resultados, text="R$ 0,00", font=('Arial', 12))
        self.lucro_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
    def calcular_roi(self):
        try:
            # Obter valores dos campos
            investimento = float(self.investimento_entry.get().replace(',', '.'))
            retorno = float(self.retorno_entry.get().replace(',', '.'))
            periodo = float(self.periodo_entry.get().replace(',', '.'))
            
            # Calcular ROI total
            lucro = retorno - investimento
            roi_total = (lucro / investimento) * 100
            
            # Calcular ROI anualizado
            if periodo > 0:
                roi_anual = ((1 + roi_total / 100) ** (1 / periodo) - 1) * 100
            else:
                roi_anual = roi_total
            
            # Atualizar os rótulos de resultados
            self.roi_total_label.config(text=f"{roi_total:.2f}%".replace('.', ','))
            self.roi_anual_label.config(text=f"{roi_anual:.2f}%".replace('.', ','))
            self.lucro_label.config(text=f"R$ {lucro:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            
            # Adicionar ao histórico
            entrada = f"ROI: Investimento={investimento:.2f}, Retorno={retorno:.2f}, Período={periodo:.2f} anos -> ROI={roi_total:.2f}%"
            self.historico.append(entrada)
            self.lista_historico.insert(0, entrada)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def criar_historico(self):
        # Frame para histórico
        self.frame_historico = ttk.Frame(self.master)
        self.frame_historico.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Label para o histórico
        ttk.Label(self.frame_historico, text="Histórico", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Lista para o histórico
        self.lista_historico = tk.Listbox(self.frame_historico, width=25, height=20, font=('Arial', 10))
        self.lista_historico.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Permitir selecionar itens do histórico
        self.lista_historico.bind('<<ListboxSelect>>', self.selecionar_historico)
        
        # Botão para limpar histórico
        ttk.Button(self.frame_historico, text="Limpar Histórico", 
                command=self.limpar_historico).pack(pady=5)
    
    def limpar_historico(self):
        self.historico = []
        self.lista_historico.delete(0, tk.END)
    
    def selecionar_historico(self, event):
        if self.lista_historico.curselection():
            indice = self.lista_historico.curselection()[0]
            expressao = self.historico[indice].split(" -> ")[0]
            messagebox.showinfo("Histórico", expressao)
    
    def alternar_modo(self):
        self.modo_rad = not self.modo_rad
        self.btn_modo.config(text="RAD" if self.modo_rad else "DEG")
    
    def teclado_pressionado(self, event):
        key = event.char
        
        # Números e operadores
        if key in "0123456789+-*/().":
            self.clicar_botao(key)
        # Enter ou igual para calcular
        elif key == "\r" or key == "=":
            self.clicar_botao("=")
        # Backspace
        elif event.keysym == "BackSpace":
            self.clicar_botao("⌫")
        # Esc ou Delete para limpar
        elif event.keysym == "Escape" or event.keysym == "Delete":
            self.clicar_botao("C")
    
    def clicar_botao(self, texto):
        # Atualizar ambos os displays
        tab_atual = self.notebook.index(self.notebook.select())
        
        # Botões de memória
        if texto == "MC":  # Memory Clear
            self.resultado_anterior = 0
            return
        elif texto == "MR":  # Memory Recall
            self.expressao = str(self.resultado_anterior)
            self.atualizar_display(self.expressao)
            return
        elif texto == "M+":  # Memory Add
            try:
                valor = eval(self.expressao)
                self.resultado_anterior += valor
            except:
                pass
            return
        elif texto == "M-":  # Memory Subtract
            try:
                valor = eval(self.expressao)
                self.resultado_anterior -= valor
            except:
                pass
            return
        
        # Para os botões normais
        self.processar_botao(texto)
        
        # Atualizar o display adequado
        if tab_atual == 0:  # Aba básica
            self.atualizar_display(self.expressao)
        else:  # Aba científica
            self.atualizar_display_cientifico(self.expressao)
    
    def clicar_botao_cientifico(self, texto):
        # Botões científicos especiais
        if texto == "π":
            self.expressao += "math.pi"
        elif texto == "e":
            self.expressao += "math.e"
        elif texto == "x²":
            if self.expressao:
                self.expressao = f"({self.expressao})**2"
            else:
                self.expressao = "math.pi**2"
        elif texto == "x³":
            if self.expressao:
                self.expressao = f"({self.expressao})**3"
            else:
                return
        elif texto == "xʸ":
            self.expressao += "**"
        elif texto == "√x":
            if self.expressao:
                self.expressao = f"math.sqrt({self.expressao})"
            else:
                self.expressao = "math.sqrt("
        elif texto == "∛x":
            if self.expressao:
                self.expressao = f"({self.expressao})**(1/3)"
            else:
                self.expressao = "math.pow(, 1/3)"
        elif texto == "ʸ√x":
            self.expressao += "**(1/"
        elif texto == "ln":
            self.expressao += "math.log("
        elif texto == "log":
            self.expressao += "math.log10("
        elif texto == "sin":
            self.expressao += "math.sin(" + ("" if self.modo_rad else "math.radians(")
        elif texto == "cos":
            self.expressao += "math.cos(" + ("" if self.modo_rad else "math.radians(")
        elif texto == "tan":
            self.expressao += "math.tan(" + ("" if self.modo_rad else "math.radians(")
        elif texto == "asin":
            if self.modo_rad:
                self.expressao += "math.asin("
            else:
                self.expressao += "math.degrees(math.asin("
        elif texto == "acos":
            if self.modo_rad:
                self.expressao += "math.acos("
            else:
                self.expressao += "math.degrees(math.acos("
        elif texto == "atan":
            if self.modo_rad:
                self.expressao += "math.atan("
            else:
                self.expressao += "math.degrees(math.atan("
        elif texto == "sinh":
            self.expressao += "math.sinh("
        elif texto == "cosh":
            self.expressao += "math.cosh("
        elif texto == "tanh":
            self.expressao += "math.tanh("
        elif texto == "!":
            if self.expressao:
                try:
                    n = eval(self.expressao)
                    if n.is_integer() and n >= 0:
                        self.expressao = str(math.factorial(int(n)))
                    else:
                        messagebox.showerror("Erro", "Fatorial apenas para inteiros não-negativos")
                except:
                    messagebox.showerror("Erro", "Expressão inválida para fatorial")
        elif texto == "1/x":
            if self.expressao:
                self.expressao = f"1/({self.expressao})"
            else:
                return
        elif texto == "mod":
            self.expressao += "%"
        elif texto == "exp":
            self.expressao += "math.exp("
        elif texto == "|x|":
            if self.expressao:
                self.expressao = f"abs({self.expressao})"
            else:
                self.expressao = "abs("
        elif texto == "deg":
            if self.modo_rad:
                self.alternar_modo()
        elif texto == "rad":
            if not self.modo_rad:
                self.alternar_modo()
        elif texto == "+/-":
            if self.expressao:
                try:
                    valor = eval(self.expressao)
                    self.expressao = str(-valor)
                except:
                    if self.expressao.startswith("-"):
                        self.expressao = self.expressao[1:]
                    else:
                        self.expressao = "-" + self.expressao
        elif texto == "2nd":
            # Toggle between primary and secondary functions
            pass
        else:
            # Para botões normais usar o processador normal
            self.processar_botao(texto)
        
        self.atualizar_display_cientifico(self.expressao)
    
    def processar_botao(self, texto):
        # Função comum para processar os botões em ambas as abas
        atual = self.display.get()
        
        if texto == "C":
            # Limpar o display
            self.expressao = ""
            self.atualizar_display("0")
            self.atualizar_display_cientifico("0")
            
        elif texto == "⌫":
            # Apagar o último caracter
            if len(self.expressao) > 0:
                # Verificar se é uma função matemática
                for func in ["math.sin", "math.cos", "math.tan", "math.sqrt", "math.log", "math.log10"]:
                    if self.expressao.endswith(func + "("):
                        self.expressao = self.expressao[:-len(func + "(")]
                        break
                else:
                    self.expressao = self.expressao[:-1]
                    
                if not self.expressao:
                    self.atualizar_display("0")
                    self.atualizar_display_cientifico("0")
                else:
                    self.atualizar_display(self.expressao)
                    self.atualizar_display_cientifico(self.expressao)
                    
        elif texto == "=":
            # Calcular o resultado
            if not self.expressao:
                return
                
            try:
                # Avaliar a expressão
                resultado = eval(self.expressao)
                
                # Verificar se o resultado é um número
                if isinstance(resultado, (int, float)):
                    # Arredondar para evitar problemas de precisão
                    if isinstance(resultado, float):
                        # Usar Decimal para arredondamento preciso
                        resultado = float(Decimal(str(resultado)).quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP))
                    
                    # Adicionar ao histórico
                    entrada = f"{self.expressao} = {resultado}"
                    self.historico.append(entrada)
                    self.lista_historico.insert(0, entrada)
                    
                    # Atualizar o resultado anterior
                    self.resultado_anterior = resultado
                    
                    # Atualizar a expressão e o display
                    self.expressao = str(resultado)
                    self.atualizar_display(self.expressao)
                    self.atualizar_display_cientifico(self.expressao)
                else:
                    messagebox.showerror("Erro", "Resultado inválido")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao calcular: {str(e)}")
                
        else:
            # Adicionar o texto à expressão
            self.expressao += texto
    
    def atualizar_display(self, texto):
        # Atualizar o display da aba básica
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, texto)
        self.display.config(state="readonly")
    
    def atualizar_display_cientifico(self, texto):
        # Atualizar o display da aba científica
        self.display_cient.config(state="normal")
        self.display_cient.delete(0, tk.END)
        self.display_cient.insert(0, texto)
        self.display_cient.config(state="readonly")

# Função principal para iniciar a aplicação
def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = CalculadoraCompleta(root)
    root.mainloop()

if __name__ == "__main__":
    main()