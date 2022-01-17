product_delivery_area = """
SELECT DISTINCTROW c.*
	FROM delivery_partner_service_areas
			 JOIN cities c on delivery_partner_service_areas.city_id = c.id
	WHERE delivery_partner_service_id IN
		  (SELECT delivery_partner_service_id FROM product_delivery_partners WHERE product_id = %(pid)s)
		  UNION
	SELECT c.*
	FROM product_delivery_partners pdp
	JOIN products p
		ON p.id = pdp.product_id
	JOIN outlet_couriers oc
		ON p.outlet_id = oc.outlet_id
	JOIN outlet_courier_configurations occ
		ON oc.id = occ.outlet_courier_id
	JOIN cities c
		ON c.id = occ.city_id
	WHERE pdp.product_id = %(pid)s
		AND pdp.delivery_partner_service_id = 25
		AND occ.is_deleted = 0;
"""