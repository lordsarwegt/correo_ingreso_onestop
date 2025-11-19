import lib.email_sender as email_sender
import ingresos as ing
import os
from datetime import datetime

def  main():

    from dotenv import load_dotenv
    load_dotenv()

    ings = ing.odoo_conection()
    model = ings.start_odoo_connection()
    ids = []
    registros= ings.get_ingresos(model)

    for item in registros:
        title = ""
        ids.append(item.get('id'))
        url = f"https://agiotech.odoo.com//web#id={item.get('id')}&model=x_ingreso_lb&view_type=form"
        if item.get('x_studio_orden_general'):
            title = "Ingreso de un producto ONE STOP sin prealerta."
        else:
            title = "Ingreso de un producto ONE STOP."

        html = f"""
            <tr>
              <td class="section" style="padding-top:12px;">
                <h1 class="title">🔔 {title}</h1>
                <p class="subtitle">Comunicación interna: Esta es una notificación automatica e informativa.</p>
                <p class="subtitle"> Generado automáticamente el: {datetime.now().strftime("%Y-%m-%d")}</p>
              </td>
            </tr>
            <tr>
              <td class="section" style="padding-top:12px;">
                    <p><strong>INGRESO:</strong> {item.get('x_name')}</p>
                    <p><strong>ORDEN:</strong> {item.get('x_studio_orden_de_reparacin',['',''])[1] if item.get('x_studio_orden_de_reparacin') else ''}</p>
                    <p><strong>PRODUCTO:</strong> {item.get('x_studio_producto',['',''])[1] if item.get('x_studio_producto') else ''}</p>
                    <p><strong>SERIE:</strong> {item.get('x_studio_numero_de_serie_interna',['',''])[1] if item.get('x_studio_numero_de_serie_interna') else ''}</p>
                    <p><strong>MODELO:</strong> {item.get('x_studio_modelo',['',''])[1] if item.get('x_studio_modelo') else ''}</p>
                    <p><strong>PAQUETERIA:</strong> {item.get('x_studio_paqueteria',['',''])[1] if item.get('x_studio_paqueteria') else ''}</p>
                    <p><strong>FECHA DE INGRESO:</strong> {item.get('create_date')}</p>
                    <a href='{url}' style='background:#007BFF;
                    color:white;
                    padding:12px 20px;
                    text-decoration:none;
                    border-radius:6px;
                    font-family:Arial;'>
                        Ver Ingreso
                    </a>
                 </td>
            </tr>
            
        """

        sender = email_sender.EmailSender(
                smtp_server = os.getenv('MAIL_SERVER'), 
                smtp_port = os.getenv('MAIL_PORT'), 
                username = os.getenv('MAIL_USERNAME'), 
                password = os.getenv('MAIL_PASSWORD'), use_tls=True)
        
        template = sender.mail_template(title="Notificacion ONE STOP", rows=html)

        sender.send_html_email(
            to_email= os.getenv('MAIL_TO'),
            subject="Notificacion ONE STOP",
            html_content=template,
            from_email=os.getenv('MAIL_FROM')
        )
    ings.write_ingreso(model,ids)    

if __name__ == "__main__":
    main()