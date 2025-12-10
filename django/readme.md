# 🎬 **COURS COMPLET — Django 6.0 : Toutes les nouveautés, explications, sigles, exemples (comparé à Django 5.2)**

🎯 **Objectif : que même un débutant comprenne, et qu’un expert soit satisfait.**

* **chaque changement de Django 6.0**
* **pourquoi il existe**
* **ce que cela change dans les projets réels**
* **les sigles techniques expliqués clairement**
* **des exemples complets de code**
* **des comparaisons Django 5.2 → Django 6.0**

---

# 🟥 I. INTRODUCTION

Django 6.0 est une version **majeure**, ce qui signifie :
➡️ Ajout de fonctionnalités **nouvelles**
➡️ Suppression de fonctionnalités **anciennes ou dangereuses**
➡️ Mise à jour de dépendances importantes
➡️ Améliorations de performance
➡️ Changements qui peuvent casser un projet existant (**breaking changes**)

---

# 🟦 II. LES SIGLES IMPORTANTS À CONNAÎTRE

Avant d’entrer dans les nouveautés, voici les sigles que Django utilise souvent :

| Sigle      | Signification                            | Explication                                                               |
| ---------- | ---------------------------------------- | ------------------------------------------------------------------------- |
| **CSP**    | Content Security Policy                  | Politique de sécurité empêchant l’injection de scripts malveillants (XSS) |
| **XSS**    | Cross-Site Scripting                     | Attaque où un hacker injecte du JavaScript dans ton site                  |
| **ASGI**   | Asynchronous Server Gateway Interface    | Interface moderne permettant les vues asynchrones                         |
| **ORM**    | Object Relational Mapper                 | Système convertissant les modèles Python en SQL                           |
| **SGBD**   | Système de Gestion de Base de Données    | Exemple : PostgreSQL, SQLite, MySQL                                       |
| **PBKDF2** | Password-Based Key Derivation Function 2 | Algorithme de hachage sécurisé pour les mots de passe                     |

Maintenant que tout est clair, allons dans le vif du sujet.

---

# 🟩 III. COMPATIBILITÉ PYTHON — Django devient plus rapide et plus strict

## 🔥 Changement :

* Django 5.2 supportait : **Python 3.10–3.12**
* Django 6 supporte : **Python 3.12, 3.13, 3.14**

## ❓ Pourquoi ce changement ?

Python 3.12+ apporte :

* Jusqu’à **50% de performance en plus** dans certaines opérations.
* Une nouvelle manière d’exécuter le code (PEP 709, PEP 684).
* Une meilleure gestion de la mémoire.

Django exploite ces avancées.

## 🎯 Conséquence :

➡️ Tous les projets doivent être migrés vers Python ≥ 3.12
➡️ Les packages non compatibles doivent être mis à jour.

---

# 🟩 IV. NOUVEAUTÉ 1 — Content Security Policy (CSP)

La **CSP** (Content Security Policy) protège ton site contre les attaques **XSS**.

### ⭐ Nouveau dans Django 6 :

✔️ Middleware intégré
✔️ Gestion des nonces
✔️ Paramétrage simple via `SECURE_CSP`

---

## 🔍 Exemple réel d’attaque XSS (pour expliquer) :

Une zone de texte non sécurisée permet :

```html
<script>alert('Vous êtes piraté')</script>
```

Avec CSP, Django refuse ce script.

---

## ✔️ Exemple Django 6 :

```python
# settings.py

SECURE_CSP = {
    "default-src": ["'self'"],
    "script-src": ["'self'", "'nonce'"],
}
```

---

## 📌 Exemple d’intégration dans un template :

```django
<script nonce="{{ request.csp_nonce }}">
    console.log("Script autorisé !");
</script>
```

---

## 🎯 Ce que cela change :

* Sécurité renforcée dès l’installation
* Moins besoin de bibliothèques externes
* Conformité aux normes modernes (RGPD, OWASP)

---

# 🟩 V. NOUVEAUTÉ 2 — Template Partials

C’est l’une des innovations **les plus importantes**.

Avant Django 6 → très difficile de créer des composants HTML réutilisables.

Maintenant → **Django se rapproche de React / Vue / Angular**.

---

## ✔️ Exemple AVANT (Django 5.2) :

Tu devais créer `card.html` :

```django
<div class="card">
  <h3>{{ title }}</h3>
  <p>{{ text }}</p>
</div>
```

Et ensuite :

```django
{% include "card.html" with title="Salut" text="Bienvenue" %}
```

---

## ✔️ Exemple Django 6 — PARTIAL :

```django
{% partialdef card title, text %}
    <div class="card">
        <h3>{{ title }}</h3>
        <p>{{ text }}</p>
    </div>
{% endpartialdef %}
```

Pour appeler :

```django
{% partial card title="Bienvenue" text="Voici un composant" %}
```

---

## 🎯 Ce que cela change :

