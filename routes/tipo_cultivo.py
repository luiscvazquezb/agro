from flask import Blueprint, render_template, request, redirect, flash, session
from supabase_client import supabase
from routes.utils import is_authenticated, is_admin

tipo_cultivo_bp = Blueprint('tipo_cultivo', __name__)

@tipo_cultivo_bp.route('/tipo-cultivo', methods=['GET', 'POST'])
def tipo_cultivo():
    if not is_authenticated() or not is_admin():
        return redirect('/login')

    # Procesar nuevo cultivo
    if request.method == 'POST':
        nombre = request.form.get("nombre")
        unidad_id = request.form.get("unidad_id")
        if nombre and unidad_id:
            try:
                supabase.table("tipo_cultivo").insert({
                    "nombre": nombre,
                    "unidad_id": unidad_id
                }).execute()
                flash("Tipo de cultivo agregado correctamente", "success")
            except Exception as e:
                flash(f"Error al agregar tipo de cultivo: {str(e)}", "danger")
        else:
            flash("Todos los campos son obligatorios.", "warning")

    # Cargar tipos de cultivo
    try:
        cultivos_data = supabase.from_("tipo_cultivo").select("id, nombre, unidad_id").execute().data
        unidades_data = supabase.from_("unidades").select("id, nombre").execute().data
        unidades_dict = {str(u['id']): u['nombre'] for u in unidades_data}

        for c in cultivos_data:
            c['unidad_nombre'] = unidades_dict.get(str(c['unidad_id']), 'Desconocida')

    except Exception as e:
        cultivos_data = []
        unidades_data = []
        flash(f"Error al cargar datos: {str(e)}", "danger")

    return render_template("tipo_cultivo.html", cultivos=cultivos_data, unidades=unidades_data)
