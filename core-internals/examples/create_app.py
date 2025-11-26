
import os
import sys
from pathlib import Path
import subprocess


def create_app(app_name):
    project_root = Path(__file__).resolve().parent / "django_example_project"

    print(f"🚀 Création de l'app Django : {app_name}")

    subprocess.run([sys.executable, "-m", "django", "startapp", app_name, str(project_root / app_name)])

    # Structure avancée obligatoire pour chaque app
    required_dirs = [
        "services",
        "repositories",
        "tests",
        "use_cases"
    ]

    app_path = project_root / app_name

    for d in required_dirs:
        path = app_path / d
        path.mkdir(exist_ok=True)
        print(f"📁 Dossier créé : {path}")

    # Création automatique d'un fichier standard services.py, repository.py etc.
    standard_files = {
        "services/__init__.py": "",
        "repositories/__init__.py": "",
        "use_cases/__init__.py": "",
        "tests/__init__.py": "",
        "tests/test_app.py": "def test_placeholder(): assert True"
    }

    for file, content in standard_files.items():
        file_path = app_path / file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Fichier créé : {file_path}")

    print("\n🎉 App Django conforme créée avec succès !")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage : python create_app.py <nom_de_l_app>")
        sys.exit(1)

    app_name = sys.argv[1]
    create_app(app_name)