* Plusieurs composants dans un seul fichier
* Code mieux organisé
* Réutilisation plus facile
* Moins de duplication

C’est excellent pour :

* dashboards
* systèmes multitenants
* formulaires complexes
* interfaces modernes

---

# 🟩 VI. NOUVEAUTÉ 3 — Background Tasks (Tâches en arrière-plan)

Django introduit un système **simple et natif**.

### ⭐ Pourquoi ?

Dans Django 5.2 → aucune solution interne
Il fallait installer **Celery**, **Redis**, **RabbitMQ**, etc.

Maintenant → beaucoup plus simple.

---

## ✔️ Exemple Django 6 :

```python
from django.tasks import task

@task
def envoyer_email(users):
    print("Email envoyé à", users)
```

Pour exécuter :

```python
envoyer_email.enqueue(["demo@gmail.com"])
```

---

## 🎯 Ce que ça change :

* Plus besoin de Celery pour les tâches simples
* Plus facile pour les débutants
* Plus rapide à configurer
* Meilleure intégration avec Django

> ⚠️ Pour des tâches lourdes ou complexes → Celery reste conseillé.

---

# 🟩 VII. NOUVEAUTÉ 4 — API Email modernisée

Django abandonne l’ancien système MIME qui avait 15 ans.

### ⭐ Pourquoi ?

* Bugs fréquents
* Mauvaise gestion des encodages
* Code difficile à maintenir
* Python a introduit une API moderne depuis 3.6

---

## ✔️ Exemple Django 6 :

```python
from django.core.mail import EmailMessage

email = EmailMessage(
    subject="Bienvenue",
    body="Merci pour votre inscription",
    to=["test@example.com"]
)
email.send()
```

---

## 🎯 Ce que cela change :

* emails plus propres
* meilleure gestion des pièces jointes
* support Unicode complet
* compatibilité meilleure avec Gmail / AWS SES / Mailgun / Sendinblue

---

# 🟩 VIII. NOUVEAUTÉ 5 — ORM amélioré

## 1) StringAgg maintenant multi-base

Avant → réservé à PostgreSQL

Exemple :

```python
from django.db.models import StringAgg

Auteur.objects.aggregate(
    liste=StringAgg("nom", ", ")
)
```

🎯 Conséquence :
→ Fonctionne même sous SQLite.

---

## 2) order_by dans les agrégations

Nouvelle possibilité :

```python
StringAgg("nom", ",", order_by="nom")
```

Avant → impossible sans hack.

🎯 Impact :
→ Les résultats sont enfin **ordonnés comme tu veux**.

---

## 3) JSONField : support index négatif sous SQLite

Exemple :

```python
personne.data["hobbies"][-1]
```

🎯 Impact :
→ Tests locaux fidèles à la prod (PostgreSQL).

---

# 🟩 IX. ADMIN — Mise à jour des icônes

Django 6 utilise maintenant **FontAwesome 6.7.2**.

---

## 🎯 Ce que cela change :

* icônes plus belles
* plus de choix
* interface plus moderne
* meilleure accessibilité

---

# 🟩 X. BREAKING CHANGES — Les choses qui disparaissent

## ❌ 1. DEFAULT_AUTO_FIELD devient BigAutoField

ID automatique passe de :

* 32 bits → Django 5
* 64 bits → Django 6

🎯 Pourquoi ?
→ plus d’espace pour les grandes bases de données.

---

## ❌ 2. Méthodes internes ORM supprimées

Exemples supprimés :

* `get_joining_columns()`
* `get_reverse_joining_columns()`

🎯 Pourquoi ?
→ Ces méthodes n’étaient pas stables et empêchaient des améliorations internes.

---

## ❌ 3. MariaDB 10.5 n’est plus supporté

→ minimum maintenant = **10.6**

---

## ❌ 4. Ancienne API email supprimée

→ passage obligatoire à la nouvelle API Python

---

# 🟩 XI. MIGRATION — Comment passer de Django 5.2 → Django 6

## 1️⃣ Mettre Python en 3.12+

## 2️⃣ Mettre à jour les dépendances

## 3️⃣ Activer les warnings :

```bash
python -Wd manage.py runserver
```

## 4️⃣ Vérifier les emails

## 5️⃣ Vérifier l’ORM si tu as du code personnalisé

## 6️⃣ Tester les templates (partials)

## 7️⃣ Vérifier les IDs auto (BigAutoField)

---

# 🟦 XII. CONCLUSION — Pourquoi Django 6 est une révolution

✔️ Plus sécurisé (CSP)
✔️ Plus moderne (partials)
✔️ Plus rapide (Python 3.12+)
✔️ Plus simple (tâches natives)
✔️ Plus puissant (ORM amélioré)
✔️ Plus élégant (admin modernisé)
✔️ Plus propre (suppression du legacy)

**Django reste l’un des frameworks les plus robustes et professionnels au monde.**
