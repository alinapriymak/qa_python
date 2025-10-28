import pytest
from main import BooksCollector

class TestBooksCollector:

    # фикстура для создания экземпляра класса BooksCollector()
    @pytest.fixture
    def collector(self):
        return BooksCollector()
    
    # фикстура для создания экземпляра со списком книг 
    @pytest.fixture
    def collector_with_books(self):
        collector = BooksCollector()
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
    

    # пример теста из прекода:
    #def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        #collector = BooksCollector()

        # добавляем две книги
        #collector.add_new_book('Гордость и предубеждение и зомби')
        #collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        #assert len(collector.get_books_genre()) == 2


    # проверяем добавление книги
    @pytest.mark.parametrize('book_name, expected', [
        ('Пролетая над гнездом кукушки', True), # обычное название
        ('А', True),  # минимальная длина
        ('А' * 39, True),  # проверка граничных значений допустимой длины
        ('А' * 40, True),  # максимальная длина
        ('А' * 41, False),  # проверка граничных значений невалидного класса
        ('А' * 42, False),  # проверка граничных значений, шаг внутрь невалидного класса
        ('А' * 100, False),  # проверка граничных значений
        ('', False),  # пустая строка
    ])
    def test_add_new_book(self, collector, book_name, expected):
        collector.add_new_book(book_name)
        assert (book_name in collector.get_books_genre()) == expected
    

    # негативная проверка на добавление одной и той же книги дважды 
    def test_add_new_book_cannot_add_same_book_twice(self, collector):
    
        collector.add_new_book('Над пропастью в пшенице')
        collector.add_new_book('Над пропастью в пшенице')

        books = collector.get_books_genre()
        assert 'Над пропастью в пшенице' in books
        assert len(books) == 1


    # проверяем установку жанра
    @pytest.mark.parametrize('genre, expected', [
        ('Фантастика', 'Фантастика'),
        ('Ужасы', 'Ужасы'),
        ('Детективы', 'Детективы'),
        ('Мультфильмы', 'Мультфильмы'),
        ('Комедии', 'Комедии'),
        ('Героический эпос', ''),
    ])
    def test_set_book_genre(self, collector, genre, expected):
        collector.add_new_book('Тестовая книга')
        collector.set_book_genre('Тестовая книга', genre)
        
        if genre in collector.genre:
            assert collector.get_book_genre('Тестовая книга') == expected
        else:
            assert collector.get_book_genre('Тестовая книга') == ''


    # проверяем вывод жанра по названию книги 
    @pytest.mark.parametrize('book_name, expected_genre', [
    ('Гордость и предубеждение и зомби', 'Ужасы'),
    ('Что делать, если ваш кот хочет вас убить', 'Детективы'),
    ('Трое в лодке', 'Комедии'),
    ('Властелин колец', 'Фантастика'),
    ])
    def test_get_book_genre_returns_genre(self, collector_with_books, book_name, expected_genre):
        result = collector_with_books.get_book_genre(book_name)
        assert result == expected_genre


    # проверяем вывод списка книг по жанру 
    @pytest.mark.parametrize('genre, expected_books', [
        ('Ужасы', ['Гордость и предубеждение и зомби']),
        ('Фантастика', ['Властелин колец']),
        ('Детективы', ['Что делать, если ваш кот хочет вас убить']),
        ('Мультфильмы', []),
        ('Комедии', ['Трое в лодке', 'Божественная комедия']),
        ('Несуществующий жанр', []),
    ])
    def test_get_books_with_specific_genre(self, collector_with_books, genre, expected_books):
        result = collector_with_books.get_books_with_specific_genre(genre)
        assert sorted(result) == sorted(expected_books)


    # проверяем вывод текущего словаря books_genre
    def test_get_books_genre_with_books(self, collector_with_books):
        books_genre = collector_with_books.get_books_genre()
        expected = {
            'Гордость и предубеждение и зомби': 'Ужасы',
            'Что делать, если ваш кот хочет вас убить': 'Детективы',
            'Трое в лодке': 'Комедии',
            'Божественная комедия': 'Комедии',
            'Властелин колец': 'Фантастика'
        }
        assert books_genre == expected


    # проверяем вывод книг, подходящих детям
    def test_get_books_for_children(self, collector_with_books):
        collector_with_books.add_new_book('Простоквашино')
        collector_with_books.set_book_genre('Простоквашино', 'Мультфильмы')
        
        children_books = collector_with_books.get_books_for_children()
        
        assert 'Простоквашино' in children_books
        assert 'Трое в лодке' in children_books
        assert 'Властелин колец' in children_books 
        assert 'Гордость и предубеждение и зомби' not in children_books 
        assert 'Что делать, если ваш кот хочет вас убить' not in children_books  


    # проверяем добавление книги в избранное 
    def test_add_book_in_favorites(self, collector_with_books):
        collector_with_books.add_book_in_favorites('Властелин колец')
        assert 'Властелин колец' in collector_with_books.get_list_of_favorites_books()


    # проверяем, что нельзя добавить книгу в избранное дважды
    def test_add_duplicate_to_favorites(self, collector_with_books):
        collector_with_books.add_book_in_favorites('Властелин колец')
        collector_with_books.add_book_in_favorites('Властелин колец')
        
        favorites = collector_with_books.get_list_of_favorites_books()
        assert favorites.count('Властелин колец') == 1


    # проверяем удаление книги из избранного 
    def test_delete_book_from_favorites(self, collector_with_books):
        collector_with_books.add_book_in_favorites('Властелин колец')
        collector_with_books.delete_book_from_favorites('Властелин колец')
        assert 'Властелин колец' not in collector_with_books.get_list_of_favorites_books()
    

    # проверяем пустой список избранного 
    def test_get_list_of_favorites_books_empty(self, collector):
        assert collector.get_list_of_favorites_books() == []


    # проверяем список избранного с книгами
    def test_get_list_of_favorites_books_with_books(self, collector_with_books):
        collector_with_books.add_book_in_favorites('Властелин колец')
        collector_with_books.add_book_in_favorites('Трое в лодке')
        
        favorites = collector_with_books.get_list_of_favorites_books()
        expected = ['Властелин колец', 'Трое в лодке']
        assert sorted(favorites) == sorted(expected)



