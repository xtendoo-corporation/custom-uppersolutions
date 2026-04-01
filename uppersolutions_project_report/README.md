# uppersolutions_project_report

Módulo para Odoo 19 Enterprise que añade en **Ventas > Reporting** el menú **Reporte de proyectos**.

## Qué hace en esta primera versión

- Abre un wizard con **Fecha inicio** y **Fecha fin**
- Valida que la fecha inicial no sea mayor que la final
- Genera un archivo Excel `.xlsx` desde el wizard
- Deja el archivo listo para descargar en el mismo wizard
- Usa la librería Python `xlsxwriter` para construir el archivo
- Crea la estructura base del reporte con estas columnas:
  - Proyecto
  - Cliente
  - Pedido de venta
  - Responsable
  - Fecha inicio
  - Fecha fin
  - Estado

## Pendiente para la siguiente iteración

- Consultar proyectos reales según el rango indicado
- Llenar las filas con los valores correspondientes
- Ajustar columnas definitivas del cliente si cambian


