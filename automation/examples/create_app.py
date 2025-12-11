import os
import sys
from pathlib import Path
import subprocess


def create_app(app_name):
    project_root = Path(__file__).resolve().parent / "django_example_project"
    
    # Créer le répertoire du projet s'il n'existe pas
    project_root.mkdir(parents=True, exist_ok=True)

    print(f"🚀 Création de l'app Django : {app_name}")

    # Créer l'app Django
    result = subprocess.run(
        [sys.executable, "-m", "django", "startapp", app_name, str(project_root / app_name)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Erreur lors de la création de l'app Django : {result.stderr}")
        # Si Django échoue, créer la structure manuellement
        app_path = project_root / app_name
        app_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Création manuelle du répertoire de l'app : {app_path}")

    app_path = project_root / app_name

    # Structure avancée obligatoire pour chaque app
    required_dirs = [
        "services",
        "repositories", 
        "tests",
        "use_cases"
    ]

    for d in required_dirs:
        path = app_path / d
        path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Dossier créé : {path}")

    # Création automatique des fichiers standards
    standard_files = {
        "services/__init__.py": "",
        "repositories/__init__.py": "",
        "use_cases/__init__.py": "", 
        "tests/__init__.py": "",
        "tests/test_app.py": "def test_placeholder(): assert True",
        "__init__.py": "",
        "apps.py": f"""
from django.apps import AppConfig

class {app_name.title().replace('_', '')}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app_name}'
"""
    }

    for file, content in standard_files.items():
        file_path = app_path / file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"📄 Fichier créé : {file_path}")

    print("\n🎉 App Django conforme créée avec succès !")
    print(f"📍 Emplacement : {app_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage : python create_app.py <nom_de_l_app>")
        sys.exit(1)

    app_name = sys.argv[1]
    create_app(app_name)