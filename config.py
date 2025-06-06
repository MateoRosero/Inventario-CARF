import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cambia_esto_por_una_clave_segura')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql://root:mateorosero30@localhost:3306/inventario_carf'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOADED_IMAGES_DEST = os.path.join(BASE_DIR, 'static', 'uploads')
