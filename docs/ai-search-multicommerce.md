# AI Search Backend + Magento Integration (Multi-Commerce)

## 1) Objetivo de esta implementacion
Este desarrollo separa la inteligencia de busqueda en un backend FastAPI reutilizable para multiples ecommerce (multi-commerce), manteniendo Adobe Commerce (Magento) como consumidor de filtros y resultados.

Principios aplicados:
- FastAPI como servicio de IA compartido.
- Magento como cliente de integracion, no como motor IA.
- Contrato de respuesta estable versionado (v1).
- Trazabilidad de decisiones (source/fallback), correcciones y metricas.

## 2) Alcance implementado
Se incorporaron 4 bloques funcionales:
- Bloque A: Robustez de integracion Magento -> FastAPI.
- Bloque B: Contrato v1 normalizado para consultas IA.
- Bloque C: Correcciones administrables (rules engine liviano).
- Bloque D: Observabilidad de negocio (eventos y KPIs).

## 3) Arquitectura funcional
### 3.1 Flujo principal
1. Front Magento envia texto de usuario.
2. Magento solicita IA al endpoint FastAPI v1.
3. FastAPI extrae intencion + arma filtros candidatos.
4. FastAPI aplica correcciones activas por tenant/contexto.
5. FastAPI responde filtros + metadatos operativos.
6. Magento convierte filtros al SearchCriteria propio.
7. Front muestra resultados y etiqueta origen (IA/fallback).
8. Front o backend reporta eventos para metricas.

### 3.2 Contexto multi-commerce
Cada request viaja con:
- platform
- tenant_id
- locale
- session_id (para trazabilidad)

Con esto, un mismo backend soporta multiples marcas/tiendas/paises sin duplicar logica.

## 4) Para que sirve cada tabla nueva
## 4.1 corrections
Tabla de reglas de correccion manual para ajustar resultados IA sin redeploy.

Uso:
- Corregir sinonimos, errores frecuentes, expresiones locales.
- Forzar valor de atributo cuando una frase aparece.

Campos clave:
- platform, tenant_id, locale: delimitan alcance multi-commerce.
- attribute_code: atributo a corregir (ejemplo: color).
- raw_phrase: frase gatillo.
- corrected_value_string / corrected_value_number: valor final forzado.
- rule_type: tipo de matching (exact, contains, regex).
- priority: orden de aplicacion.
- is_active: activacion/desactivacion sin borrar historial.

## 4.2 corrections_audit
Tabla de auditoria de cambios sobre corrections.

Uso:
- Saber quien creo/edito/desactivo una regla.
- Recuperar old_data/new_data para trazabilidad y debugging.
- Soporte de gobierno y compliance interno.

Acciones registradas:
- insert
- update
- delete (soft delete por desactivacion)

Nota tecnica importante:
- Se serializa old_data/new_data con conversion robusta para tipos de BD (por ejemplo Decimal y datetime), evitando error 500 por JSON serialization.

## 4.3 search_events
Tabla de eventos de experiencia y conversion para medir calidad del buscador.

Uso:
- Registrar search, result_click, add_to_cart, conversion.
- Calcular KPIs por rango de fechas, plataforma y tenant.

KPIs derivados:
- total_searches
- total_clicks
- ctr
- add_to_cart_rate
- conversion_rate
- avg_latency_ms
- sources_breakdown (IA vs fallback)

## 4.4 embedded_phrase (existente, optimizada en esta fase)
Tabla vectorial de frases embebidas para mapear texto libre a atributos/valores.

Mejoras aplicadas:
- top-k
- umbral minimo de similitud
- deduplicacion
- preferencia de candidatos numericos
- scoping multi-tenant por platform + tenant_id + locale + store_code

Objetivo:
- Mejorar precision y estabilidad de filtros candidatos antes de correcciones.
- Evitar contaminacion semantica entre tiendas/comercios que comparten la misma base.

Campos de contexto recomendados en embedded_phrase:
- platform
- tenant_id
- locale
- store_code

Nota operativa:
- Para habilitar este aislamiento, aplicar la migracion [docs/sql/002_embedded_phrase_multitenant.sql](sql/002_embedded_phrase_multitenant.sql).

## 5) Endpoints relevantes
## 5.1 IA principal
- GET /get_response/v1

