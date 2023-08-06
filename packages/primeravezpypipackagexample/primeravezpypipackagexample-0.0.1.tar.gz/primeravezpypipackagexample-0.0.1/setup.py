# Serie de parametros imprescindibles

from setuptools import setup, find_packages

# introducimos la configuracion
setup(
    name= "primeravezpypipackagexample" ,
    version= "0.0.1",
    licence= "MIT" ,
    description= "paquete de prueba" ,
    author= "Micaela C Bergmann" ,
    packages= find_packages() ,
    url= "https://github.com/MicaBergmann/pypipackageexample"
)

# Para setup
# nombre que le queremos poner, la version de python, la licencia siempre es MIT, la descripcion que queramos poner, nuestro nombre de autores
# En el caso de que hayamos usado paquetes, se deban instalar. Para ello se coloca install_requires
# A modo de ejemplo, si usamos "math" seria: install_requires= ["math"]
# los mas importantes son: name, version, licence y url
# url es el creado en GitHub: para que agarre el repositorio y lo traiga ahi
# para eso vas a GitHub seleccionas el paquete y copias el link/url de la pagina
# Por ultimo, arriba instalamos tambien find_packages. Importante este comando porque ayuda a buscar los subpaquetes que tenemos compuestos y el paquete principal de nuestro repositorio