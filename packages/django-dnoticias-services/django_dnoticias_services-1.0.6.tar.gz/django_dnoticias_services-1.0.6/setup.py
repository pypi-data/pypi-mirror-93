from setuptools import find_packages, setup

setup(
    name="django_dnoticias_services",
    version='1.0.6',
    url="https://www.dnoticias.pt/",
    author="Pedro Mendes",
    author_email="pedro.trabalho.uma@gmail.com",
    license="MIT",
    install_requires=[
        'requests',
        'django',
        'python-keycloak',
        'mozilla-django-oidc'
    ],
    packages=find_packages(),
)