Entrega:
- response estructurado
- filters normalizados
- applied_corrections
- meta (api_version, request_id, source, fallback_reason, latency_ms, contexto)

## 5.2 Correcciones
- GET /corrections/
- POST /corrections/
- PUT/PATCH (segun router implementado)
- DELETE logico (desactivacion)

Entrega:
- CRUD operativo de reglas
- auditoria automatica en corrections_audit

## 5.3 Metricas
- POST /metrics/event
- GET /metrics/summary
- GET /metrics/export

Entrega:
- Ingestion de eventos
- resumen de KPIs
- export para analisis externo

## 6) Cambios funcionales en Magento
## 6.1 Integracion de backend IA
- Provider con timeout/retry/min_similarity configurables.
- Validacion de contrato de API.
- Manejo explicito de source/fallback_reason.
- Envio de contexto multi-tenant desde Magento a FastAPI: platform=magento, tenant_id=website_code, locale=store locale, store_code=store code.

## 6.2 UX de transparencia
- Badge visible en resultados para indicar origen IA/fallback.
- Exposicion de fallback_reason para soporte y debugging.

## 7) Estado actual de lineamientos iniciales
Si. El lineamiento inicial se mantiene y esta mejor alineado ahora:
- Se avanzo de integracion puntual a plataforma reutilizable.
- Se separo logica IA del canal Magento.
- Se agrego control humano (correcciones) sin romper automatizacion.
- Se agrego medicion de negocio para cerrar loop de mejora.

## 8) Roadmap propuesto (multi-commerce)
## Fase 1 (completada)
- Contrato v1 y metadatos de trazabilidad.
- Correcciones con auditoria.
- Metricas base y export.
- Integracion Magento resiliente.
- Validacion de unicidad logica para correcciones activas en API (respuesta HTTP 409 en duplicados).

## Fase 2 (siguiente recomendada)
- API key o auth para endpoints administrativos (corrections/metrics).
- Catalogo de attributes permitidos por tenant para validacion estricta.
- Endpoint de lectura de auditoria paginado.

## 8.1 Deploy tecnico recomendado para unicidad en BD
Para blindar concurrencia y evitar duplicados por carrera, aplicar en PostgreSQL:
- [docs/sql/001_corrections_active_uniqueness.sql](sql/001_corrections_active_uniqueness.sql)

Clave unica activa aplicada:
- platform + tenant_id + locale + attribute_code + lower(trim(raw_phrase)) + is_active=true

## 8.2 Deploy tecnico recomendado para embeddings multi-tenant
Para evitar mezcla de frases y option_ids entre tiendas/comercios que comparten infraestructura:
- [docs/sql/002_embedded_phrase_multitenant.sql](sql/002_embedded_phrase_multitenant.sql)

Contexto de consulta/carga aplicado:
- platform + tenant_id + locale + store_code

## Fase 3 (escala multi-commerce)
- Namespaces por comercio y versionado de reglas por tenant.
- Workflow de aprobacion de correcciones (draft -> approved).
- Panel de analitica con cohorts por canal/categoria.
- Evaluacion offline (golden set) y scorecards por release.

## 9) Operacion diaria recomendada
1. Monitorear /metrics/summary por periodo.
2. Detectar queries con baja conversion o alto fallback.
3. Crear/ajustar reglas en /corrections.
4. Verificar impacto en CTR/conversion.
5. Mantener higiene de reglas (prioridad, duplicados, reglas inactivas).

## 10) Riesgos conocidos y mitigacion
- Riesgo: duplicado de reglas activas para misma frase.
  Mitigacion: constraint parcial unica o validacion aplicativa previa.

- Riesgo: sobreajuste por reglas regex agresivas.
  Mitigacion: limitar regex por tenant y auditar cambios.

- Riesgo: drift de contrato entre consumidores.
  Mitigacion: schema versionado y tests de contrato.

## 11) Definicion de exito
El sistema cumple objetivo cuando:
- Baja porcentaje de fallback.
- Sube CTR y conversion sobre busqueda.
- Disminuye tiempo de correccion operativa (sin deploy).
- Nuevos comercios se conectan reutilizando mismo backend.

## 12) Checklist para onboarding de un nuevo commerce
- Definir platform y tenant_id.
- Cargar atributos habilitados.
- Cargar primeras reglas de corrections.
- Integrar eventos de click/add_to_cart/conversion.
- Validar KPIs base antes y despues de activacion.
