import os
import sys
import tempfile
import shutil
import pytest
from io import StringIO
from unittest.mock import patch, MagicMock

# Добавляем путь к src для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Импортируем функции
from src.commands.ls import ls
from src.commands.cd import cd
from src.commands.cat import cat
from src.commands.cp import cp
from src.commands.mv import mv
from src.commands.rm import rm
from src.main import main

# =============================================================================
# ТЕСТЫ ДЛЯ КОМАНД (UNIT TESTS)
# =============================================================================

class TestCommands:
    """Тесты для всех команд оболочки"""
    
    def setup_method(self):
        """Создаем временную структуру файлов перед каждым тестом"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Создаем тестовые файлы и папки
        with open("file1.txt", "w", encoding='utf-8') as f:
            f.write("Hello World!")
        
        with open("file2.txt", "w", encoding='utf-8') as f:
            f.write("Test content")
        
        os.makedirs("test_dir")
        with open("test_dir/file3.txt", "w", encoding='utf-8') as f:
            f.write("Nested file")
        
        os.makedirs("empty_dir")
    
    def teardown_method(self):
        """Очищаем после каждого теста"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    # ===== TESTS FOR ls =====
    def test_ls_current_directory(self, capsys):
        """Тест ls без аргументов"""
        ls([])
        captured = capsys.readouterr()
        assert "file1.txt" in captured.out
        assert "file2.txt" in captured.out
        assert "test_dir" in captured.out
    
    def test_ls_with_path(self, capsys):
        """Тест ls с указанием пути"""
        ls(["test_dir"])
        captured = capsys.readouterr()
        assert "file3.txt" in captured.out
    
    def test_ls_detailed(self, capsys):
        """Тест ls с опцией -l"""
        ls(["-l"])
        captured = capsys.readouterr()
        assert "file1.txt" in captured.out
    
    def test_ls_nonexistent(self, capsys):
        """Тест ls с несуществующим путем"""
        ls(["nonexistent"])
        captured = capsys.readouterr()
        # Ищем любой вывод в stderr или определенные фразы
        assert captured.err != "" or "nonexistent" in captured.out
    
    # ===== TESTS FOR cd =====
    def test_cd_valid_directory(self):
        """Тест cd с существующей папкой"""
        original = os.getcwd()
        cd(["test_dir"])
        assert os.getcwd() == os.path.join(original, "test_dir")
    
    def test_cd_nonexistent(self, capsys):
        """Тест cd с несуществующей папкой"""
        cd(["nonexistent_dir"])
        captured = capsys.readouterr()
        # Ищем сообщение об ошибке (на русском)
        assert "не удается найти" in captured.out.lower() or "error" in captured.out.lower()

    def test_cd_no_args(self, capsys):
        """Тест cd без аргументов"""
        cd([])
        captured = capsys.readouterr()
        assert "неправильно указан путь" in captured.out
    
    # ===== TESTS FOR cat =====
    def test_cat_file(self, capsys):
        """Тест cat с существующим файлом"""
        cat(["file1.txt"])
        captured = capsys.readouterr()
        assert "Hello World!" in captured.out
    
    def test_cat_nonexistent(self, capsys):
        """Тест cat с несуществующим файлом"""
        cat(["nonexistent.txt"])
        captured = capsys.readouterr()
        # Ищем сообщение об ошибке
        assert "no such file" in captured.out.lower() or "error" in captured.out.lower()
    
    def test_cat_directory(self, capsys):
        """Тест cat с папкой вместо файла"""
        cat(["test_dir"])
        captured = capsys.readouterr()
        assert "каталог" in captured.out.lower() or "directory" in captured.out.lower()
    
    def test_cat_no_args(self, capsys):
        """Тест cat без аргументов"""
        cat([])
        captured = capsys.readouterr()
        assert "не указан файл" in captured.out
    
    # ===== TESTS FOR cp =====
    def test_cp_file(self):
        """Тест копирования файла"""
        cp(["file1.txt", "file1_copy.txt"])
        assert os.path.exists("file1_copy.txt")
        with open("file1_copy.txt", "r", encoding='utf-8') as f:
            assert f.read() == "Hello World!"
    
    def test_cp_directory_without_r(self, capsys):
        """Тест копирования папки без -r"""
        cp(["test_dir", "test_dir_copy"])
        captured = capsys.readouterr()
        assert "-r не указан" in captured.out
    
    def test_cp_directory_with_r(self):
        """Тест копирования папки с -r"""
        cp(["-r", "test_dir", "test_dir_copy"])
        assert os.path.exists("test_dir_copy")
        assert os.path.exists("test_dir_copy/file3.txt")
    
    def test_cp_insufficient_args(self, capsys):
        """Тест cp с недостаточным количеством аргументов"""
        cp(["file1.txt"])
        captured = capsys.readouterr()
        assert "нужно указать источник и назначение" in captured.out
    
    # ===== TESTS FOR mv =====
    def test_mv_rename_file(self):
        """Тест переименования файла"""
        mv(["file1.txt", "renamed_file.txt"])
        assert not os.path.exists("file1.txt")
        assert os.path.exists("renamed_file.txt")
    
    def test_mv_move_file(self):
        """Тест перемещения файла в папку"""
        mv(["file1.txt", "empty_dir"])
        assert not os.path.exists("file1.txt")
        assert os.path.exists("empty_dir/file1.txt")
    
    def test_mv_insufficient_args(self, capsys):
        """Тест mv с недостаточным количеством аргументов"""
        mv(["file1.txt"])
        captured = capsys.readouterr()
        assert "нужно указать источник и назначение" in captured.out
    
    # ===== TESTS FOR rm =====
    def test_rm_file(self):
        """Тест удаления файла"""
        rm(["file1.txt"])
        assert not os.path.exists("file1.txt")
    
    def test_rm_directory_without_r(self, capsys):
        """Тест удаления папки без -r"""
        rm(["test_dir"])
        captured = capsys.readouterr()
        # Ищем сообщение о том, что это каталог
        assert "каталог" in captured.out.lower() or "directory" in captured.out.lower()
        assert os.path.exists("test_dir")  # Папка должна остаться
    
    def test_rm_directory_with_r(self, monkeypatch, capsys):
        """Тест удаления папки с -r (подтверждаем удаление)"""
        # Мокаем input чтобы автоматически подтвердить удаление
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        rm(["-r", "test_dir"])
        assert not os.path.exists("test_dir")
    
    def test_rm_cancel(self, monkeypatch, capsys):
        """Тест отмены удаления папки"""
        # Мокаем input чтобы отменить удаление
        monkeypatch.setattr('builtins.input', lambda _: 'n')
        rm(["-r", "test_dir"])
        captured = capsys.readouterr()
        assert os.path.exists("test_dir")  # Папка должна остаться
    
    def test_rm_protected_paths(self, capsys):
        """Тест защиты системных путей"""
        rm(["/"])
        captured = capsys.readouterr()
        assert "запрещено" in captured.out.lower()
    
    def test_rm_no_args(self, capsys):
        """Тест rm без аргументов"""
        rm([])
        captured = capsys.readouterr()
        assert "не указан путь" in captured.out


