#!/usr/bin/env python3
"""
Bot de Recibos por Honorarios
Automatiza la generación de recibos por honorarios desde Excel hacia SUNAT
Autora: Daniela Fernanda Ojeda Arrelucea
"""

import logging
import pandas as pd
import os
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class BotRecibosHonorarios:
    def __init__(self, archivo_excel="data/input/recibos_ejemplos.xlsx"):
        """
        Inicializa el bot con la ruta del archivo Excel
        
        Args:
            archivo_excel (str): Ruta al archivo Excel con los datos
        """
        self.archivo_excel = archivo_excel
        self.recibos_ejemplos = None
        
    def verificar_archivo_excel(self):
        """Verifica que el archivo Excel exista"""
        if not os.path.exists(self.archivo_excel):
            logger.error(f"❌ El archivo {self.archivo_excel} no existe")
            return False
        
        logger.info(f"✅ Archivo {self.archivo_excel} encontrado")
        return True
    
    def leer_excel(self):
        """
        Lee el archivo Excel y carga los datos en memoria
        
        Returns:
            bool: True si la lectura fue exitosa, False en caso contrario
        """
        try:
            logger.info("📖 Leyendo archivo Excel...")
            
            # Leer el archivo Excel
            self.recibos_ejemplos = pd.read_excel(
                self.archivo_excel,
                engine='openpyxl'  # Motor para archivos .xlsx
            )
            
            # Mostrar información básica
            logger.info(f"✅ Excel leído exitosamente")
            logger.info(f"📊 Total de registros: {len(self.recibos_ejemplos)}")
            logger.info(f"📋 Columnas encontradas: {list(self.recibos_ejemplos.columns)}")
            
            return True
            
        except FileNotFoundError:
            logger.error(f"❌ No se encontró el archivo {self.archivo_excel}")
            return False
        except Exception as e:
            logger.error(f"❌ Error al leer el Excel: {str(e)}")
            return False
    
    def validar_datos(self):
        """
        Valida que los datos del Excel tengan la estructura correcta
        
        Returns:
            bool: True si los datos son válidos, False en caso contrario
        """
        if self.recibos_ejemplos is None:
            logger.error("❌ No hay datos cargados")
            return False
        
        # Columnas esperadas basadas en tu imagen
        columnas_esperadas = [
            'fecha', 'cliente_nombre', 'cliente_ruc', 'concepto', 
            'monto', 'igv', 'total', 'email_cliente'
        ]
        
        # Verificar que existan las columnas necesarias
        columnas_faltantes = []
        for col in columnas_esperadas:
            if col not in self.recibos_ejemplos.columns:
                columnas_faltantes.append(col)
        
        if columnas_faltantes:
            logger.warning(f"⚠️ Columnas faltantes: {columnas_faltantes}")
            logger.info("📝 Columnas disponibles en el Excel:")
            for col in self.recibos_ejemplos.columns:
                logger.info(f"   - {col}")
        else:
            logger.info("✅ Todas las columnas necesarias están presentes")
        
        # Verificar datos vacíos
        filas_con_datos_vacios = self.recibos_ejemplos.isnull().any(axis=1).sum()
        if filas_con_datos_vacios > 0:
            logger.warning(f"⚠️ {filas_con_datos_vacios} filas tienen datos vacíos")
        
        return len(columnas_faltantes) == 0
    
    def mostrar_resumen_datos(self):
        """Muestra un resumen de los datos cargados"""
        if self.recibos_ejemplos is None:
            logger.error("❌ No hay datos para mostrar")
            return
        
        print("\n" + "="*60)
        print("📊 RESUMEN DE DATOS CARGADOS")
        print("="*60)
        
        # Mostrar las primeras filas
        print("\n🔍 Primeras 3 filas:")
        print(self.recibos_ejemplos.head(3).to_string(index=False))
        
        # Estadísticas básicas
        if 'total' in self.recibos_ejemplos.columns:
            total_general = self.recibos_ejemplos['total'].sum()
            print(f"\n💰 Total general: S/ {total_general:,.2f}")
            print(f"📈 Monto promedio: S/ {self.recibos_ejemplos['total'].mean():,.2f}")
            print(f"🎯 Cantidad de recibos: {len(self.recibos_ejemplos)}")
        
        # Fechas
        if 'fecha' in self.recibos_ejemplos.columns:
            try:
                # Convertir fechas si no están en formato datetime
                if not pd.api.types.is_datetime64_any_dtype(self.recibos_ejemplos['fecha']):
                    self.recibos_ejemplos['fecha'] = pd.to_datetime(self.recibos_ejemplos['fecha'])
                
                fecha_min = self.recibos_ejemplos['fecha'].min().strftime('%d/%m/%Y')
                fecha_max = self.recibos_ejemplos['fecha'].max().strftime('%d/%m/%Y')
                print(f"📅 Rango de fechas: {fecha_min} - {fecha_max}")
            except:
                print("📅 Fechas: No se pudieron procesar")
    
    def obtener_registro_por_indice(self, indice):
        """
        Obtiene un registro específico por su índice
        
        Args:
            indice (int): Índice del registro
            
        Returns:
            dict: Diccionario con los datos del registro
        """
        if self.recibos_ejemplos is None:
            return None
        
        if indice >= len(self.recibos_ejemplos):
            logger.error(f"❌ Índice {indice} fuera de rango")
            return None
        
        registro = self.recibos_ejemplos.iloc[indice].to_dict()
        return registro
    
    def procesar_todos_los_recibos(self):
        """
        Procesa todos los recibos (aquí irá la lógica de SUNAT)
        """
        if self.recibos_ejemplos is None:
            logger.error("❌ No hay datos para procesar")
            return
        
        logger.info("🚀 Iniciando procesamiento de recibos...")
        
        for indice, fila in self.recibos_ejemplos.iterrows():
            logger.info(f"📄 Procesando recibo {indice + 1}/{len(self.recibos_ejemplos)}")
            logger.info(f"   Cliente: {fila['cliente_nombre']}")
            logger.info(f"   Monto: S/ {fila['total']}")
            
            # Aquí irá la lógica de automatización con Selenium
            # self.generar_recibo_sunat(fila)
            
        logger.info("✅ Procesamiento completado")

