# Правила выживания в проекте

*Или как не сломать прод и остаться друзьями*

## Что нельзя делать НИКОГДА

### 1. **Не пушить прямо в main!**
```bash
# ❌ ТАК НЕ ДЕЛАТЬ!
git checkout main
git add .
git commit -m "срочный фикс"
git push origin main

# ✅ ДЕЛАТЬ ТАК!
git checkout develop
git pull origin develop
git checkout -b feature/my-awesome-feature
# ... работаем ...
git push origin feature/my-awesome-feature
# создаем pull request в GitHub
```

### 2. **Не коммитить чувствительные данные**
- Пароли, ключи API, `.env` файлы
- Личные данные пользователей
- Секретные URLы

### 3. **Стараемся не делать force-push**
Если все же пришлось, во-первых, делаем --force-with-lease, а во-вторых, сообщаем об этом в Telegram-чате остальным участникам.

## Что делать ОБЯЗАТЕЛЬНО

### 1. **Следуем процессу ветвления**

### 1. **Следуем процессу ветвления**

```bash
# Создаем ветку от main 
git checkout main
git pull origin main
git checkout -b type/description

# Типы веток:
feature/    # Новая функциональность
bugfix/     # Исправление бага
hotfix/     # Срочное исправление
docs/       # Документация 
```
**Примеры хороших названий:**
- `feature/add-building-map`
- `bugfix/fix-login-error` 
- `hotfix/critical-security-fix`

### 2. **Пишем понятные коммиты**

```bash
# ❌ Плохо
git commit -m "fix"
git commit -m "update"
git commit -m "some changes"

# ✅ Хорошо
git commit -m "feat(map): add clusterization"
git commit -m "fix(auth): resolve login redirect"
git commit -m "docs(readme): update instructions"
```

**Формат:** `type: description`

**Типы коммитов:**
- `feat` - новая функциональность
- `fix` - исправление бага  
- `docs` - документация
- `style` - форматирование
- `refactor` - рефакторинг
- `test` - добавление тестов
- `chore` - обновление зависимостей, конфигов

### 3. **Проходим код-ревью**

**Процесс ревью:**
1. Создаем pull request
2. Назначаем 2 ревьюверов
3. Ждем аппрувов ✅
4. Мержим только после 2+ аппрувов!

**Ревьюверы, проверяем:**
- Код читаемый и понятный?
- Нет ли уязвимостей безопасности?
- Соответствует ли архитектуре проекта?

## Код-стайл

### Python
```bash
# Автоформатирование (обязательно!)
black backend/
isort backend/

# Проверка стиля
flake8 backend/

# Перед коммитом:
тестирование - я с тестами на python не очень, тут Оля подскажет, какая команда универсальная должна быть
black backend/
isort backend/
flake8 backend/
```
### Pre-commit хуки
Установите один раз:
```bash
pip install pre-commit
pre-commit install
```
Теперь при каждом коммите автоматически проверяется код

## Работа с багами

### Нашли баг?
1. Не паникуем! 
2. Создаем issue в GitHub
3. Используем шаблон бага
4. Назначаем на себя (если будете фиксить)

**Шаблон для багов:**
```markdown
## Что случилось?
[Краткое описание]

## Как воспроизвести?
1. Зайти туда-то
2. Нажать то-то
3. Увидеть ошибку

## Что ожидали увидеть?
[Ожидаемое поведение]

## Скриншоты/логи:
[Прикладываем, если есть]
```

### Если всё сломалось:
```bash
git log --oneline -10  # смотрим что натворили
git reset --hard HEAD~1 # откатываем последний коммит
# или
git rebase -i HEAD~5    # переписываем историю
```