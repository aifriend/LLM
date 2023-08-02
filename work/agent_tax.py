import json
import os

# Standard Helpers
# Text Helpers
# Kor!
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text
# For token counting
# LangChain Models
from langchain.chat_models import ChatOpenAI

from api_key import ApiKey


def print_output(out_data):
    print(json.dumps(out_data, sort_keys=True, indent=3))


"""
Let's start off by creating our LLM
"""
os.environ["OPENAI_API_KEY"] = ApiKey.OPENAI_API_KEY
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    max_tokens=2000,
    openai_api_key=ApiKey.OPENAI_API_KEY
)

taxes = Object(
    id="taxes",
    description="Taxes and tributes invoice data",
    examples=[
        (
            "GOBIERNO DE LA RIOJA Dirección General de Tributos Servicios de Gestión Integral Tributaria AYUNTAMIENTO DE NALDA IMPUESTO SOBRE BIENES INMUEBLES NATURALEZA URBANA EJERCICIO 2021 C.I.F. S-2633001- DATOS DEL CONTRIBUYENTE NIF/NIE: IDENTIFICACIÓN DEL CONTRIBUYENTE A95652210 HARRI INMUEBLES SA DOMICILIO FISCAL AV AGUIRRE LEHENDAKARI 0009 6 D 48014 BILBAO DATOS DEL OBJETO TRIBUTARIO OBJETO TIBUTARIO VIRGEN DE VALVANERA, 0001B, 3, 00, C3 DATOS DEL RECIBO PERIODO NÚMERO RECIBO N° FIJO CONCEPTO ANUAL 2021 2610320210000IU0000008336/00 10686882 IMPUESTO SOBRE BIENES INMUEBLES NATURALEZA URBANA FECHA LÍMITE PAGO EMISORA MOD IDENTIFICACIÓN REFERENCIA IMPORTE TOTAL 09/11/2021 265550 2 5073211313 000018616353 13,47 € 24/11/2021 265550 2 9073211328 000018616392 14,14€ Recibo: 2610320210000IU0000008336/00 Conc IMPUESTO BIENES INMUEBLES URBANA Entidad: NALDA Ref. Catastral: 0876602WM4807N0063XA Uso: A Tipo impositivo: 0.54 Base liquidable: 2.494,21 € Valor Catastral: 2.494,21 € Porc. Pago: 100,00 Valor suelo: 166,26 € Valor construcción: 2.327,95 € Objeto Tributario: CL VIRGEN DE VALVANERA 0001B 3 00 C3 N° Fijo: 10686882 Cuota: 13,47 € % Bonif: 0 (Plazo 00° 100%) Cuota Liq Part: 13,47 € Ejemplar para el Contribuyente INFORMACION DEL CONTRIBUYENTE FORMA DE PAGO AVISO EJECUTIVA Ingreso en cualquier sucursal de la red de oficinas de BANKIA o IBERCAJA Transcurrido el periodo voluntario de pago, se inicia el periodo ejecutivo, VALIDACIÓN que determina el devengo del recargo y de los intereses de demora, así Este documento no libera del pago sin la validación de la Entidad Financiera como, en su caso de las costas del procedimiento, de acuerdo con lo o si se paga con posterioridad a la fecha límite de pago (fin de voluntaria) establecido en los articulo 25 y 28 de la Ley General Tributaria y DOMICILIACIÓN disposiciones concordantes Por su comodidad domicilie sus tributos Ejemplar para la Entidad Financiera Período voluntario Emisora Mod. Referencia Identificación Importe a ingresar",
            [
                {
                    "ref_cat": "0876602WM4807N0063XA",
                    "payer": "HARRI INMUEBLES SA",
                    "payer_id": "A95652210",
                    "barcode": "905222655500000186163539207321131300001347132800001414"
                }
            ]
        ),
        (
            "PATRONATO DE RECAUDACION PROVINCIAL CARTA DE PAGO DIPUTACION PROVINCIAL DE MALAGA PERIODO VOLUNTARIO EJEMPLAR PARA EL CONTRIBUYENTE Este recibo se podrá abonar hasta la fecha límite de pago y no tendrá validez sin sello de caja o impresión mecánica. ORGANISMO: AYUNTAMIENTO DE MOLLINA Fecha Límite de Pago CONCEPTO: I.B.I. (URBANA E INMUEBLES DS) 13/09/2021 Obligado al pago: CAJASUR BANCO SA NIF/CIF/NIE: A95622841 Domicilio Fiscal del Recibo: AVDA RONDA DE LOS TEJARES 18 C.P. 14001 CORDOBA (CORDOBA) 20 JUL NECKS INFORMACIÓN DE LIQUIDACIÓN MATRÍCULA Domicilio: CL UE-14 101 0 S UE LO 29532 44874180 N. Cargo / Recibo: 1D7028 - 407 Identificativo: 2306729UG5120N0000FG AÑO Fecha Emisión: 07/07/2021 Periodo / Año Devengo: R-ANO-2021 2021 2021 Fecha Fin Voluntaria: 13/09/2021 TOTAL EUROS PRINCIPAL PRINCIPAL IVA SANCIÓN REC 27 INT.VOL REC. APR. INT.DEMORA COSTAS INICIAL PENDIENTE PENDIENTE PENDIENTE PENDIENTE PENDIENTE PENDIENTE PENDIENTE PENDIENTE 34,83 34,83 0,00 0,00 0,00 0,00 0,00 0,00 0,00 34,83 DATOS DEL RECIBO Dirección Tributaria : CL UE-14 101 S UE LO 0 Base Imponible-Valor Catastra 8.707,89 NEINOR Valor Catastral Suelo 8.707,89 Valor Catastral Construcción. 0,00 Base Liquidable 8.707,89 2 0 JUL. 2021 Año V.Catast/Año Ult Rev 2021/2006 Valor Base 10.619,38 Naturaleza Bien Inmueble URBANA Uso/Tipo Aplicado M-SUELOS SIN EDIFICAR/0, 400000% Cuota Integra 34,83 Cuota Líquida 34,83 CSB57 EMISORA: 79000010 SUFIJO: 533 REFERENCIA: 0091321614538 IDENTIFICACION: 130921 IMPORTE: 0000000034,83 Finalizado el periodo voluntario, el importe de la deuda se incrementará con el recargo de apremio, interés de demora y costas. PATRONATO DE RECAUDACIÓN PROVINCIAL DE MALAGA C/ SEVERO OCHOA 32 (P T.A) Sr. Cartero/a: Desconocido 29590 CAMPANILLAS MALAGA en caso de devolución, ATENCIÓN AL PÚBLICO Y REMISIÓN DE ESCRITOS Se marchó sin dejar señas marque con una X EN LAS OFICINAS ABAJO INDICADAS el motivo. Dirección incompleta MÁS INFORMACIÓN EN LA PÁGINA WEB: https://portalweb.prpmalaga.es",
            [
                {
                    "r": "2306729UG5120N0000FG",
                    "payer": "CAJASUR BANCO SA",
                    "payer_id": "A95622841",
                    "barcode": ""
                }
            ]
        ),
        (
            "DIPUTACIÓN 1 de 1 D ZARAGOZA GESTION Y ATENCION TRIBUTARIA Oficina: C/ Alfonso n° 17 7 planta 50003 Zaragoza Información al contribuyente 1. Inicio de Ejecutiva: Finalizado el periodo voluntario, los recibos pendientes incurren en Recargo, devengando interés de demora y costas del procedimiento. 9052250000821013083708882073211204000006051 2. Este documento es nulo sin la validación de Entidad 21800000635 autorizada, el pago no libera de la deuda si se efectúa con posterioridad al último día de pago señalado. NEINOR NORTE SL 3. Pago: https://dpz.tributoslocales.es o CL ERCILLA 24 Pla 2 http://www.ibercaja.es/tributos, cajeros de Ibercaja, Ibercaja Directo (clientes Ibercaja) u oficinas Ibercaja con servicio en Efectivo (listado https://www.ibercaja.es/oficinas/). 48011 BILBAO BIZKAIA CADRETE PERIODO: 2021 ANUAL RECIBO DEL IMPUESTO SOBRE BIENES INMUEBLES - NAT. URBANA Referencia Catastral Val.Suelo Jal.Construc. Val.Catastral Total 6954501 TG34650 0270 320,95 889,39 1.210,34 Año Val. Año Rev. Uso Base Liquidable Tipo Cuota Íntegra 2021 2007 A 1.210,34 0,5000 6,05 % Part.Indivi Bonificación C.Liq.Participada 100,00 0,00 6,05 Contribuyente Identificador Fiscal Periodo voluntario Referencia de pago Importe a ingresar NEINOR NORTE SL B 95788626 21/05/2021 al 210130837088 EUR* 6,05 23/07/2021 Identificación del Recibo Número fijo Periodo ejecutivo Referencia de pago Importe a ingresar 20210750066IU01R003900 10406259 06/08/2021 210130837082 EUR* 6,35 CL SERVET, MIGUEL 0006 1 -1 M1 Principal 6,05 Recargo 0,00 Ing. Cuenta 0,00 Recibo en Voluntaria Ejemplar para el Contribuyente Código procedimiento recaudación: 9052180 DIPUTACIÓN Recibo en Voluntaria Ejemplar para la Entidad Financiera D ZARAGOZA Último día de pago Emisora Modo Referencia Identificación Importe a ingresar GESTION Y ATENCION 23/07/2021 500008 2 210130837088 5073211204 EUR* 6,05 06/08/2021 500008 2 210130837082 9073211218 EUR* 6,35 Titular según el Padrón Identificador Fiscal NEINOR NORTE SL B 95788626 Alta de",
            [
                {
                    "ref_cat": "6954501 TG34650 0270",
                    "payer": "NEINOR NORTE SL",
                    "payer_id": "B 95788626",
                    "barcode": "9052250000821013083708882073211204000006051"
                }
            ]
        ),
        (
            "white DOCUMENTO DE PAGO Ayuntamiento de Viladecans AJUNTAMENT DE C/ Jaume Abril, 2 VILADECANS Telf.: 936351800 CSV: 14620543657471737274 EJEMPLAR PARA EL CONTRIBUYENTE CPR PERÍODO DE PAGO EMISORA MOD REFERENCIA IDENTIFICACIÓN IMPORTE 9050299 Hasta et 07/08/2023 083010 1 000206285141 0732301 102,69 € INSTITUCIÓN VCN Ajuntament de Viladecans REF. REC. RB 2062851 CONCEPTO TRIBUT METROPOLITÀ (AMB) OBJETO TRIBUTARIO 91544526 - C TORRENT FONDO, 6 Esc B 04 02 DEVENGO Anual 2023 TRIBUT METROPOLITANA EXERCICI 2023 OBJ. TRIBUTARI o TORRENT FONDO, 6 Esc B 04 02 NUM. FIX: 91544526 REFERENCIA CADASTRAL : 8649805DF1784H0043RO ANY REVISIÓ 2006 VAL SOL: 67742,06 VAL CONS: 46326,61 VAL CADAS: 114068,67 TIPUS 0,200 % QUOTA INTEGRA: 228,14 REDUC. 125,45 BONIF. 0,00 QUOTA LÍQUIDA: 102,69 BANC SABADELL SA (A08000143) 90502083010000205285141073230100010269 LUGAR DE PAGO: En cualquier sucursal de ServiCaixa, BBVA, Banco de Sabadell, Bankia y Banco de Santander INFORMACIÓN AL PAGADOR PARA REALIZAR EL PAGO dirijáse con este documento, no más tarde de la fecha límite de pago del mismo, a cualquier sucursal de una de las Entidades Colaboradoras señaladas No es necesario tener cuenta abierta en las mismas, ESTE DOCUMENTO SE EXPIDE A PETICIÓN DE INTERESADO Y AL SOLO EFECTO DE REALIZAR EL PAGO DE LA DEUDA DETALLADA. Su emisión es un acto de trámite que no admite recurso alguno, sin perjuicio de los que en su caso procedan contra el acto de liquidación origen de la deuda. ESPACIO RESERVADO PARA LA VALIDACIÓN MECÁNICA EJEMPLAR PARA LA ENTIDAD CO ABORADORA CPR PERIODO DE PAGO EMISORA MOD REFERENCIA IDENTIFICACIÓN IMPORTE 9050299 Hasta el 07/08/2023 083010 1 000206285141 0732301 102,69 6 BANC SABADELL SA (A08000143) 9050208301000020628514107323010001025 CPR PERÍODO DE PAGO EMISORA MOD REFERENCIA IDENTIFICACIÓN IMPORTE 9050299 Hasta et 07/08/2023 083010 1 000206285141 0732301 102,69 € INSTITUCIÓN VCN Ajuntament de Viladecans REF. REC. RB 2062851 CONCEPTO TRIBUT METROPOLITÀ (AMB) OBJETO TRIBUTARIO 91",
            [
                {
                    "ref_cat": "8649805DF1784H0043RO",
                    "payer": "BANC SABADELL SA",
                    "payer_id": "A08000143",
                    "barcode": "90502083010000205285141073230100010269"
                }
            ]
        ),
        (
            "DOCUMENTO PARA PAGAR DATOS DEL CONTRIBUYENTE PROMONTORIA COLISEUM REAL ESTATE SLU B67479451 1510 AJUNTAMENT DE SABADELL - NIF: P0818600 EJERCICIO - CONCEPTO 2023 IMPUESTO SOBRE BIENES INMUEBLES URBANOS ema la OBJETO C SANT PAU 149 PBX Refer. cadastral.: 5894021 DF2959H-0003/FX Número fix: 91705353 Any Revisió 2002 Val.cadastral: 37.042,59 Val.constr.: 5.004,12 Val.sól: 32.038,47 Base imposable.. 37.042,59 Base liquidable 37,042.59 Tipus aplicati 0,5416 Quota integra 200,62 CSU QUOTA LÍQUIDA 200,62 Codido Doc. documento Referencia 02809923-0001290125 Plazo de pago De 02.05.2023 a 05.07.2023 Abonaré 8809923-08385011 TOTAL A PAGAR 200,62 € del CPR: 9050299 Diputació Datos y comprobante para la entidad bancaria 9196 Barcelona Organisme de Gestió Tributária Pea. Núm. Abonaré 8809923-08385011 IMPORTE 200,62 € 10502085005000838501147880992300020062 Emisora: 085005 Referencia: 000838501147 Identificación: 8809923 EUR 200,62 € Base liquidable 37,042.59 Tipus aplicati 0,5416 Quota integra 200,62 QUOTA LÍQUIDA 200,62 Key Value Abonaré 8809923-08385011 Referencia 02809923-0001290125 TOTAL A PAGAR 200,62 € IMPORTE 200,62 € Núm. Abonaré 8809923-08385011 Plazo de pago De 02.05.2023 a 05.07.2023 QUOTA LÍQUIDA 200,62 Identificación: 8809923 Referencia: 000838501147 Emisora: 085005 Quota integra 200,62 CPR: 9050299 Tipus aplicati 0,5416 Base liquidable 37,042.59 AJUNTAMENT DE SABADELL - NIF: P0818600 Base imposable.. 37.042,59 EUR 200,62 € Val.cadastral: 37.042,59 Val.sól: 32.038,47 Refer. cadastral.: 5894021 DF2959H-0003/FX Número fix: 91705353 Any Revisió 2002 DATOS DEL CONTRIBUYENTE PROMONTORIA COLISEUM REAL ESTATE SLU B67479451 OBJETO C SANT PAU 149 PBX Val.constr.: 5.004,12",
            [
                {
                    "ref_cat": "5894021 DF2959H-0003/FX",
                    "payer": "PROMONTORIA COLISEUM REAL ESTATE SLU",
                    "payer_id": "B67479451",
                    "barcode": "10502085005000838501147880992300020062"
                }
            ]
        )
    ],
    attributes=[
        Text(
            id="ref_cat",
            description="Real state cadastral reference."
        ),
        Text(
            id="payer",
            description="The name of the person who pay the bill"
        ),
        Text(
            id="payer_id",
            description="Identity card number of the person who pay the bill"
        ),
        Text(
            id="barcode",
            description="Bar code encrypted data"
        ),
    ]
)

