from flask import Blueprint, render_template, request, redirect, flash, session
from supabase_client import supabase
from routes.utils import is_authenticated, is_admin

tipo_cultivo_bp = Blueprint('tipo_cultivo', __name__)

@tipo_cultivo_bp.route('/tipos-cultivo', methods=['GET', 'POST'])
def tipo_cultivo():
    if not is_authenticated() or not is_admin():
        return redirect('/login')

    # Procesar nuevo cultivo si se envió el formulario
    if request.method == 'POST':
        nombre = request.form.get("nombre")
        unidad_id = request.form.get("unidad_id")

        if not nombre or not unidad_id:
            flash("Todos los campos son obligatorios.", "warning")
        else:
            try:
                supabase.table("tipo_cultivo").insert({
                    "nombre": nombre.strip(),
                    "unidad_id": unidad_id
                }).execute()
                flash("✅ Tipo de cultivo agregado correctamente", "success")
                return redirect('/tipo-cultivo')
            except Exception as e:
                flash(f"❌ Error al agregar tipo de cultivo: {str(e)}", "danger")

    # Obtener lista de tipos de cultivo y unidades
    try:
        cultivos_data = supabase.from_("tipo_cultivo").select("id, nombre, unidad_id").execute().data
        unidades_data = supabase.from_("unidades").select("id, nombre").execute().data

        # Asociar nombre de unidad a cada cultivo
        unidades_dict = {str(u['id']): u['nombre'] for u in unidades_data}
        for cultivo in cultivos_data:
            cultivo['unidad_nombre'] = unidades_dict.get(str(cultivo['unidad_id']), 'Sin unidad')

    except Exception as e:
        flash(f"❌ Error al cargar datos: {str(e)}", "danger")
        cultivos_data = []
        unidades_data = []

    return render_template("tipo_cultivo.html", cultivos=cultivos_data, unidades=unidades_data)
