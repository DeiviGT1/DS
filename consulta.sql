select item, ano_despacho, unidades_despachadas from(
    select item, 
        min(ano_despacho) as ano_despacho,
        sum(unidades_despachadas) as unidades_despachadas
        from despachos
            inner join item_extensiones 
                on despachos.row_id_item_ext = item_extensiones.row_id_item_ext
            inner join bodegas
                on bodegas.row_id_bodega = despachos.row_id_bodega
                    and cod_bodega ~*'^[MFT]*[0-9]'
                    or cod_bodega = 'B005'
        where fecha_exhibicion >= '2022-01-01'
    group by item

    UNION ALL

    SELECT 
        item_extensiones.item AS item,
        ano_despacho,
        SUM(neto_inv_ic)::int AS unidades_despachadas
        
    FROM movimientos
    INNER JOIN bodegas ON bodegas.row_id_bodega = movimientos.row_id_bodega 
    AND bodegas.cod_bodega SIMILAR TO '(B001)%%'
            
    INNER JOIN item_extensiones ON item_extensiones.row_id_item_ext = movimientos.row_id_item_ext 
    AND item_extensiones.tipo_inventario IN ('PTC', 'PTP') 
    AND item_extensiones.genero IN ('HOMBRE', 'MUJER') 
    AND item_extensiones.extension IN ('S', 'M', 'L')

    INNER JOIN (
        SELECT item, min(ano_despacho) AS ano_despacho from despachos
        INNER JOIN item_extensiones ON despachos.row_id_item_ext = item_extensiones.row_id_item_ext
        GROUP BY item
    ) consulta_despacho  ON consulta_despacho.item = item_extensiones.item
        
    WHERE movimientos.fecha BETWEEN '2021-01-01' AND CURRENT_DATE 
    AND movimientos.estado NOT IN ('Anulado')
        
    GROUP BY item_extensiones.item, ano_despacho) AS consulta
WHERE unidades_despachadas > 0
GROUP BY item, ano_despacho, unidades_despachadas