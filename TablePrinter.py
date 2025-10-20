from tabulate import tabulate

class TablePrinter:
    @staticmethod
    def afficher_table(df, colonnes, center_cols=None):
        if center_cols is None:
            center_cols = []
        table = []
        headers = df[colonnes].columns.tolist()
        for _, row in df[colonnes].iterrows():
            row_vals = []
            for col in colonnes:
                val = str(row[col])
                if col in center_cols:
                    val = val.center(20)
                row_vals.append(val)
            table.append(row_vals)
        print(tabulate(table, headers=headers, tablefmt="fancy_grid", stralign="center"))
