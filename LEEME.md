# Backend Sistema ERP

## Para correrlo
1. Crear y activar el entorno virtual (la carpeta `venv` no se sube a GitHub):
   - `python -m venv venv`
   - Windows: `venv\Scripts\activate`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Copiar `.env.example` como `.env` y poner tu contraseña de PostgreSQL.
4. Si no tienes la base: crear `sistema_erp_db` en pgAdmin y ejecutar `sql/script_bd.sql`.
5. `python manage.py runserver`

El front (Angular) corre en `http://localhost:4200` y ya tiene permiso (CORS) para llamar al back.

## Login
`POST /api/usuarios/login/`

Se puede entrar con el correo o con el nombre de usuario:
```json
{ "correo": "jperez@empresa.com", "contrasenia": "Prueba123" }
```
Respuestas:
- 200: correcto, devuelve `data` con id_usuario, nombre, rol, estado y un `token`
- 401: correo o contraseña incorrectos
- 403: el usuario está suspendido o retirado

## Seguridad y permisos
Después del login, el front manda el token en cada petición (`Authorization: Bearer <token>`).
Sin token responde 401. La sesión dura 12 horas, y si suspenden o retiran al usuario pierde el acceso de una vez.

| Acción | Administrador | Auxiliar administrativo | Vendedor |
|---|---|---|---|
| Ver usuarios y auditoría | Sí | Sí | No |
| Crear / editar / cambiar estado de usuarios | No | Sí | No |
| Ver productos inactivos | Sí | No | No |
| Crear / editar productos, entradas y salidas | Sí | Sí | No |
| Activar / inactivar / eliminar productos | Sí | No | No |

## Reglas que valida el back
- Usuario nuevo: queda siempre en estado **Contratado**. El sistema genera una contraseña aleatoria y la manda al correo.
  Sin correo configurado en el `.env`, la contraseña sale en la consola del back.
- Los usuarios no se eliminan. Se retiran cambiando el estado, así no se pierde el historial.
- El documento (tipo y número) no se puede modificar.
- Nadie puede cambiar su propio rol ni su propio estado.
- Correo con formato válido y terminación real (`.coml`, `.con`, etc. no pasan). Correo, usuario y documento no se repiten.
- Producto: el código lo genera el sistema según la categoría (CAL-001, BOL-001...).
- El stock solo cambia con entradas y salidas.
- Un producto solo se inactiva con 0 unidades.
- Un producto solo se elimina si tiene 0 unidades y ningún movimiento.
- Los errores llegan como `{"message": "...", "errores": {"campo": "mensaje"}}` para mostrarlos debajo de cada campo.

## Endpoints nuevos
- `GET /api/usuarios/perfil/`: datos del usuario de la sesión
- `POST /api/usuarios/cambiar-contrasenia/`: `{contrasenia_actual, contrasenia_nueva, confirmacion}`
- `GET /api/inventario/categorias/`
- Se quitó `DELETE /api/usuarios/eliminar/<id>/`
