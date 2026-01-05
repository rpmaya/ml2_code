# Anexo: Guías de Instalación y Configuración de n8n

> **Nota:** Este documento es un anexo de la Unidad 4: Automatización con n8n y Agentes de IA. Contiene las instrucciones técnicas detalladas para instalación y configuración que complementan el contenido teórico de la unidad.

---

## Tabla de Contenidos

1. [Instalación local con npx](#1-instalación-local-con-npx)
2. [Despliegue en Koyeb desde GitHub](#2-despliegue-en-koyeb-desde-github)
3. [Configuración de credenciales OAuth2 para Google](#3-configuración-de-credenciales-oauth2-para-google)
4. [Memoria persistente con PostgreSQL (Supabase)](#4-memoria-persistente-con-postgresql-supabase)
5. [Solución de problemas comunes](#5-solución-de-problemas-comunes)

---

## 1. Instalación local con npx

La forma más rápida de probar n8n es ejecutarlo localmente usando Node.js. Esta opción es perfecta para el desarrollo y aprendizaje.

### Requisitos previos

- **Node.js versión 18 o superior** instalado
- **npm** (incluido con Node.js)

### Pasos de instalación

#### Paso 1: Verificar Node.js instalado

Abre una terminal y ejecuta:

```bash
node --version
# Debería mostrar v18.x.x o superior
```

Si no tienes Node.js instalado, descárgalo desde [nodejs.org](https://nodejs.org/).

#### Paso 2: Ejecutar n8n con npx

```bash
npx n8n
```

Este comando descarga y ejecuta n8n automáticamente. La primera vez tardará unos minutos en descargar las dependencias.

#### Paso 3: Acceder a la interfaz

Una vez iniciado, verás un mensaje indicando la URL de acceso:

```
n8n ready on 0.0.0.0, port 5678
```

Abre tu navegador y accede a: **http://localhost:5678**

#### Paso 4: Crear cuenta de administrador

La primera vez que accedas, n8n te pedirá crear una cuenta de administrador. Esta cuenta es local y solo existe en tu instalación.

### Comandos útiles

```bash
# Ejecutar n8n en segundo plano
npx n8n start

# Ejecutar con un túnel para acceso externo (útil para webhooks)
npx n8n start --tunnel

# Especificar puerto diferente
npx n8n start --port 8080

# Ver ayuda de comandos disponibles
npx n8n --help
```

### ⚠️ Nota importante sobre webhooks

Al ejecutar n8n localmente, los webhooks **no serán accesibles desde Internet**. Para pruebas con servicios externos como Telegram, necesitarás:

- Usar la opción `--tunnel` (crea un túnel temporal)
- O desplegar en un servidor accesible (ver sección 2)

### Persistencia de datos

Por defecto, n8n guarda los datos en:
- **Linux/Mac:** `~/.n8n/`
- **Windows:** `%USERPROFILE%\.n8n\`

Si eliminas esta carpeta, perderás todos los workflows y credenciales.

---

## 2. Despliegue en Koyeb desde GitHub

Para tener n8n accesible desde Internet de forma gratuita, podemos desplegarlo en **Koyeb**, una plataforma de hosting que ofrece un tier gratuito generoso.

### Paso 1: Preparar el repositorio

1. Ve a [https://github.com/n8n-io/n8n](https://github.com/n8n-io/n8n)
2. Haz clic en **Fork** para copiar el repositorio a tu cuenta de GitHub
3. Espera a que se complete el fork (puede tardar unos segundos)

### Paso 2: Crear cuenta en Koyeb

1. Accede a [https://www.koyeb.com/](https://www.koyeb.com/)
2. Regístrate con tu cuenta de **GitHub** (recomendado) o email
3. Completa el proceso de verificación de email
4. Opcionalmente, añade un método de pago (no se cobra en el tier gratuito)

### Paso 3: Crear el servicio

1. En el dashboard de Koyeb, haz clic en **Create Service**
2. Selecciona **Web Service**
3. En la sección "Deployment method", selecciona **GitHub**
4. Conecta tu cuenta de GitHub si no lo has hecho
5. Selecciona el repositorio forkeado de n8n

### Paso 4: Configurar el servicio

Configura los siguientes parámetros:

| Parámetro | Valor |
|-----------|-------|
| **Name** | `n8n` (o el nombre que prefieras) |
| **Region** | Frankfurt (o la más cercana a ti) |
| **Instance type** | Free tier |
| **Port** | 8000 |

### Paso 5: Variables de entorno

En la sección "Environment Variables", añade las siguientes variables:

```
N8N_PORT=8000
NODE_OPTIONS=--max_old_space_size=4096
N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false
N8N_RUNNERS_ENABLED=true
WEBHOOK_URL=https://tu-subdominio.koyeb.app/
```

> **Importante:** Reemplaza `tu-subdominio` con el subdominio que Koyeb te asigne después del despliegue (lo verás en el paso 7).

### Paso 6: Desplegar

1. Haz clic en **Deploy**
2. Espera a que el despliegue se complete (puede tardar 5-10 minutos la primera vez)
3. Verás el progreso en los logs de la aplicación

### Paso 7: Obtener la URL

Una vez completado el despliegue, Koyeb te proporcionará una URL como:

```
https://n8n-tu-usuario.koyeb.app/
```

### Paso 8: Configuración inicial

1. Accede a la URL proporcionada
2. Añade `/setup` al final: `https://tu-app.koyeb.app/setup`
3. Crea tu cuenta de administrador
4. ¡Listo para usar!

### Paso 9: Actualizar WEBHOOK_URL

Ahora que conoces tu URL real:

1. Ve a Settings → Environment Variables en Koyeb
2. Actualiza `WEBHOOK_URL` con tu URL real: `https://n8n-tu-usuario.koyeb.app/`
3. Redespliega el servicio

### Consideraciones del tier gratuito

| Aspecto | Limitación |
|---------|------------|
| **Instancias** | 1 instancia gratuita |
| **RAM** | 512 MB |
| **CPU** | Compartida |
| **Sleep** | La app puede "dormirse" tras inactividad |
| **Bandwidth** | 100 GB/mes |

Para uso en producción real, considera actualizar a un plan de pago o usar n8n Cloud.

---

## 3. Configuración de credenciales OAuth2 para Google

Este proceso es necesario para conectar n8n con servicios de Google como Gmail, Google Drive, Google Sheets, Google Calendar, etc.

### Paso 1: Crear proyecto en Google Cloud

1. Accede a [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Si es tu primera vez, acepta los términos de servicio
3. Haz clic en el selector de proyectos (parte superior)
4. Clic en **"Nuevo Proyecto"**
5. Nombre del proyecto: `n8n-integraciones` (o similar)
6. Haz clic en **"Crear"**
7. Espera a que se cree y **selecciona el proyecto**

### Paso 2: Configurar pantalla de consentimiento OAuth

1. En el menú lateral, ve a **APIs y servicios → Pantalla de consentimiento OAuth**
2. Selecciona **"Externo"** como tipo de usuario
3. Haz clic en **"Crear"**

Completa la información requerida:

| Campo | Valor |
|-------|-------|
| **Nombre de la app** | n8n Automations |
| **Correo de asistencia** | Tu email |
| **Logo** | (opcional) |
| **Página principal** | (dejar vacío o tu web) |
| **Correo del desarrollador** | Tu email |

4. Haz clic en **"Guardar y continuar"**
5. En "Alcances" (Scopes), haz clic en **"Guardar y continuar"** (sin añadir nada)
6. En "Usuarios de prueba", haz clic en **"+ Add Users"**
7. Añade tu email de Google
8. Haz clic en **"Guardar y continuar"**
9. Revisa el resumen y haz clic en **"Volver al panel"**

### Paso 3: Crear credenciales OAuth2

1. En el menú lateral, ve a **APIs y servicios → Credenciales**
2. Haz clic en **"+ Crear credenciales"**
3. Selecciona **"ID de cliente OAuth"**

Configura:

| Campo | Valor |
|-------|-------|
| **Tipo de aplicación** | Aplicación web |
| **Nombre** | n8n OAuth Client |

4. En **"URIs de redirección autorizados"**, haz clic en **"+ Añadir URI"**

5. Añade la URI correspondiente a tu instalación:

| Instalación | URI de redirección |
|-------------|-------------------|
| **n8n local** | `http://localhost:5678/rest/oauth2-credential/callback` |
| **n8n en Koyeb** | `https://tu-app.koyeb.app/rest/oauth2-credential/callback` |
| **n8n Cloud** | `https://oauth.n8n.cloud/oauth2/callback` |

6. Haz clic en **"Crear"**

7. **¡IMPORTANTE!** Se mostrarán tus credenciales:
   - **Client ID:** `xxxx.apps.googleusercontent.com`
   - **Client Secret:** `GOCSPX-xxxx`

8. **Guarda estos valores de forma segura.** Los necesitarás en n8n.

### Paso 4: Habilitar las APIs necesarias

1. Ve a **APIs y servicios → Biblioteca**
2. Busca y habilita las APIs que necesites:

| API | Uso |
|-----|-----|
| **Gmail API** | Enviar/recibir emails |
| **Google Drive API** | Acceso a archivos en Drive |
| **Google Sheets API** | Leer/escribir hojas de cálculo |
| **Google Calendar API** | Gestionar eventos |
| **Google Docs API** | Crear/editar documentos |

Para habilitar cada una:
1. Busca el nombre de la API
2. Haz clic en el resultado
3. Haz clic en **"Habilitar"**

### Paso 5: Configurar en n8n

1. En n8n, ve a **Credentials** (panel lateral izquierdo)
2. Haz clic en **"+ Add Credential"**
3. Busca **"Google OAuth2 API"** (o el servicio específico como "Gmail OAuth2")
4. Introduce:
   - **Client ID:** El que copiaste en el paso 3
   - **Client Secret:** El que copiaste en el paso 3
5. Haz clic en **"Sign in with Google"**
6. Selecciona tu cuenta de Google
7. Autoriza los permisos solicitados
8. Si todo es correcto, verás **"Account connected"**

### Solución de errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "Access blocked: This app's request is invalid" | URI de redirección incorrecta | Verifica que la URI en Google Cloud coincide exactamente con la de tu n8n |
| "Error 403: access_denied" | Usuario no está en lista de prueba | Añade tu email en "Usuarios de prueba" de la pantalla de consentimiento |
| "This app isn't verified" | App en modo prueba | Normal si no has publicado la app. Haz clic en "Continue" → "Go to app (unsafe)" |
| "API not enabled" | API no habilitada | Ve a la Biblioteca de APIs y habilita la API correspondiente |

---

## 4. Memoria persistente con PostgreSQL (Supabase)

Para producción, necesitamos memoria que persista entre reinicios de n8n. Supabase ofrece PostgreSQL gestionado con un tier gratuito generoso.

### Paso 1: Crear proyecto en Supabase

1. Accede a [https://supabase.com/](https://supabase.com/)
2. Haz clic en **"Start your project"**
3. Regístrate con GitHub (recomendado) o email
4. Haz clic en **"New Project"**

Configura el proyecto:

| Campo | Valor |
|-------|-------|
| **Organization** | Tu organización (crear si no tienes) |
| **Project name** | `n8n-memory` |
| **Database password** | Genera una contraseña segura y **guárdala** |
| **Region** | La más cercana a tu servidor n8n |
| **Pricing Plan** | Free (suficiente para desarrollo) |

5. Haz clic en **"Create new project"**
6. Espera 2-3 minutos a que se aprovisione

### Paso 2: Obtener credenciales de conexión

1. Una vez creado, ve a **Project Settings** (icono de engranaje)
2. En el menú lateral, haz clic en **Database**
3. Haz clic en **"Connect"** (botón verde)
4. Selecciona la pestaña **"ORMs"** o **"Connection string"**

Encontrarás los siguientes datos:

| Parámetro | Ejemplo |
|-----------|---------|
| **Host** | `aws-0-eu-west-2.pooler.supabase.com` |
| **Port** | `5432` |
| **Database** | `postgres` |
| **User** | `postgres.abcd1234` |
| **Password** | La que definiste al crear el proyecto |

### Paso 3: Configurar en n8n

1. En tu workflow, selecciona el nodo **AI Agent**
2. Haz clic en **"+ Memory"**
3. Selecciona **"Postgres Chat Memory"**
4. Haz clic en **"Create New Credential"**

Completa los campos:

| Campo | Valor |
|-------|-------|
| **Host** | `aws-0-eu-west-2.pooler.supabase.com` (tu host de Supabase) |
| **Database** | `postgres` |
| **User** | `postgres.abcd1234` (tu usuario de Supabase) |
| **Password** | Tu contraseña de base de datos |
| **Port** | `5432` |
| **SSL** | Activar (Require) |

5. Haz clic en **"Test Connection"** para verificar
6. Si es exitoso, haz clic en **"Save"**

### Paso 4: Configurar Session ID

En el nodo de memoria, configura el Session ID:

```
Session ID Source: Define Below
Session ID: {{ $json.sessionId }}
```

O para usar el ID del chat de n8n automáticamente:
```
Session ID Source: Connected Chat Trigger
```

### Paso 5: Verificar funcionamiento

1. Ejecuta el workflow y envía algunos mensajes al agente
2. En Supabase, ve a **Table Editor**
3. Verás una tabla `n8n_chat_histories` con los mensajes guardados

### Estructura de la tabla creada automáticamente

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | SERIAL | ID único del mensaje |
| `session_id` | VARCHAR | Identificador de la conversación |
| `message` | JSONB | Contenido del mensaje |
| `type` | VARCHAR | "human" o "ai" |
| `created_at` | TIMESTAMP | Fecha y hora del mensaje |

### Consultas útiles en Supabase

```sql
-- Ver todas las conversaciones
SELECT DISTINCT session_id, 
       MIN(created_at) as inicio,
       MAX(created_at) as fin,
       COUNT(*) as mensajes
FROM n8n_chat_histories
GROUP BY session_id
ORDER BY inicio DESC;

-- Ver mensajes de una conversación específica
SELECT type, message, created_at
FROM n8n_chat_histories
WHERE session_id = 'ID_DE_SESION'
ORDER BY created_at;

-- Limpiar conversaciones antiguas (más de 30 días)
DELETE FROM n8n_chat_histories
WHERE created_at < NOW() - INTERVAL '30 days';
```

---

## 5. Solución de problemas comunes

### Problemas de instalación local

| Problema | Solución |
|----------|----------|
| `npx: command not found` | Instala Node.js desde [nodejs.org](https://nodejs.org/) |
| `EACCES: permission denied` | En Linux/Mac: `sudo chown -R $(whoami) ~/.npm` |
| Puerto 5678 ocupado | Usa `npx n8n start --port 8080` |
| n8n muy lento | Aumenta memoria: `NODE_OPTIONS="--max-old-space-size=4096" npx n8n` |

### Problemas de Koyeb

| Problema | Solución |
|----------|----------|
| Build fails | Verifica que el fork está actualizado |
| App se duerme | Normal en tier gratuito. Considera plan de pago para producción |
| Webhooks no funcionan | Verifica que WEBHOOK_URL tiene tu URL correcta |

### Problemas de OAuth2 Google

| Problema | Solución |
|----------|----------|
| "redirect_uri_mismatch" | La URI en Google Cloud debe coincidir EXACTAMENTE con la de n8n |
| "Access blocked" | Asegúrate de estar usando la cuenta añadida como usuario de prueba |
| Token expira constantemente | Normal si la app no está verificada. El token de refresh debería renovarlo automáticamente |

### Problemas de memoria PostgreSQL

| Problema | Solución |
|----------|----------|
| "Connection refused" | Verifica host, puerto y que SSL esté activado |
| "Password authentication failed" | Revisa usuario y contraseña (sin espacios extra) |
| "Table not found" | La tabla se crea automáticamente en la primera ejecución |
| Mensajes no se guardan | Verifica que Session ID está configurado correctamente |

---

## Enlaces útiles

- **Documentación oficial de n8n:** [https://docs.n8n.io/](https://docs.n8n.io/)
- **Comunidad n8n:** [https://community.n8n.io/](https://community.n8n.io/)
- **Templates de workflows:** [https://n8n.io/workflows/](https://n8n.io/workflows/)
- **Google Cloud Console:** [https://console.cloud.google.com/](https://console.cloud.google.com/)
- **Supabase Dashboard:** [https://supabase.com/dashboard](https://supabase.com/dashboard)
- **Koyeb Dashboard:** [https://app.koyeb.com/](https://app.koyeb.com/)

---

> **Última actualización:** Enero 2025  
> **Autor:** Material complementario para el Máster en IA Generativa y LLMs