def main():
    """Función principal del bot"""
    logger.info("🚀 Iniciando Bot de Recibos por Honorarios")
    
    # Verificar ubicación actual y archivos
    import os
    print("🔍 DIAGNÓSTICO DE ARCHIVOS:")
    print(f"📂 Directorio actual: {os.getcwd()}")
    print(f"📁 Archivos en directorio actual:")
    for item in os.listdir('.'):
        print(f"   - {item}")
    
    # Verificar si existe la carpeta data
    if os.path.exists('data'):
        print(f"✅ Carpeta 'data' encontrada")
        if os.path.exists('data/input'):
            print(f"✅ Carpeta 'data/input' encontrada")
            print(f"📁 Archivos en data/input:")
            for item in os.listdir('data/input'):
                print(f"   - {item}")
        else:
            print(f"❌ Carpeta 'data/input' NO encontrada")
    else:
        print(f"❌ Carpeta 'data' NO encontrada")
    
    print("=" * 60)
    print("🤖 BOT DE RECIBOS POR HONORARIOS")
    print("=" * 60)
    
    # Crear instancia del bot
    bot = BotRecibosHonorarios()  # Ahora usa la ruta por defecto
    
    # Verificar archivo
    if not bot.verificar_archivo_excel():
        print("❌ No se puede continuar sin el archivo Excel")
        return
    
    # Leer datos del Excel
    if not bot.leer_excel():
        print("❌ Error al leer el archivo Excel")
        return
    
    # Validar estructura de datos
    if not bot.validar_datos():
        print("⚠️ Advertencia: La estructura de datos puede tener problemas")
    
    # Mostrar resumen
    bot.mostrar_resumen_datos()
    
    # Preguntar si proceder
    print("\n" + "="*60)
    respuesta = input("¿Deseas procesar todos los recibos? (si/no): ").lower()
    
    if respuesta == 'si':
        bot.procesar_todos_los_recibos()
    else:
        print("👋 Proceso cancelado por el usuario")
    
    logger.info("✅ Bot ejecutado exitosamente")

if __name__ == "__main__":
    main()