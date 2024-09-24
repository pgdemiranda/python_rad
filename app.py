import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend import read_students, create_student, delete_students, update_student
import pandas as pd

class radapp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicação de Gestão de Alunos")
        self.create_table() 
        self.create_buttons()

    def create_table(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frame, columns=(
            'id', 'matricula', 'cpf', 'nome', 'idade', 'email', 'curso',
            'ano_conclusao', 'periodo_conclusao', 'situacao', 
            'telefone_celular', 'sexo', 'raca'
        ), show='headings')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('matricula', text='Matrícula')
        self.tree.heading('cpf', text='CPF')
        self.tree.heading('nome', text='Nome')
        self.tree.heading('idade', text='Idade')
        self.tree.heading('email', text='Email')
        self.tree.heading('curso', text='Curso')
        self.tree.heading('ano_conclusao', text='Ano Conclusão')
        self.tree.heading('periodo_conclusao', text='Período Conclusão')
        self.tree.heading('situacao', text='Situação')
        self.tree.heading('telefone_celular', text='Telefone Celular')
        self.tree.heading('sexo', text='Sexo')
        self.tree.heading('raca', text='Raça')
        
        scrollbar_vertical = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_horizontal = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)
        
        scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        btn_listar = tk.Button(button_frame, text="Listar", command=self.populate_table)
        btn_cadastrar = tk.Button(button_frame, text="Cadastrar", command=self.open_register_window)
        btn_alterar = tk.Button(button_frame, text="Alterar", command=self.open_update_window)
        btn_excluir = tk.Button(button_frame, text="Excluir", command=self.delete_selected)
        btn_exportar = tk.Button(button_frame, text="Exportar", command=self.open_export_window)

        btn_listar.grid(row=0, column=0, padx=10)
        btn_cadastrar.grid(row=0, column=1, padx=10)
        btn_alterar.grid(row=0, column=2, padx=10)
        btn_excluir.grid(row=0, column=3, padx=10)
        btn_exportar.grid(row=0, column=4, padx=10)

    def populate_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        students = read_students()
        for student in students:
            self.tree.insert('', tk.END, values=student)

    def open_register_window(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Cadastrar Aluno")
        
        fields = {
            'Matrícula': tk.StringVar(),
            'CPF': tk.StringVar(),
            'Nome': tk.StringVar(),
            'Idade': tk.IntVar(),
            'Email': tk.StringVar(),
            'Curso': tk.StringVar(),
            'Ano Conclusão': tk.IntVar(),
            'Período Conclusão': tk.IntVar(),
            'Situação': tk.StringVar(),
            'Telefone Celular': tk.StringVar(),
            'Sexo': tk.StringVar(),
            'Raça': tk.StringVar()
        }

        for idx, (label, var) in enumerate(fields.items()):
            tk.Label(register_window, text=label).grid(row=idx, column=0, padx=10, pady=5)
            
            if label == 'Sexo':
                ttk.Combobox(register_window, textvariable=var, values=['M', 'F']).grid(row=idx, column=1, padx=10, pady=5)
            elif label == 'Raça':
                ttk.Combobox(register_window, textvariable=var, values=['Branca', 'Indígena', 'Negra', 'Parda', 'Amarela']).grid(row=idx, column=1, padx=10, pady=5)
            elif label == 'Curso':
                ttk.Combobox(register_window, textvariable=var, values=['IDOS', 'CIRU', 'UTI', 'NEO']).grid(row=idx, column=1, padx=10, pady=5)
            elif label == 'Situação':
                ttk.Combobox(register_window, textvariable=var, values=['Ativo', 'Concluinte']).grid(row=idx, column=1, padx=10, pady=5)
            else:
                tk.Entry(register_window, textvariable=var).grid(row=idx, column=1, padx=10, pady=5)

        btn_save = tk.Button(register_window, text="Salvar", command=lambda: self.save_student(fields, register_window))
        btn_save.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def save_student(self, fields, window):
        values = {label: var.get() for label, var in fields.items()}
        
        create_student(
            values['Matrícula'], values['CPF'], values['Nome'], values['Idade'], values['Email'], 
            values['Curso'], values['Ano Conclusão'], values['Período Conclusão'], values['Situação'],
            values['Telefone Celular'], values['Sexo'], values['Raça']
        )
        window.destroy()
        self.populate_table()

    def open_update_window(self):
        selected_items = self.tree.selection()
        if len(selected_items) != 1:
            messagebox.showwarning("Aviso", "Selecione apenas um aluno para alterar.")
            return
        
        selected_item = selected_items[0]
        student_data = self.tree.item(selected_item, 'values')

        update_window = tk.Toplevel(self.root)
        update_window.title("Alterar Aluno")

        fields = {
            'Matrícula': tk.StringVar(value=student_data[1]),
            'CPF': tk.StringVar(value=student_data[2]),
            'Nome': tk.StringVar(value=student_data[3]),
            'Idade': tk.IntVar(value=student_data[4]),
            'Email': tk.StringVar(value=student_data[5]),
            'Curso': tk.StringVar(value=student_data[6]),
            'Ano Conclusão': tk.IntVar(value=student_data[7]),
            'Período Conclusão': tk.IntVar(value=student_data[8]),
            'Situação': tk.StringVar(value=student_data[9]),
            'Telefone Celular': tk.StringVar(value=student_data[10]),
            'Sexo': tk.StringVar(value=student_data[11]),
            'Raça': tk.StringVar(value=student_data[12])
        }

        for idx, (label, var) in enumerate(fields.items()):
            tk.Label(update_window, text=label).grid(row=idx, column=0, padx=10, pady=5)
            
            if label == 'Sexo':
                ttk.Combobox(update_window, textvariable=var, values=['M', 'F']).grid(row=idx, column=1, padx=10, pady=5)
            elif label == 'Raça':
                ttk.Combobox(update_window, textvariable=var, values=['Branca', 'Indígena', 'Negra', 'Parda', 'Amarela']).grid(row=idx, column=1, padx=10, pady=5)
            elif label == 'Curso':
                ttk.Combobox(update_window, textvariable=var, values=['IDOS', 'CIRU', 'UTI', 'NEO']).grid(row=idx, column=1, padx=10, pady=5)
            elif label == 'Situação':
                ttk.Combobox(update_window, textvariable=var, values=['Ativo', 'Concluinte']).grid(row=idx, column=1, padx=10, pady=5)
            else:
                tk.Entry(update_window, textvariable=var).grid(row=idx, column=1, padx=10, pady=5)

        btn_save = tk.Button(update_window, text="Salvar", command=lambda: self.save_update(student_data[0], fields, update_window))
        btn_save.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def save_update(self, student_id, fields, window):
        values = {label: var.get() for label, var in fields.items()}
        
        if messagebox.askyesno("Confirmar", "Tem certeza de que deseja alterar os dados do aluno?"):
            update_student(
                student_id, values['Matrícula'], values['CPF'], values['Nome'], values['Idade'], values['Email'],
                values['Curso'], values['Ano Conclusão'], values['Período Conclusão'], values['Situação'],
                values['Telefone Celular'], values['Sexo'], values['Raça']
            )
            window.destroy()
            self.populate_table()

    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Nenhum aluno selecionado.")
            return
        
        # Confirmação de exclusão
        if not messagebox.askyesno("Confirmar", "Tem certeza de que deseja excluir os alunos selecionados?"):
            return
        
        ids = [int(self.tree.item(item, 'values')[0]) for item in selected_items]
        delete_students(ids)
        self.populate_table()

    def open_export_window(self):
        export_window = tk.Toplevel(self.root)
        export_window.title("Exportar Lista de Alunos")

        tk.Label(export_window, text="Escolha o formato do arquivo:").pack(padx=10, pady=10)

        format_var = tk.StringVar(value="CSV")
        tk.Radiobutton(export_window, text="CSV", variable=format_var, value="CSV").pack(anchor="w", padx=10)
        tk.Radiobutton(export_window, text="Excel", variable=format_var, value="Excel").pack(anchor="w", padx=10)

        button_frame = tk.Frame(export_window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Salvar", command=lambda: self.save_export(format_var.get(), export_window)).pack(side="left", padx=10)
        tk.Button(button_frame, text="Cancelar", command=export_window.destroy).pack(side="right", padx=10)

    def save_export(self, file_format, window):
        # Função para salvar o arquivo exportado
        file_path = filedialog.asksaveasfilename(
            title="Salvar Arquivo",
            defaultextension=f".{file_format.lower()}",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")],
            initialfile=f"alunos.{file_format.lower()}"
        )

        if not file_path:
            return

        students = read_students()
        df = pd.DataFrame(students, columns=[
            "id", "matricula", "cpf", "nome", "idade", "email", "curso",
            "ano_conclusao", "periodo_conclusao", "situacao", 
            "telefone_celular", "sexo", "raca"
        ])

        try:
            if file_format == "CSV":
                df.to_csv(file_path, index=False)
            elif file_format == "Excel":
                df.to_excel(file_path, index=False)

            messagebox.showinfo("Exportar", "Dados exportados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao Exportar", f"Ocorreu um erro ao salvar o arquivo: {e}")
        
        window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = radapp(root)
    root.mainloop()