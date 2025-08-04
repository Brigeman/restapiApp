#!/usr/bin/env python3
"""
Скрипт для запуска тестов с покрытием
"""

import subprocess
import sys
import os


def run_coverage():
    """Запускает тесты с покрытием и выводит отчет"""
    print("🧪 Запуск тестов с покрытием...")
    print("=" * 50)
    
    # Устанавливаем переменную окружения для coverage
    env = os.environ.copy()
    env['COVERAGE_FILE'] = '.coverage'
    
    try:
        # Запускаем тесты с coverage
        result = subprocess.run([
            'python', '-m', 'pytest', 
            'test_*.py', 
            '--cov=.', 
            '--cov-report=term-missing',
            '--cov-report=html:htmlcov',
            '--cov-report=xml',
            '-v'
        ], env=env, capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Предупреждения:")
            print(result.stderr)
        
        # Проверяем результат
        if result.returncode == 0:
            print("\n✅ Тесты прошли успешно!")
        else:
            print(f"\n❌ Тесты завершились с ошибкой (код: {result.returncode})")
            
        # Показываем краткую статистику
        print("\n📊 Статистика покрытия:")
        subprocess.run(['python', '-m', 'coverage', 'report', '--show-missing'])
        
        print("\n🌐 HTML отчет создан в папке htmlcov/")
        print("📄 Откройте htmlcov/index.html в браузере для детального отчета")
        
    except Exception as e:
        print(f"❌ Ошибка при запуске coverage: {e}")
        return False
    
    return True


def show_coverage_summary():
    """Показывает краткую статистику покрытия"""
    print("\n📈 Краткая статистика покрытия:")
    print("-" * 30)
    
    try:
        result = subprocess.run([
            'python', '-m', 'coverage', 'report', '--show-missing'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        
    except Exception as e:
        print(f"❌ Ошибка при получении статистики: {e}")


if __name__ == "__main__":
    print("🚀 Coverage Runner для REST API")
    print("=" * 50)
    
    # Проверяем, установлен ли coverage
    try:
        import coverage
        print("✅ coverage установлен")
    except ImportError:
        print("❌ coverage не установлен. Установите: pip install coverage")
        sys.exit(1)
    
    # Запускаем тесты с покрытием
    success = run_coverage()
    
    if success:
        show_coverage_summary()
        print("\n🎉 Coverage анализ завершен!")
    else:
        print("\n💥 Coverage анализ завершился с ошибками")
        sys.exit(1) 