# =============================================================================
# ТЕСТЫ ДЛЯ MAIN (INTEGRATION TESTS)
# =============================================================================

class TestMainShell:
    """Тесты для основной оболочки"""
    
    def setup_method(self):
        """Создаем временную структуру файлов"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Создаем тестовые файлы
        with open("test_file.txt", "w", encoding='utf-8') as f:
            f.write("Hello Main!")
        
        os.makedirs("test_folder")
    
    def teardown_method(self):
        """Очищаем после каждого теста"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_main_exit_command(self):
        """Тест выхода из оболочки"""
        with patch('builtins.input', side_effect=['exit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "Мини-оболочка" in output
                assert "Введите 'exit' для выхода" in output
    
    def test_main_ls_command(self):
        """Тест команды ls через main"""
        with patch('builtins.input', side_effect=['ls', 'exit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "test_file.txt" in output
                assert "test_folder" in output
    
    def test_main_cat_command(self):
        """Тест команды cat через main"""
        with patch('builtins.input', side_effect=['cat test_file.txt', 'exit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "Hello Main!" in output
    
    def test_main_unknown_command(self):
        """Тест неизвестной команды"""
        with patch('builtins.input', side_effect=['unknown_command', 'exit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "команда не найдена" in output or "command not found" in output
    
    def test_main_empty_input(self):
        """Тест пустого ввода"""
        with patch('builtins.input', side_effect=['', 'exit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                # Не должно быть ошибок при пустом вводе
    
    def test_main_keyboard_interrupt(self):
        """Тест обработки Ctrl+C"""
        with patch('builtins.input', side_effect=[KeyboardInterrupt, 'exit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert 'Введите "exit" для выхода' in output
    
    def test_main_error_handling(self):
        """Тест что оболочка не падает при ошибках"""
        with patch('builtins.input', side_effect=['cd nonexistent_folder', 'ls', 'exit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                # Оболочка должна продолжить работу после ошибки cd
                assert "test_file.txt" in output  # ls должен работать


# =============================================================================
# ПРОСТЫЕ ТЕСТЫ ДЛЯ ПРОВЕРКИ
# =============================================================================

def test_simple_math():
    """Простой тест для проверки работы pytest"""
    assert 1 + 1 == 2

def test_string_operations():
    """Еще один простой тест"""
    assert "hello".upper() == "HELLO"


if __name__ == "__main__":
    # Можно запустить тесты напрямую через Python
    pytest.main([__file__, "-v"])