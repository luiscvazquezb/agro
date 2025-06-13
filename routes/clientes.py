from flask import Blueprint, render_template, request, redirect, flash, session, abort
from routes.utils import is_authenticated, is_admin
from supabase_client import supabase

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes')
def ver_clientes():
    if not session.get('autenticado'):
        return redirect('/login')

    buscar = request.args.get('buscar', '').strip().lower()
    try:
        resultado = supabase.table("clientes").select("*").order("fecha_alta", desc=True).execute()
        clientes = resultado.data if resultado.data else []

        if buscar:
            clientes = [c for c in clientes if buscar in c['nombre'].lower()]
    except Exception as e:
        clientes = []
        flash(f"Error al cargar clientes: {str(e)}", "danger")

    return render_template("clientes.html", clientes=clientes)


@clientes_bp.route('/nuevo-cliente', methods=['GET', 'POST'])
def nuevo_cliente():
    if not session.get('es_admin'):
        return redirect('/menu')

    if request.method == 'POST':
        datos = {
            "nombre": request.form.get("nombre"),
            "representante": request.form.get("representante"),
            "telefono": request.form.get("telefono"),
            "whatsapp": request.form.get("whatsapp"),
            "telegram": request.form.get("telegram"),
            "correo": request.form.get("correo"),
            "logo_url": request.form.get("logo_url"),
            "colorhex": request.form.get("colorhex"),
            "pagina": request.form.get("pagina"),
            "password": request.form.get("password"),
            "username": request.form.get("username")
        }
        try:
            supabase.table("clientes").insert(datos).execute()
            flash("Cliente registrado exitosamente", "success")
        except Exception as e:
            flash(f"Error al registrar cliente: {str(e)}", "danger")

        return redirect('/nuevo-cliente')

    return render_template("nuevo_cliente.html")


@clientes_bp.route('/editar-cliente/<uuid:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if not session.get('autenticado'):
        return redirect('/login')

    if request.method == 'POST':
        datos = {
            "nombre": request.form.get("nombre"),
            "representante": request.form.get("representante"),
            "telefono": request.form.get("telefono"),
            "whatsapp": request.form.get("whatsapp"),
            "telegram": request.form.get("telegram"),
            "correo": request.form.get("correo"),
            "logo_url": request.form.get("logo_url"),
            "colorhex": request.form.get("colorhex"),
            "pagina": request.form.get("pagina"),
            "password": request.form.get("password"),
            "username": request.form.get("username")
        }
        try:
            supabase.table("clientes").update(datos).eq("id", str(id)).execute()
            flash("Cliente actualizado exitosamente", "success")
            return redirect('/clientes')
        except Exception as e:
            flash(f"Error al actualizar cliente: {str(e)}", "danger")

    resultado = supabase.table("clientes").select("*").eq("id", str(id)).single().execute()
    if resultado.data:
        return render_template("editar_cliente.html", cliente=resultado.data)
    else:
        abort(404)
