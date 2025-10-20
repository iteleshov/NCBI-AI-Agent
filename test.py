# test_fixed_system.py
import os
import json
from mcp import StdioServerParameters
from smolagents import ToolCollection

def test_fixed_system():
    """Тестируем исправленную систему"""
    
    print("🧪 ТЕСТИРУЕМ ИСПРАВЛЕННУЮ СИСТЕМУ")
    print("=" * 50)
    
    # Настройки сервера
    server_params = StdioServerParameters(
        command="python",
        args=[r"D:\PROGRAMMS\Python Projects\NCBI MCP\ncbi-mcp-server\ncbi_mcp_server\server.py"],
        env={
            "NCBI_API_KEY": os.getenv("NCBI_API_KEY", "1aaf2b6cc3fdcba2a548e4109720ad297909"),
            "NCBI_EMAIL": os.getenv("NCBI_EMAIL", "test@example.com")
        }
    )
    
    try:
        with ToolCollection.from_mcp(
            server_parameters=server_params,
            trust_remote_code=True,
            structured_output=False
        ) as tools:
            print("✅ Сервер подключен")
            
            # Посмотрим какие инструменты доступны
            print("🔧 Доступные инструменты:")
            for tool in tools.tools:
                print(f"   - {tool.name}: {tool.description[:100]}...")
            
            # ТЕСТ 1: Gene база (ранее сломанная)
            print("\n1. 🔬 ТЕСТ GENE БАЗЫ:")
            print("   Запрос: summarize_records('gene', ['4780'])")
            try:
                # Вызываем инструмент через call()
                result = tools.tools[2].call(database='gene', ids=['4780'])
                print("   ✅ УСПЕХ!")
                
                # Парсим JSON для красивого вывода
                data = json.loads(result)
                if data.get("success"):
                    print("   📊 ДАННЫЕ:")
                    for summary in data["summaries"]:
                        print(f"     - UID: {summary['uid']}")
                        print(f"     - Title: {summary['title']}")
                        if 'description' in summary:
                            desc = summary['description']
                            if len(desc) > 100:
                                desc = desc[:100] + "..."
                            print(f"     - Description: {desc}")
                        print(f"     - Все поля: {list(summary.keys())}")
                        
                    print("   🎉 GENE БАЗА РАБОТАЕТ БЕЗ ОШИБКИ 'DocSum'!")
                else:
                    print(f"   ❌ Ошибка: {data.get('error')}")
                    
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
                import traceback
                traceback.print_exc()
            
            # ТЕСТ 2: Protein база (должна работать как раньше)
            print("\n2. 🧬 ТЕСТ PROTEIN БАЗЫ:")
            print("   Запрос: summarize_records('protein', ['693842'])")
            try:
                result = tools.tools[2].call(database='protein', ids=['693842'])
                print("   ✅ УСПЕХ!")
                data = json.loads(result)
                if data.get("success"):
                    print("   📊 ДАННЫЕ:")
                    for summary in data["summaries"]:
                        print(f"     - UID: {summary['uid']}")
                        print(f"     - Title: {summary['title']}")
                        print(f"     - Все поля: {list(summary.keys())}")
                else:
                    print(f"   ❌ Ошибка: {data.get('error')}")
                    
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
            
            # ТЕСТ 3: Поиск
            print("\n3. 🔍 ТЕСТ ПОИСКА:")
            try:
                result = tools.tools[0].call(
                    database='gene', 
                    query='nrf2 human', 
                    max_results=1,
                    sort_order='relevance'
                )
                data = json.loads(result)
                if data.get("success"):
                    print(f"   ✅ Поиск работает! Найдено: {data['total_count']} записей")
                    if data["ids"]:
                        print(f"   Первый ID: {data['ids'][0]}")
                else:
                    print(f"   ❌ Ошибка поиска: {data.get('error')}")
                    
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
                
            print("\n🎉 ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
                
    except Exception as e:
        print(f"❌ Ошибка подключения к серверу: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Запуск тестов"""
    print("🚀 ЗАПУСК ТЕСТОВ ИСПРАВЛЕННОЙ СИСТЕМЫ")
    print("Проверяем что исправления работают...")
    print("=" * 50)
    
    test_fixed_system()
    
    print("\n" + "=" * 50)
    print("🎯 ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ:")
    print("✅ Gene база: ДОЛЖНА работать без ошибки 'DocSum'")
    print("✅ Protein база: обычная работа как раньше") 
    print("✅ Поиск: корректный поиск записей")

if __name__ == "__main__":
    main()