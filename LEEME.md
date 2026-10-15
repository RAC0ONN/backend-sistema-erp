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
