# Investigacion: Estructura de Guardado v0.9.0 vs v0.8.x

## Fecha: 12 de Noviembre 2025

## Hallazgos Principales

### Diferencia Clave

**VotV 0.8.x** (s_1.sav):
```
Offset 0x000006ad: "Points" -> IntProperty -> Valor: 75000
```

La propiedad `Points` existe como IntProperty en el formato de guardado.

**VotV 0.9.0 alpha** (s_09colege.sav):
```
NO existe la propiedad "Points" como IntProperty
```

La palabra "points" solo aparece en textos descriptivos, no como propiedad del juego.

## Analisis Tecnico

### Formato de Archivo

Ambas versiones usan:
- **Magic Number**: `GVAS` (0x53415647)
- **Engine**: Unreal Engine 4.27 (++UE4+Release-4.27)
- **Formato**: Unreal SaveGame binary serialization

### Propiedades Encontradas

#### v0.8.x (FUNCIONAL)
- `Points`: IntProperty con valor modificable
- Offset fijo y predecible
- Estructura simple y directa

#### v0.9.0 alpha (NO FUNCIONAL)
- NO existe `Points` como IntProperty
- Estructura de datos reorganizada completamente
- Posibles ubicaciones alternativas:
  1. Dentro de una estructura compleja (StructProperty)
  2. En un array de propiedades
  3. Con nombre de variable diferente
  4. En GameInstance en vez de SaveGame

## Strings Relevantes Encontrados

### v0.8.x
```
points_7_6DD8FF16419714EB5D548B976F625F36  (offset 0x00002c37)
```
Esto sugiere que los puntos podrian estar en una estructura con GUID.

### v0.9.0
```
No se encontraron propiedades similares
```

## Teorias

### Teoria 1: Cambio de Arquitectura
Los puntos podrian haberse movido a:
- GameInstance persistente
- Sistema de guardado en la nube
- Base de datos local separada

### Teoria 2: Nombre Diferente
La propiedad podria llamarse ahora:
- Currency
- Money
- Score
- PlayerPoints
- O estar dentro de una estructura PlayerData

### Teoria 3: Serializacion Compleja
Los puntos podrian estar en:
- StructProperty anidado
- ArrayProperty
- MapProperty
- Comprimido o encriptado

## Proximos Pasos para Investigacion

### Metodo 1: Comparacion Diferencial
1. Crear un nuevo save en v0.9
2. Anotar puntos iniciales
3. Ganar exactamente X puntos (ej: 100)
4. Guardar juego
5. Comparar archivos byte por byte
6. Buscar valores que cambien en +100

### Metodo 2: Analisis de Codigo
1. Acceder a la carpeta del juego:
   ```
   J:\Onedrive\OneDrive - Fundacion Instituto Profesional Duoc UC\Documentos\a09_0015\WindowsNoEditor
   ```
2. Buscar archivos .pak (paquetes de assets)
3. Intentar extraer blueprints
4. Buscar referencias a "Points" en el codigo

### Metodo 3: Memory Scanning
1. Ejecutar el juego
2. Usar Cheat Engine para buscar valor de puntos en memoria
3. Cambiar puntos en juego
4. Re-escanear para encontrar direccion de memoria
5. Ver como se serializa al guardar

### Metodo 4: Network Analysis
Si los puntos se guardan en servidor:
1. Capturar trafico de red con Wireshark
2. Buscar peticiones al guardar
3. Ver si los puntos se sincronizan online

## Datos Tecnicos

### Estructura GVAS (Unreal SaveGame)

```
Header:
- Magic: GVAS (4 bytes)
- SaveGame Version (4 bytes)
- Package Version (4 bytes)
- Engine Version String
- Custom Version Format
- Custom Version GUID

Body:
- ClassName (FString)
- Properties (serialized)
```

### Formato de Propiedades

```
PropertyName (FString)
PropertyType (FString) - "IntProperty", "FloatProperty", etc.
PropertySize (int32)
PropertyIndex (int32) 
PropertyValue (variable size)
```

## Herramientas Recomendadas

1. **UE4 SaveGame Reader**: Para deserializar archivos .sav
2. **HxD / 010 Editor**: Hex editors con templates UE4
3. **UAssetGUI**: Para explorar archivos .pak
4. **Cheat Engine**: Para memory scanning
5. **Wireshark**: Para analisis de red

## Estado Actual

**BLOQUEADO**: No se puede modificar puntos en v0.9.0 alpha hasta:
1. Encontrar la nueva ubicacion de los puntos
2. Entender el nuevo formato de serializacion
3. Implementar parser para la nueva estructura

## Recomendacion

Por ahora, usar VotV 0.8.2c con el editor de la carpeta `v0.8.x/` que funciona perfectamente.

---

**Investigadores**: Si encuentras algo, por favor abre un issue en GitHub con tus hallazgos.

