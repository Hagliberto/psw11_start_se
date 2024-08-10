#!/usr/bin/env python
"""
Utilitário de linha de comando do Django para tarefas administrativas.
"""
import os
import sys


def main():
    """
    Executa as tarefas administrativas.
    """
    # Define o módulo de configurações do Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        # Importa a função execute_from_command_line do gerenciamento do Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Lança uma exceção se não for possível importar o Django
        raise ImportError(
            "Não foi possível importar o Django. Você tem certeza de que ele está "
            "instalado e disponível na sua variável de ambiente PYTHONPATH? Você "
            "esqueceu de ativar um ambiente virtual?"
        ) from exc
    # Executa o gerenciamento de linha de comando do Django
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()