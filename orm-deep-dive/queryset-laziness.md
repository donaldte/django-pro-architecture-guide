# 1.1 — Why is a Django QuerySet Lazy? / Pourquoi le QuerySet est “lazy” ?

A **Django QuerySet is lazy**: defining the query does **not** hit the database immediately.  
The SQL statement is only executed when the data is actually needed.

---

## 🔍 1. Concept: Lazy Evaluation

# The problem lazy evaluation solves

## example of bad code

```python
from django.contrib.auth import get_user_model
User = get_user_model()

qs = User.objects.filter(is_active=True)

# ❌ BAD: forces QuerySet evaluation too early
users = list(qs)     # Query executed here unnecessarily

# ❌ BAD: second iteration forces evaluation AGAIN (because list() was not needed)
for user in users:
    print(user.username)
```

## example of good code
```python
from django.contrib.auth import get_user_model
User = get_user_model()

qs = User.objects.filter(is_active=True)

# ✅ GOOD: QuerySet is lazy here — no SQL yet
for user in qs:
    # QuerySet is evaluated only at the FIRST iteration
    print(user.username)

```


When you write:

```python
from django.contrib.auth import get_user_model

User = get_user_model()

qs = User.objects.filter(is_active=True)  # No SQL query yet!
````

At this point:

* `qs` contains a **QuerySet object**
* Internally, it wraps a `Query` object (Django ORM internal representation)
* The SQL string is *prepared*, but **not executed**

The database is only hit when the QuerySet is **evaluated**.

---

## ⚙️ 2. When does a QuerySet actually execute?

A QuerySet triggers a real SQL query when you do one of the following:

* You **iterate** over it:

```sh
for user in qs:
    ...
```

* You **materialize** it into a concrete container:

```python
users = list(qs)
```

* You **access an element**:

```python
first_user = qs[0]
```

* You call **evaluation methods**:

```python
count = qs.count()
exists = qs.exists()
user = qs.first()
aggregate = qs.aggregate(...)
values = list(qs.values("id"))
```

Each of these actions forces Django to:

1. Compile the `QuerySet` into SQL
2. Send the query to the database
3. Fetch results into Python objects

---

## 🧪 3. Simple Example (Conceptual)

```python
from django.contrib.auth import get_user_model

User = get_user_model()

qs = User.objects.filter(is_active=True)  # NO SQL query yet

print("Before evaluation")
users = list(qs)  # SQL query is executed here
print("After evaluation, number of users:", len(users))
```

Internally:

* Before `list(qs)`: the ORM only holds a **description** of the query
* At `list(qs)`: the ORM performs the actual `SELECT ... FROM ... WHERE ...`

---

## 🎯 4. Why is laziness important?

Main advantages:

1. **Performance optimization**

   You can build complex queries step by step **without hitting the database**:

   ```python
   qs = User.objects.filter(is_active=True)
   qs = qs.filter(country="CA")
   qs = qs.select_related("profile")

   # Only now the query is executed:
   result = list(qs)
   ```

   Django composes all filters and options into a **single optimized SQL query**.

2. **Composability**

   You can pass QuerySets around (to services, repositories, etc.)
   and let the *consumer* decide when and how to evaluate them.

3. **Reusability**

   Lazy QuerySets allow you to define reusable building blocks:

   ```python
   active_users = User.objects.filter(is_active=True)

   canada_active_users = active_users.filter(country="CA")
   france_active_users = active_users.filter(country="FR")
   ```

---

## 🧪 5. Concrete Test in This Repo

See the example app:

```bash
orm-deep-dive/examples/django_example_project/queryset_laziness/
```

File:

```bash
tests/test_queryset_laziness.py
```

It uses `assertNumQueries` to **prove** that:

* Creating a QuerySet does **not** execute any query
* Evaluating it (e.g. `list(qs)`) executes exactly **one** SQL query

---

## 🔗 Next Steps

* 1.2 — How QuerySet caching works (in-memory cache after first evaluation)
* 1.3 — Chaining vs re-evaluating QuerySets
* 1.4 — Common pitfalls: forcing evaluation too early