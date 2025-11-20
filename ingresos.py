from dotenv import load_dotenv
import os
import xmlrpc.client
from datetime import datetime
import logging


class odoo_conection:

    def __init__(self):
        load_dotenv()

    def start_odoo_connection(self):
        # -- Odoo connection - Begin
        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(os.getenv('URL_ACCS')))

        self.uid = self.common.authenticate(os.getenv('DB_LOC'), os.getenv('DB_USR'), os.getenv('DB_PASS'), {})

        if not self.uid:
            raise Exception("Error de autenticación en Odoo")

        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(os.getenv('URL_ACCS')))
        # -- Odoo connection - Begin

        # Save DataBase 
        return self.models
    
    def close_odoo_connection(self):
        self.common._ServerProxy__transport.close()
        self.models._ServerProxy__transport.close()

    
    def get_ingresos(self, models):
        domain =  [        
            ['x_studio_stage_id','=',4],
            ['x_studio_tipo_de_ingreso','=','ONE STOP'],
            ['x_studio_correo_electronico','=','NO ENVIADO'],
        ]

        fields_list = ['x_name', 'x_studio_orden_de_reparacin','x_studio_producto', 'x_studio_numero_de_serie_interna','x_studio_modelo','x_studio_paqueteria',
                  'x_studio_fecha_de_ingreso','x_studio_stage_id','x_studio_orden_general']
        
        fields = fields_list

        datos = models.execute_kw(
            os.getenv('DB_LOC'), 
            self.uid, 
            os.getenv('DB_PASS'),     
            'x_ingreso_lb', 
            'search_read', 
            [domain],
            {'fields': fields})
        
        return datos
    
    def write_ingreso(self,models,ids):
        if ids:

            try:
        
                models.execute_kw(
                    os.getenv('DB_LOC'), 
                    self.uid, 
                    os.getenv('DB_PASS'),     
                    'x_ingreso_lb', 
                    'write',
                    [ids, {'x_studio_correo_electronico': 'ENVIADO'}])
                
                logging.info(f"Se cambio el status correctamente id{ids}")
                
            except Exception as e:

                logging.error(f"Error al actualizar el status: {e}")


        #for item in datos:
        #    lista = []
        #    url = f"https://agiotech.odoo.com//web#id={item.get('id')}&model=x_ingreso_lb&view_type=form"
        #    lista.append(url)
        #    lista.append(item.get('x_name'))
        #    lista.append(item.get('x_studio_orden_de_reparacin',['',''])[1] if item.get('x_studio_orden_de_reparacin') else '')
        #    lista.append(item.get('x_studio_producto',['',''])[1] if item.get('x_studio_producto') else '')
        #    lista.append(item.get('x_studio_numero_de_serie_interna',['',''])[1] if item.get('x_studio_numero_de_serie_interna') else '')
        #    lista.append(item.get('x_studio_modelo',['',''])[1] if item.get('x_studio_modelo') else '')
        #    lista.append(item.get('x_studio_paqueteria',['',''])[1] if item.get('x_studio_paqueteria') else '')
        #    lista.append(item.get('create_date'))
        #    if item.get('x_studio_orden_general'):
        #        lista.append("Ingreso de un producto ONE STOP sin prealerta.")
        #    else:
        #        lista.append("Ingreso de un producto ONE STOP.")
                
            #return self.create_html(datos)
            
        
    #def create_html(self,lista):
#
    #    
    #    html = f"""
    #        <tr>
    #          <td class="section" style="padding-top:12px;">
    #            <h1 class="title">🔔 {lista[8]}</h1>
    #            <p class="subtitle">Comunicación interna: Esta es una notificación automatica e informativa.</p>
    #            <p class="subtitle"> Generado automáticamente el: {datetime.now().strftime("%Y-%m-%d")}</p>
    #          </td>
    #        </tr>
    #        <tr>
    #          <td class="section" style="padding-top:12px;">
    #                <p><strong>INGRESO:</strong> {lista[1]}</p>
    #                <p><strong>ORDEN:</strong> {lista[2]}</p>
    #                <p><strong>PRODUCTO:</strong> {lista[3]}</p>
    #                <p><strong>SERIE:</strong> {lista[4]}</p>
    #                <p><strong>MODELO:</strong> {lista[5]}</p>
    #                <p><strong>PAQUETERIA:</strong> {lista[6]}</p>
    #                <p><strong>FECHA DE INGRESO:</strong> {lista[7]}</p>
    #                <a href='{lista[0]}' style='background:#007BFF;
    #                color:white;
    #                padding:12px 20px;
    #                text-decoration:none;
    #                border-radius:6px;
    #                font-family:Arial;'>
    #                    Ver Ingreso
    #                </a>
    #             </td>
    #        </tr>
    #        
    #    """
    #    return html


