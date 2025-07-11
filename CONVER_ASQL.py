import json

def cargar_mdj(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def construir_indices(data):
    # Índices para buscar entidades y columnas por _id
    entidades = {}
    columnas = {}
    for elem in data.get('ownedElements', []):
        if elem.get('_type') == 'ERDDataModel':
            for entidad in elem.get('ownedElements', []):
                if entidad.get('_type') == 'ERDEntity':
                    entidades[entidad['_id']] = entidad
                    for col in entidad.get('columns', []):
                        columnas[col['_id']] = (entidad['name'], col)
    return entidades, columnas

def extraer_tablas_y_relaciones(data):
    entidades, columnas_idx = construir_indices(data)
    tablas = []
    for entidad in entidades.values():
        nombre_tabla = entidad.get('name')
        columnas = []
        fks = []
        for col in entidad.get('columns', []):
            nombre_col = col.get('name')
            tipo = col.get('type', 'VARCHAR(255)')
            longitud = col.get('length', 0)
            tipo_sql = f"VARCHAR({longitud})" if tipo == 'VARCHAR' and longitud else tipo
            es_pk = col.get('primaryKey', False)
            # Procesar llave foránea si existe
            fk = None
            ref = col.get('referenceTo', {}).get('$ref') if isinstance(col.get('referenceTo'), dict) else None
            if ref and ref in columnas_idx:
                ref_tabla, ref_col = columnas_idx[ref]
                fk = {
                    'columna': nombre_col,
                    'tabla_ref': ref_tabla,
                    'col_ref': ref_col.get('name')
                }
                fks.append(fk)
            columnas.append({
                'name': nombre_col,
                'type': tipo_sql,
                'primaryKey': es_pk
            })
        tablas.append({
            'name': nombre_tabla,
            'columns': columnas,
            'foreignKeys': fks
        })
    return tablas

def generar_sql(tablas):
    sql = ""
    for tabla in tablas:
        sql += f"CREATE TABLE {tabla['name']} (\n"
        columnas_sql = []
        pks = []
        for col in tabla['columns']:
            col_def = f"    {col['name']} {col['type']}"
            columnas_sql.append(col_def)
            if col.get('primaryKey'):
                pks.append(col['name'])
        if pks:
            columnas_sql.append(f"    PRIMARY KEY ({', '.join(pks)})")
        # Llaves foráneas
        for fk in tabla['foreignKeys']:
            columnas_sql.append(
                f"    FOREIGN KEY ({fk['columna']}) REFERENCES {fk['tabla_ref']}({fk['col_ref']})"
            )
        sql += ",\n".join(columnas_sql) + "\n);\n\n"
    return sql

def main():
    archivo = "Untitled.mdj"
    data = cargar_mdj(archivo)
    tablas = extraer_tablas_y_relaciones(data)
    sql = generar_sql(tablas)
    with open("estructura.sql", "w", encoding="utf-8") as f:
        f.write(sql)
    print("Archivo estructura.sql generado con éxito.")

if __name__ == "__main__":
    main()