if __name__ == '__main__':
    text = "Periodo de pago Emisora Referencia Identificación Importe 20/04/2023-30/06/2023 41 091 3 2300928051 99 001 23 01 57,40 € IMECESTO SOBRE BIENES ENEURBLES NATURALFZA URBANA PERIODS LIQUIDADO: 01/01/2023 AL 30/06/2003 NOSDO OBJETO TRIBUTARIO : 01 CRFEBPE CAYETANG GLEZ 3 .263 0000 00000 33 Referencia Catastral: 7290030 1333795 0215 T E AYUNTAMIENTO Número Fijo : 00615728 DE SEVILLA Superficie : 87,00 11.2 Cost. partic.: 6.16 LIGHTEACTON USA : PESIDENCIAL Base Liquidable 16.987,726 Año ult. rev. : C V. Base: 7.728.266 Tipo de gravemen 0,6758 C.I.F.: P4109100J V. Suelo: 4.399.82€ V. Const: 12.587,98€ Cuota integra 114,80€ Agencia VALOR CATASTRAL (Base Imponible) : 16.987,726 Liquidación Sujeto Pasivo: 100,00 Tributaria Cuota Int. Sujeto Pasivo : 114,80€ de Sevilla Gorificacion 0,00 Derecho Prevalente : PROPIETARIO Cuota Liquida (Anual) 114,80€ Benef. Fiscales DEUDA TRIB. SEMESTRAL: 57,400 Ref. Domiciliación: 202000029114 C5202304200012301904082000613 PROMONTORIA COLISEUM REAL ESTATE SL CL SERRANO N: 0026 Piso 06 90502410913230092805199001230200005740 28001 MADRID MADRID EXPEDIENTE: 202000029114 NÚMERO DE RECIBO: 202300928051 DNI/NIF: B67479451 Código IBAN de cuenta cliente Este documento no será válido sin certificación mecánica 0 firma autorizada Ejemplar para el Contribuyente Periodo de pago Emisora Referencia Identificación Importe 20/04/2023-30/06/2023 41 091 3 2300928051 99 001 23 01 57,40 € IMPUESTO SCBRE BIENES INMUEBLES NATURALEZA URBANA PERICDO LIQUIDADO: 01/01/2023 AL 33/06/2023 NOSDO OBJETO TRIBUTARIO : CL ORFEBRE CAYETANO GLEZ 3 0260 0000 00000 93 C Referencia Catastral: 7290810 1G33793 0015 T B AYUNTAMIENTO Núrero Fito : 03/10/28 DE SEVILLA Superficie : 87,00 IT.2 Coef. partic. 6,163 LIQUIDACION Use : RESIDENCIAL Base Liquidable 16.997.72€ Año ult. rev. : is : Base: 7,728,266 Tipo de gravamen 0,6758 C.I.F.: P4109100J V. Suelo: 4.399,82€ V. Const: 1,487,966 Chora interest 114,80€ VALOR CATACIPAL (Base 16.987,726 Liquidación Sujeto Pasivo: 100,00 Cuota Int. Sugeto Pasivo : 114,806 Agencia Bonificacton 0.00 Tributaria Derecho Prevalente PESPIETARIO Cucca Bround (Anual) : 114,806 Berst. Fiscales LECIA TEIE SEMESTRAL: 57,40€ de Sevilla Código IBAN de cuenta cliente Este documento no será válido sin certi- PROMONTORIA COLISEUM REAL ESTATE SL DNI/NIF: B67479451 Ref. Domicillación: 202000029114 ficación mecánica CL SERRANO N: 0026 Piso 06 EXPEDIENTE: 202000029114 o firma autorizada 28001 MADRID MADRID NÚMERO DE RECIBO: 202300928051 90502410913230092805199001230100005740 Ejemplar para la Entidad Colaboradora 1271 Periodo de pago Emisora Referencia Identificación Importe 20/04/2023-30/06/2023 41 091 3 2300928051 99 001 23 01 57,40 € Base Liquidable 16.987,726 Tipo de"
    chain = create_extraction_chain(llm, taxes, encoder_or_encoder_class="json")
    prompt = chain.prompt.format_prompt(text=text).to_string()
    print(f"View the prompt that was sent over:\n{prompt}\n")
    output = chain.predict_and_parse(text=text)['data']
    print_output(output)
