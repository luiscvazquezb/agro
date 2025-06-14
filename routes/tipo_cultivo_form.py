# routes/tipo_cultivo_form.py
from flask import Blueprint, render_template, request, redirect, flash, session
from supabase_client import supabase

cultivo_form_bp = Blueprint('cultivo_form', __name__)

@cultivo_form_bp.route('/alta-cultivo', methods=['GET', 'POST'])
def alta_cultivo():
    if 'cliente_id' not in session:
        flash("Sesión expirada. Inicia sesión nuevamente.", "warning")
        return redirect('/')

    cliente_id = session['cliente_id']

    # Obtener variedades e injertos existentes (opcionales)
    variedades = supabase.table("variedades").select("id,nombre").eq("activo", True).execute().data
    injertos = supabase.table("porta_injertos").select("id,nombre").execute().data

    if request.method == 'POST':
        datos = {
            "cliente_id": cliente_id,
            "nombre": request.form.get("nombre"),
            "nombre_cientifico": request.form.get("nombre_cientifico"),
            "nombre_comercial": request.form.get("nombre_comercial"),
            "descripcion": request.form.get("descripcion"),
            "unidad_produccion": request.form.get("unidad_produccion"),
            "categoria": request.form.get("categoria"),
            "ciclo_dias": request.form.get("ciclo_dias"),
            "activo": True
        }

        try:
            # Insertar tipo de cultivo principal
            res = supabase.table("tipo_cultivo").insert(datos).execute()
            cultivo_id = res.data[0]['id']

            # Si hay variedad seleccionada
            variedad_id = request.form.get("variedad_id")
            injerto_id = request.form.get("porta_injerto_id")

            if variedad_id or injerto_id:
                supabase.table("tipo_cultivo_config").insert({
                    "tipo_cultivo_id": cultivo_id,
                    "variedad_id": variedad_id or None,
                    "porta_injerto_id": injerto_id or None
                }).execute()

            flash("Tipo de cultivo registrado con éxito.", "success")
            return redirect("/tipos-cultivo")
        except Exception as e:
            flash(f"Error al guardar: {e}", "danger")

    return render_template("alta_cultivo.html", variedades=variedades, injertos=injertos)
