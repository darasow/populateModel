import os
import django
from faker import Faker

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from authors.models import Author
from books.models import Book
from books.models import ISBN
from publishers.models import Publisher

fake = Faker()

def populate(num_authors=10, num_books=50, num_publishers=5):
    # Créer des éditeurs
    publishers = []
    for _ in range(num_publishers):
        publisher = Publisher.objects.create(name=fake.company())
        publishers.append(publisher)

    # Créer des auteurs
    authors = []
    for _ in range(num_authors):
        author = Author.objects.create(
            name=fake.name(),
            birthdate=fake.date_of_birth()  # Générer une date de naissance valide
        )
        authors.append(author)

    # Créer des livres
    for _ in range(num_books):
        # Créer une instance ISBN
        isbn_instance = ISBN.objects.create(code=fake.isbn13())

        # Créer le livre avec l'ISBN créé
        book = Book.objects.create(
            title=fake.sentence(nb_words=4),
            publication_date=fake.date(),
            summary=fake.text(),
            author=fake.random_element(authors),  # Assigner un auteur aléatoire
            isbn=isbn_instance,  # Utiliser l'instance ISBN
        )
        # Assigner des éditeurs aléatoires
        book.publishers.set(fake.random_elements(publishers, unique=True, length=fake.random_int(min=1, max=3)))

if __name__ == '__main__':
    print("Remplissage des modèles avec des données factices...")
    populate()
    print("Terminé.")
