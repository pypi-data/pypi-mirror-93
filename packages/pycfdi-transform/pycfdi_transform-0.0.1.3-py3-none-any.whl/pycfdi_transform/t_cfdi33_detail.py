import os 
from pycfdi_transform.__t_base__ import TBase

class TCfdi33Detail(TBase):
  def __init__(self,xslt_file = 'cfdi33_detail.xslt'):
    super().__init__(xslt_file)
  
  def convert_to_columns(self,line):
    lista = list()
    if len(line) <= 2:
      return lista
    line = line[2:]
    rows = str(line).split('‡‡')    
    for row in rows:
      columns_data = str(row).split('~')
      lista.append(columns_data)
    return lista
  
  def get_column_names(self):
    return [
      "VERSION",
      "SERIE",
      "FOLIO",
      "FECHA",
      "NOCERTIFICADO",
      "SUBTOTAL",
      "DESCUENTO",
      "TOTAL",
      "MONEDA",
      "TIPOCAMBIO",
      "TIPODECOMPROBANTE",
      "METODOPAGO",
      "FORMAPAGO",
      "CONDICIONESDEPAGO",
      "LUGAREXPEDICION",
      "EMISORRFC",
      "EMISORNOMBRE",
      "EMISORREGIMENFISCAL",
      "RECEPTORRFC",
      "RECEPTORNOMBRE",      
      "RECEPTORUSOCFDI",      
      "UUID",
      "FECHATIMBRADO",
      "C_ID",
      "C_CLAVEPRODSERV",
      "C_NOIDENTIFICACION",
      "C_CANTIDAD",
      "C_CLAVEUNIDAD",
      "C_UNIDAD",
      "C_DESCRIPCION",
      "C_VALORUNITARIO",
      "C_DESCUENTO",
      "C_IMPORTE"
    ]