# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Configuracion(models.Model):
    id_configuracion = models.AutoField(primary_key=True)
    id_inventario = models.ForeignKey('Inventario', models.DO_NOTHING, db_column='id_inventario')
    descripcion = models.TextField(blank=True, null=True)
    parametros_personalizados = models.TextField(blank=True, null=True)
    ultima_actualizacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'configuracion'


class Dependencia(models.Model):
    id_dependencia = models.AutoField(primary_key=True)
    nombre_dependencia = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    contacto = models.CharField(max_length=255, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dependencia'


class DetallesTecnicos(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_inventario = models.ForeignKey('Inventario', models.DO_NOTHING, db_column='id_inventario')
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    numero_serie = models.CharField(unique=True, max_length=255)
    sistema_operativo = models.CharField(max_length=100, blank=True, null=True)
    version_firmware = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalles_tecnicos'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Enlaces(models.Model):
    id_enlace = models.AutoField(primary_key=True)
    dispositivo_origen = models.ForeignKey('Inventario', models.DO_NOTHING, db_column='dispositivo_origen')
    dispositivo_destino = models.ForeignKey('Inventario', models.DO_NOTHING, db_column='dispositivo_destino', related_name='enlaces_dispositivo_destino_set')
    estado = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enlaces'


class HistorialCambios(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_inventario = models.ForeignKey('Inventario', models.DO_NOTHING, db_column='id_inventario')
    fecha_cambio = models.DateField(blank=True, null=True)
    cambio_realizado = models.TextField(blank=True, null=True)
    realizado_por = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historial_cambios'


class Incidentes(models.Model):
    id_incidentes = models.AutoField(primary_key=True)
    id_inventario = models.ForeignKey('Inventario', models.DO_NOTHING, db_column='id_inventario')
    fecha_mantenimiento = models.DateField(blank=True, null=True)
    tipo_mantenimiento = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    realizado_por = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'incidentes'


class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo_elemento = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    fecha_adquisicion = models.DateField(blank=True, null=True)
    id_ubicacion = models.ForeignKey('Ubicacion', models.DO_NOTHING, db_column='id_ubicacion')
    ip = models.CharField(unique=True, max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario'


class InventarioDispositivo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo_elemento = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    fecha_adquisicion = models.DateField()
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=255)
    sistema_operativo = models.CharField(max_length=255, blank=True, null=True)
    version_firmware = models.CharField(max_length=255, blank=True, null=True)
    descripcion_configuracion = models.TextField(blank=True, null=True)
    parametros_personalizados = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField()
    ubicacion = models.ForeignKey('Ubicacion', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario_dispositivo'


class Monitoreo(models.Model):
    id_monitoreo = models.AutoField(primary_key=True)
    id_inventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='id_inventario')
    fecha_hora = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitoreo'


class RutaDispositivos(models.Model):
    id = models.AutoField(primary_key=True)
    id_ruta = models.ForeignKey('Rutas', models.DO_NOTHING, db_column='id_ruta')
    id_inventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='id_inventario')
    orden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ruta_dispositivos'


class Rutas(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    nombre_ruta = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rutas'


class Ubicacion(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    nombre_ubicacion = models.CharField(max_length=255)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ubicacion'


class UbicacionDependencia(models.Model):
    id_ubicacion = models.OneToOneField(Ubicacion, models.DO_NOTHING, db_column='id_ubicacion', primary_key=True)  # The composite primary key (id_ubicacion, id_dependencia) found, that is not supported. The first column is selected.
    id_dependencia = models.ForeignKey(Dependencia, models.DO_NOTHING, db_column='id_dependencia')

    class Meta:
        managed = False
        db_table = 'ubicacion_dependencia'
        unique_together = (('id_ubicacion', 'id_dependencia'),)
