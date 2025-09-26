import tkinter as tk
from tkinter import ttk
import time, threading
from Model.fifo.Fifo import Fifo
from Model.Processo import Processo
from Model.sjf.Sjf import SJF


class EscalonadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Escalonamento")
        self.root.geometry("700x500")
        self.simulacao_rodando = False
        self._configurar_interface()

    def _configurar_interface(self):
        frm = ttk.Frame(self.root, padding=10);
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Processos (ID, Chegada, Execução):").pack(anchor=tk.W)
        self.campo_processos = tk.Text(frm, height=4)
        self.campo_processos.pack(fill=tk.X, pady=5)
        self.campo_processos.insert(tk.END, "P1,2,15\nP2,4,6\nP3,6,11\nP4,9,8\nP5,11,7")

        alg_frame = ttk.Frame(frm);
        alg_frame.pack(fill=tk.X, pady=5)
        ttk.Label(alg_frame, text="Algoritmo:").pack(side=tk.LEFT)
        self.alg_var = tk.StringVar(value="FIFO")
        for a in ("FIFO", "SJF"): ttk.Radiobutton(alg_frame, text=a, variable=self.alg_var, value=a).pack(side=tk.LEFT,
                                                                                                          padx=5)
        for txt, cmd in (
        ("Executar", self.iniciar_simulacao), ("Parar", self.parar_simulacao), ("Resultados", self.mostrar_resultados)):
            ttk.Button(alg_frame, text=txt, command=cmd).pack(side=tk.LEFT, padx=5)

        info_frame = ttk.Frame(frm);
        info_frame.pack(fill=tk.X, pady=5)
        self.rot_tempo = ttk.Label(info_frame, text="Tempo: 0");
        self.rot_tempo.pack(side=tk.LEFT, padx=10)
        self.rot_exec = ttk.Label(info_frame, text="Executando: Nenhum");
        self.rot_exec.pack(side=tk.LEFT, padx=10)

        ttk.Label(frm, text="Fila:").pack(anchor=tk.W)
        self.canvas_fila = tk.Canvas(frm, height=60, bg="white");
        self.canvas_fila.pack(fill=tk.X, pady=2)

        cols = ("ID", "Chegada", "Execução", "Início", "Fim", "WT", "TT")
        self.tbl = ttk.Treeview(frm, columns=cols, show="headings", height=8)
        for c in cols: self.tbl.heading(c, text=c); self.tbl.column(c, width=60)
        self.tbl.pack(fill=tk.BOTH, expand=True, pady=5)

        ttk.Label(frm, text="Log:").pack(anchor=tk.W)
        self.log = tk.Text(frm, height=6);
        self.log.pack(fill=tk.X)

    def registrar_log(self, msg):
        self.log.insert(tk.END, f"T{getattr(self, 'tempo', 0)}: {msg}\n");
        self.log.see(tk.END)

    def ler_processos(self):
        lst = []
        for l in self.campo_processos.get("1.0", tk.END).strip().split('\n'):
            if l.strip():
                p, at, pt = l.split(',');
                lst.append(Processo(p, int(at), int(pt)))
        return lst

    def iniciar_simulacao(self):
        if self.simulacao_rodando: return
        self.processos = self.ler_processos()
        if not self.processos: return
        self.simulacao_rodando = True;
        self.tbl.delete(*self.tbl.get_children());
        self.log.delete(1.0, tk.END)
        threading.Thread(target=self._simular, daemon=True).start()

    def parar_simulacao(self):
        self.simulacao_rodando = False; self.registrar_log("Parada")

    def _simular(self):
        alg = self.alg_var.get()
        escal = Fifo([Processo(p.get_id(), p.get_tempo_chegada(), p.get_tempo_execucao()) for p in
                      self.processos]) if alg == "FIFO" else SJF(
            [Processo(p.get_id(), p.get_tempo_chegada(), p.get_tempo_execucao()) for p in self.processos])
        res = escal.escalonar()
        for p in self.processos: p.set_estado_processo(
            "Pronto"); p.inicio_execucao = None; p.fim_execucao = None; p.wt = None; p.tt = None

        self.tempo = 0
        for r in res:
            if not self.simulacao_rodando: break
            p = next(x for x in self.processos if x.get_id() == r["id"])
            while self.tempo < r["inicio"] and self.simulacao_rodando: self.tempo += 1; self.root.after(0,
                                                                                                        lambda: self._atualizar()); time.sleep(
                0.2)
            p.set_estado_processo("Executando");
            p.inicio_execucao = r["inicio"];
            self.registrar_log(f"{p.get_id()} iniciou");
            self.root.after(0, lambda: self._atualizar());
            time.sleep(0.3)
            while self.tempo < r["fim"] and self.simulacao_rodando: self.tempo += 1; time.sleep(0.2)
            p.set_estado_processo("Finalizado");
            p.fim_execucao = r["fim"];
            p.wt = r["wt"];
            p.tt = r["tt"]
            self.registrar_log(f"{p.get_id()} finalizado (WT:{r['wt']}, TT:{r['tt']})");
            self.root.after(0, lambda: self._atualizar());
            time.sleep(0.3)
        self.simulacao_rodando = False;
        self.registrar_log("Fim")

    def _atualizar(self):
        self.rot_tempo.config(text=f"Tempo: {self.tempo}")
        self.rot_exec.config(
            text=f"Executando: {next((p.get_id() for p in self.processos if p.get_estado_processo() == 'Executando'), 'Nenhum')}")
        self.canvas_fila.delete("all");
        x = 10;
        max_l = 100
        for p in self.processos:
            if p.get_estado_processo() != "Finalizado":
                cor = "green" if p.get_estado_processo() == "Executando" else "blue"
                prog = ((min(self.tempo,
                             p.fim_execucao if p.fim_execucao else self.tempo) - p.inicio_execucao) / p.get_tempo_execucao()) if p.inicio_execucao is not None else 0
                prog = max(0, min(prog, 1));
                larg = int(max_l * prog)
                self.canvas_fila.create_rectangle(x, 20, x + max_l, 40, fill="lightgray")
                self.canvas_fila.create_rectangle(x, 20, x + larg, 40, fill=cor)
                self.canvas_fila.create_text(x + max_l // 2, 30, text=p.get_id(), fill="white");
                x += max_l + 10
        self.tbl.delete(*self.tbl.get_children())
        for p in self.processos:
            self.tbl.insert("", tk.END, values=(
            p.get_id(), p.get_tempo_chegada(), p.get_tempo_execucao(), p.inicio_execucao or "-", p.fim_execucao or "-",
            p.wt or "-", p.tt or "-"))

    def mostrar_resultados(self):
        proc = self.ler_processos()
        if not proc: return
        fifo_res = Fifo([Processo(p.get_id(), p.get_tempo_chegada(), p.get_tempo_execucao()) for p in proc]).escalonar()
        sjf_res = SJF([Processo(p.get_id(), p.get_tempo_chegada(), p.get_tempo_execucao()) for p in proc]).escalonar()
        win = tk.Toplevel(self.root);
        win.title("Resultados");
        win.geometry("600x400");
        nb = ttk.Notebook(win);
        nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for nome, res in (("FIFO", fifo_res), ("SJF", sjf_res)):
            f = ttk.Frame(nb);
            nb.add(f, text=nome);
            self._tabela_resultados(f, res)

    def _tabela_resultados(self, parent, res):
        cols = ("Processo", "AT", "PT", "Início", "Fim", "WT", "TT");
        tbl = ttk.Treeview(parent, columns=cols, show="headings", height=10);
        tbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for c in cols: tbl.heading(c, text=c); tbl.column(c, width=70)
        for r in res: tbl.insert("", tk.END,
                                 values=(r["id"], r["chegada"], r["execucao"], r["inicio"], r["fim"], r["wt"], r["tt"]))
        ttk.Frame(parent).pack(fill=tk.X);
        ttk.Label(parent, text=f"WT Médio: {sum(r['wt'] for r in res) / len(res):.1f}").pack(anchor=tk.W)
        ttk.Label(parent, text=f"TT Médio: {sum(r['tt'] for r in res) / len(res):.1f}").pack(anchor=tk.W)


if __name__ == "__main__":
    root = tk.Tk();
    app = EscalonadorGUI(root);
    root.mainloop()
