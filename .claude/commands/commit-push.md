---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git ls-files:*), AskUserQuestion
description: Выполни коммит и пуш текущих изменений
---

Выполни коммит и пуш текущих изменений:

1. Запусти параллельно без подтверждений: `git status`, `git diff HEAD`, `git ls-files --others --exclude-standard`
2. Составь лаконичное commit message по Conventional Commits:
   `<type>[scope]: <description>` — например `fix(masa): correct adhika masa boundary`
   Типы: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `chore`, `ci`
3. Используй AskUserQuestion, чтобы показать пользователю:
   - **✅ Войдут в коммит** — список изменённых/staged файлов
   - **⬜ Не войдут в коммит** — untracked файлы (если есть)
   - Предложенное сообщение коммита
   И спроси подтверждение. ДАЛЬНЕЙШИЕ ДЕЙСТВИЯ ТОЛЬКО ПОСЛЕ ОТВЕТА ПОЛЬЗОВАТЕЛЯ.
4. После подтверждения — добавь файлы в staging, создай коммит через HEREDOC, выполни `git push` — всё без дополнительных вопросов
5. Подтверди успех командой `git status`
