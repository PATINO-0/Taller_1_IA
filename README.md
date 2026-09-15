# Taller 1 - Inteligencia Artificial

Aplicación de algoritmos genéticos construida con Next.js y FastAPI.

## Desarrollo local

```powershell
.\.venv\Scripts\Activate.ps1
npm install
npm run dev:full
```

Abra `http://localhost:3000`. El frontend usa el backend local configurado en
`.env.local` mediante `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`.

## Despliegue conjunto en Vercel

El repositorio se despliega como un solo proyecto. Next.js atiende el frontend
y `api/index.py` se empaqueta como una función Python. En producción, el cliente
envía todas las operaciones a `POST /api`, que es la ruta estable de esa función.

En la configuración del proyecto de Vercel:

1. Use la raíz del repositorio como **Root Directory**.
2. Use **Next.js** como Framework Preset.
3. Deje vacíos Build Command y Output Directory para usar la detección automática.
4. No configure `NEXT_PUBLIC_API_BASE_URL` en Preview ni Production.
5. Después de enviar los cambios a GitHub, haga un nuevo despliegue sin caché.

Verifique el backend desplegado abriendo `https://SU-DOMINIO.vercel.app/api`.
Debe responder `{"message":"Taller 1 IA API","status":"ok"}`.

## Validación

```powershell
npm run lint
npm run build
.\.venv\Scripts\python.exe -m pytest
```
