from flask import Blueprint, render_template, request, redirect, flash, session
from supabase_client import supabase

variedades_bp = Blueprint('variedades', __name__)

@variedades_bp.route('/variedades', methods=['GET', 'POST'])
def ver_variedades():
    if 'cliente' not in session:
        return redirect('/')

    tipo_id = request.args.get('tipo_id')
    if not tipo_id:
        flash("Falta el parámetro 'tipo_id' en la URL.", "warning")
        return redirect('/menu')

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        try:
            supabase.table("variedades").insert({
                "tipo_cultivo_id": tipo_id,
                "nombre": nombre,
                "descripcion": descripcion
            }).execute()
            flash("Variedad registrada exitosamente.", "success")
        except Exception as e:
            flash(f"Error al registrar: {e}", "danger")

    resultado = supabase.table("variedades").select("*").eq("tipo_cultivo_id", tipo_id).order("created_at").execute()
    variedades = resultado.data if resultado.data else []

    tipo = supabase.table("tipo_cultivo").select("nombre_tipo_cultivo").eq("id", tipo_id).execute()
    nombre_tipo = tipo.data[0]["nombre_tipo_cultivo"] if tipo.data else "Tipo desconocido"

    return render_template("variedades.html", variedades=variedades, tipo_id=tipo_id, nombre_tipo=nombre_tipo)
