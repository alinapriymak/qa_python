import pytest

from main import BooksCollector


# фикстура для создания экземпляра класса BooksCollector()
@pytest.fixture
def collector():
    return BooksCollector()
    
# фикстура для создания экземпляра со списком книг 
@pytest.fixture
def collector_with_books(collector):
    collector.add_new_book('Гордость и предубеждение и зомби')
    collector.add_new_book('Что делать, если ваш кот хочет вас убить')
    collector.add_new_book('Трое в лодке')
    collector.add_new_book('Божественная комедия')
    collector.add_new_book('Властелин колец')
        
    collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
    collector.set_book_genre('Что делать, если ваш кот хочет вас убить', 'Детективы')
    collector.set_book_genre('Трое в лодке', 'Комедии')
    collector.set_book_genre('Божественная комедия', 'Комедии')
    collector.set_book_genre('Властелин колец', 'Фантастика')
        
    return collector