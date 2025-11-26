"""
Factory para crear datos de prueba de solicitudes.
Puede ser usado en Django TestCase o como comando de gestión.
"""
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()
from tipo_solicitudes.models import (
    TipoSolicitud, FormularioSolicitud, CampoFormulario,
    Solicitud, RespuestaCampo, SeguimientoSolicitud, ArchivoAdjunto
)
import random
from datetime import timedelta


class SolicitudTestDataFactory:
    """Factory para crear datos de prueba de solicitudes."""

    def __init__(self):
        self.usuarios = []
        self.tipos_solicitud = []
        self.formularios = []
        self.solicitudes = []
        self._folio_counter = 0

    def crear_usuarios(self, cantidad=5):
        """Crea usuarios de prueba."""
        usuarios_data = [
            {'username': 'estudiante1', 'email': 'est1@example.com', 'first_name': 'Juan', 'last_name': 'Pérez'},
            {'username': 'estudiante2', 'email': 'est2@example.com', 'first_name': 'María', 'last_name': 'García'},
            {'username': 'estudiante3', 'email': 'est3@example.com', 'first_name': 'Carlos', 'last_name': 'López'},
            {'username': 'profesor1', 'email': 'prof1@example.com', 'first_name': 'Ana', 'last_name': 'Martínez'},
            {'username': 'admin1', 'email': 'admin@example.com', 'first_name': 'Pedro', 'last_name': 'Sánchez'},
        ]

        for i in range(min(cantidad, len(usuarios_data))):
            data = usuarios_data[i]
            usuario, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                }
            )
            if created:
                usuario.set_password('password123')
                usuario.save()
            self.usuarios.append(usuario)

        return self.usuarios

    def crear_tipos_solicitud(self):
        """Crea tipos de solicitud con sus formularios."""
        tipos_data = [
            {
                'nombre': 'Constancia de Estudios',
                'descripcion': 'Solicitud de constancia que acredita que el alumno está inscrito',
                'responsable': '1',  # Control escolar
                'campos': [
                    {'nombre': 'motivo', 'etiqueta': 'Motivo de la solicitud', 'tipo': 'textarea', 'requerido': True},
                    {'nombre': 'semestre', 'etiqueta': 'Semestre actual', 'tipo': 'select', 'opciones': '1,2,3,4,5,6,7,8,9', 'requerido': True},
                    {'nombre': 'fecha_necesaria', 'etiqueta': 'Fecha en que necesita el documento', 'tipo': 'date', 'requerido': True},
                ]
            },
            {
                'nombre': 'Cambio de Grupo',
                'descripcion': 'Solicitud para cambiar de grupo en una materia',
                'responsable': '2',  # Responsable de programa
                'campos': [
                    {'nombre': 'materia', 'etiqueta': 'Nombre de la materia', 'tipo': 'text', 'requerido': True},
                    {'nombre': 'grupo_actual', 'etiqueta': 'Grupo actual', 'tipo': 'text', 'requerido': True},
                    {'nombre': 'grupo_deseado', 'etiqueta': 'Grupo deseado', 'tipo': 'text', 'requerido': True},
                    {'nombre': 'justificacion', 'etiqueta': 'Justificación', 'tipo': 'textarea', 'requerido': True},
                    {'nombre': 'horario_actual', 'etiqueta': 'Horario actual', 'tipo': 'file', 'requerido': False},
                ]
            },
            {
                'nombre': 'Asesoría Académica',
                'descripcion': 'Solicitud de asesoría o tutoría académica',
                'responsable': '3',  # Responsable de tutorías
                'campos': [
                    {'nombre': 'materia', 'etiqueta': 'Materia', 'tipo': 'text', 'requerido': True},
                    {'nombre': 'tema', 'etiqueta': 'Tema específico', 'tipo': 'textarea', 'requerido': True},
                    {'nombre': 'tipo_asesoria', 'etiqueta': 'Tipo de asesoría', 'tipo': 'select', 'opciones': 'Individual,Grupal,En línea,Presencial', 'requerido': True},
                    {'nombre': 'disponibilidad', 'etiqueta': 'Disponibilidad horaria', 'tipo': 'textarea', 'requerido': True},
                ]
            },
            {
                'nombre': 'Baja de Materia',
                'descripcion': 'Solicitud para dar de baja una materia',
                'responsable': '4',  # Director
                'campos': [
                    {'nombre': 'materia', 'etiqueta': 'Nombre de la materia', 'tipo': 'text', 'requerido': True},
                    {'nombre': 'grupo', 'etiqueta': 'Grupo', 'tipo': 'text', 'requerido': True},
                    {'nombre': 'motivo', 'etiqueta': 'Motivo de la baja', 'tipo': 'textarea', 'requerido': True},
                    {'nombre': 'documentos', 'etiqueta': 'Documentos de respaldo', 'tipo': 'file', 'requerido': False, 'cantidad_archivos': 3},
                ]
            },
            {
                'nombre': 'Carta de Recomendación',
                'descripcion': 'Solicitud de carta de recomendación',
                'responsable': '2',  # Responsable de programa
                'campos': [
                    {'nombre': 'proposito', 'etiqueta': 'Propósito de la carta', 'tipo': 'select', 'opciones': 'Beca,Empleo,Intercambio,Maestría,Otro', 'requerido': True},
                    {'nombre': 'destinatario', 'etiqueta': 'Destinatario', 'tipo': 'text', 'requerido': True},
                    {'nombre': 'fecha_entrega', 'etiqueta': 'Fecha de entrega necesaria', 'tipo': 'date', 'requerido': True},
                    {'nombre': 'informacion_adicional', 'etiqueta': 'Información adicional', 'tipo': 'textarea', 'requerido': False},
                ]
            },
        ]

        for tipo_data in tipos_data:
            campos = tipo_data.pop('campos')

            tipo, created = TipoSolicitud.objects.get_or_create(
                nombre=tipo_data['nombre'],
                defaults={
                    'descripcion': tipo_data['descripcion'],
                    'responsable': tipo_data['responsable'],
                }
            )
            self.tipos_solicitud.append(tipo)

            # Crear formulario
            formulario, created = FormularioSolicitud.objects.get_or_create(
                tipo_solicitud=tipo,
                defaults={
                    'nombre': f'Formulario {tipo.nombre}',
                    'descripcion': f'Formulario para {tipo.descripcion.lower()}',
                }
            )
            self.formularios.append(formulario)

            # Crear campos del formulario
            if created:
                for i, campo_data in enumerate(campos):
                    CampoFormulario.objects.create(
                        formulario=formulario,
                        nombre=campo_data['nombre'],
                        etiqueta=campo_data['etiqueta'],
                        tipo=campo_data['tipo'],
                        requerido=campo_data['requerido'],
                        opciones=campo_data.get('opciones', ''),
                        cantidad_archivos=campo_data.get('cantidad_archivos', 1),
                        orden=i + 1
                    )

        return self.tipos_solicitud

    def generar_folio(self):
        """Genera un folio único para una solicitud."""
        import uuid
        # Usar UUID para garantizar unicidad
        unique_id = uuid.uuid4().hex[:12].upper()
        self._folio_counter += 1
        return f'SOL-{unique_id}-{self._folio_counter:04d}'

    def crear_archivo_prueba(self, nombre_archivo, tipo_archivo='txt'):
        """Crea un archivo de prueba con contenido."""
        contenidos = {
            'txt': 'Este es un archivo de prueba generado automáticamente.\nContenido de ejemplo para testing.\n',
            'pdf': b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/Resources <<\n/Font <<\n/F1 <<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\n>>\n>>\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Documento de prueba) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000314 00000 n\ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n408\n%%EOF',
            'jpg': b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xff\xd9',
        }

        if tipo_archivo in contenidos:
            contenido = contenidos[tipo_archivo]
        else:
            contenido = f'Archivo de prueba: {nombre_archivo}\n'.encode('utf-8')

        if isinstance(contenido, str):
            contenido = contenido.encode('utf-8')

        from django.core.files.base import ContentFile
        return ContentFile(contenido, name=nombre_archivo)

    def crear_solicitudes(self, cantidad=15):
        """Crea solicitudes de ejemplo con respuestas."""
        if not self.usuarios:
            self.crear_usuarios()
        if not self.tipos_solicitud:
            self.crear_tipos_solicitud()

        respuestas_ejemplo = {
            'Constancia de Estudios': {
                'motivo': [
                    'Necesito la constancia para trámite de beca',
                    'Requerida para solicitud de empleo',
                    'Trámite de seguro médico',
                    'Para participar en concurso académico',
                ],
                'semestre': ['3', '5', '7', '4', '6'],
                'fecha_necesaria': lambda: (timezone.now() + timedelta(days=random.randint(7, 30))).strftime('%Y-%m-%d'),
            },
            'Cambio de Grupo': {
                'materia': ['Programación Web', 'Base de Datos', 'Cálculo Diferencial', 'Inglés IV'],
                'grupo_actual': ['A', 'B', 'C'],
                'grupo_deseado': ['B', 'A', 'C'],
                'justificacion': [
                    'Conflicto de horario con otra materia',
                    'Problemas de transporte en ese horario',
                    'Necesito un horario más compatible con mi trabajo',
                ],
            },
            'Asesoría Académica': {
                'materia': ['Matemáticas', 'Física', 'Programación', 'Química'],
                'tema': [
                    'Derivadas e integrales',
                    'Estructuras de datos - Árboles binarios',
                    'Leyes de Newton y aplicaciones',
                    'Reacciones químicas',
                ],
                'tipo_asesoria': ['Individual', 'Grupal', 'En línea'],
                'disponibilidad': ['Lunes y miércoles por la tarde', 'Martes y jueves por la mañana', 'Viernes todo el día'],
            },
            'Baja de Materia': {
                'materia': ['Estadística', 'Programación Avanzada', 'Electrónica'],
                'grupo': ['A', 'B', 'C'],
                'motivo': [
                    'Por motivos de salud no puedo continuar',
                    'Situación laboral que requiere mi atención',
                    'No tengo los conocimientos previos necesarios',
                ],
            },
            'Carta de Recomendación': {
                'proposito': ['Beca', 'Empleo', 'Maestría', 'Intercambio'],
                'destinatario': ['Comité de becas', 'Departamento de Recursos Humanos', 'Universidad Nacional', 'Comité de selección'],
                'fecha_entrega': lambda: (timezone.now() + timedelta(days=random.randint(10, 45))).strftime('%Y-%m-%d'),
                'informacion_adicional': [
                    'He participado en proyectos de investigación',
                    'Tengo promedio de 9.5',
                    'Certificaciones en el área',
                    '',
                ],
            },
        }

        estados = ['1', '2', '3']  # Creada, En proceso, Terminada

        for i in range(cantidad):
            usuario = random.choice(self.usuarios)
            tipo = random.choice(self.tipos_solicitud)

            # Crear solicitud
            solicitud = Solicitud.objects.create(
                usuario=usuario,
                tipo_solicitud=tipo,
                folio=self.generar_folio(),
            )
            self.solicitudes.append(solicitud)

            # Crear respuestas para los campos del formulario
            formulario = tipo.formulario
            campos = formulario.campos.all()

            respuestas_tipo = respuestas_ejemplo.get(tipo.nombre, {})

            for campo in campos:
                if campo.tipo != 'file':  # Los archivos los manejamos aparte
                    valor = ''
                    if campo.nombre in respuestas_tipo:
                        opciones = respuestas_tipo[campo.nombre]
                        if callable(opciones):
                            valor = opciones()
                        else:
                            valor = random.choice(opciones)

                    RespuestaCampo.objects.create(
                        solicitud=solicitud,
                        campo=campo,
                        valor=valor
                    )
                else:
                    # Crear campos de archivo con archivos adjuntos reales
                    respuesta_campo = RespuestaCampo.objects.create(
                        solicitud=solicitud,
                        campo=campo,
                        valor=''
                    )

                    # Crear archivos adjuntos (algunos formularios permiten múltiples archivos)
                    cantidad_archivos = random.randint(1, min(campo.cantidad_archivos, 3))
                    tipos_archivo = ['pdf', 'txt', 'jpg']
                    extensiones = {'pdf': 'pdf', 'txt': 'txt', 'jpg': 'jpg'}

                    for j in range(cantidad_archivos):
                        tipo_elegido = random.choice(tipos_archivo)
                        ext = extensiones[tipo_elegido]
                        nombre_archivo = f'{campo.nombre}_{j+1}.{ext}'

                        archivo_content = self.crear_archivo_prueba(nombre_archivo, tipo_elegido)

                        archivo_adjunto = ArchivoAdjunto.objects.create(
                            solicitud=solicitud,
                            respuesta=respuesta_campo,
                            nombre=nombre_archivo
                        )
                        archivo_adjunto.archivo.save(nombre_archivo, archivo_content, save=True)

            # Crear seguimiento inicial
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estatus='1',  # Creada
                observaciones='Solicitud creada por el usuario'
            )

            # Algunos pueden tener seguimientos adicionales
            if random.random() > 0.5:
                # Agregar seguimiento "En proceso"
                SeguimientoSolicitud.objects.create(
                    solicitud=solicitud,
                    estatus='2',
                    observaciones=random.choice([
                        'La solicitud está siendo revisada',
                        'Se requiere documentación adicional',
                        'En espera de aprobación del coordinador',
                        'Procesando la solicitud',
                    ])
                )

                # Algunos pueden estar terminados
                if random.random() > 0.6:
                    SeguimientoSolicitud.objects.create(
                        solicitud=solicitud,
                        estatus='3',
                        observaciones=random.choice([
                            'Solicitud aprobada y procesada',
                            'Documento entregado al solicitante',
                            'Trámite completado exitosamente',
                            'Solicitud finalizada',
                        ])
                    )

        return self.solicitudes

    def limpiar_datos(self):
        """Elimina todos los datos de prueba creados."""
        # Eliminar archivos físicos primero
        for archivo in ArchivoAdjunto.objects.all():
            if archivo.archivo:
                archivo.archivo.delete(save=False)

        Solicitud.objects.all().delete()
        CampoFormulario.objects.all().delete()
        FormularioSolicitud.objects.all().delete()
        TipoSolicitud.objects.all().delete()
        # Opcionalmente eliminar usuarios de prueba
        User.objects.filter(username__startswith='estudiante').delete()
        User.objects.filter(username__startswith='profesor').delete()
        User.objects.filter(username='admin1').delete()

    def crear_datos_completos(self, usuarios=5, solicitudes=15):
        """Crea un conjunto completo de datos de prueba."""
        print(f'Creando {usuarios} usuarios...')
        self.crear_usuarios(usuarios)
        print(f'✓ {len(self.usuarios)} usuarios creados')

        print('Creando tipos de solicitud y formularios...')
        self.crear_tipos_solicitud()
        print(f'✓ {len(self.tipos_solicitud)} tipos de solicitud creados')

        print(f'Creando {solicitudes} solicitudes...')
        self.crear_solicitudes(solicitudes)
        print(f'✓ {len(self.solicitudes)} solicitudes creadas')

        return {
            'usuarios': self.usuarios,
            'tipos_solicitud': self.tipos_solicitud,
            'formularios': self.formularios,
            'solicitudes': self.solicitudes,
        }


def crear_datos_de_prueba(usuarios=5, solicitudes=15):
    """
    Función auxiliar para crear datos de prueba.
    Uso en TestCase:
        from atender_solicitudes.test_data_factory import crear_datos_de_prueba

        class MiTest(TestCase):
            def setUp(self):
                self.datos = crear_datos_de_prueba(usuarios=3, solicitudes=10)
    """
    factory = SolicitudTestDataFactory()
    return factory.crear_datos_completos(usuarios, solicitudes)


def limpiar_datos_de_prueba():
    """
    Función auxiliar para limpiar datos de prueba.
    Uso en TestCase:
        from atender_solicitudes.test_data_factory import limpiar_datos_de_prueba

        class MiTest(TestCase):
            def tearDown(self):
                limpiar_datos_de_prueba()
    """
    factory = SolicitudTestDataFactory()
    factory.limpiar_datos()
