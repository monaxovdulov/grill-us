# Режим комнаты в OpenClaw + Telegram

Эта настройка создаёт одно продуктовое обсуждение для двух или нескольких участников Telegram. OpenClaw использует общую сессию группы, передаёт метаданные отправителя и сохраняет обычные сообщения комнаты как тихий контекст. Grill Us использует эти данные, чтобы не смешивать наблюдения, предположения, предпочтения и решения разных людей.

Конфигурация основана на текущей документации OpenClaw по [скиллам](https://docs.openclaw.ai/tools/skills), [Telegram](https://docs.openclaw.ai/channels/telegram) и [ambient room events](https://docs.openclaw.ai/channels/ambient-room-events).

## 1. Установите Grill Us

Установите вложенный скилл через skills.sh resolver OpenClaw:

```bash
openclaw skills install skills-sh:monaxovdulov/grill-us/grill-us
openclaw skills check
```

Resolver фиксирует синхронизированный GitHub-коммит. Команда `git:monaxovdulov/grill-us` для этого репозитория не подходит: Git-установщик OpenClaw ожидает `SKILL.md` в корне репозитория.

Установка из локальной копии:

```bash
git clone https://github.com/monaxovdulov/grill-us.git
openclaw skills install ./grill-us/skills/grill-us --as grill-us
```

Если текущая сессия не обновила список скиллов, начните новую сессию OpenClaw.

## 2. Разрешите Telegram-боту видеть комнату

Privacy Mode скрывает от ботов большую часть сообщений группы без упоминания. Для постоянной комнаты Grill Us:

- отключите Privacy Mode через `/setprivacy` в BotFather; или
- назначьте бота администратором группы.

После изменения Privacy Mode удалите бота из группы и добавьте снова.

Найдите числовой Telegram ID каждого участника и отрицательный ID группы. Их показывает `openclaw logs --follow`. После добавления группы в список доступа команда `/whoami@<bot_username>` подтвердит идентификаторы.

## 3. Настройте тихую комнату с авторством

Добавьте следующие поля в `openclaw.json`, сохранив существующие настройки модели, провайдера, workspace и gateway.

```json5
{
  messages: {
    groupChat: {
      historyLimit: 50,
      unmentionedInbound: "room_event",
      visibleReplies: "message_tool",
    },
  },
  channels: {
    telegram: {
      enabled: true,
      botToken: "YOUR_TELEGRAM_BOT_TOKEN",
      groupPolicy: "allowlist",
      groupAllowFrom: [
        "TELEGRAM_ID_FIRST_PARTICIPANT",
        "TELEGRAM_ID_SECOND_PARTICIPANT",
      ],
      groups: {
        "-1001234567890": {
          requireMention: false,
        },
      },
    },
  },
}
```

После этого сообщения идут двумя маршрутами:

- обычное разрешённое сообщение становится тихим `room_event` с идентичностью отправителя;
- упоминание, ответ боту или команда остаётся явным пользовательским запросом.

Финальный текст модели от фонового события не отправляется в комнату автоматически. Для видимого ответа OpenClaw требует `message(action=send)`. Если агент работает с профилем инструментов `minimal` или `coding`, разрешите `message` отдельно:

```json5
{
  agents: {
    entries: {
      main: {
        tools: {
          alsoAllow: ["message"],
        },
      },
    },
  },
}
```

## 4. Начните продуктовую сессию

Один раз упомяните бота и явно вызовите скилл:

```text
@bot $grill-us Начни продуктовую сессию для этой комнаты.

Сначала зафиксируй наши имена, роли, непосредственный опыт и полномочия.
Затем помоги решить, что и зачем мы делаем. Сохраняй автора каждого утверждения,
не скрывай разногласия и задавай вопросы по именам. Мы можем отвечать в любом порядке.
```

После подтверждения списка участников можно писать в обычном порядке. OpenClaw передаёт идентичность отправителя, а Grill Us связывает её с участником и ведёт журнал авторства.

## 5. Проверьте поведение

Короткий тест с двух аккаунтов:

1. Первый участник пишет наблюдение без упоминания бота.
2. Второй участник пишет противоречащее ему предположение без упоминания бота.
3. Упомяните бота и попросите показать текущие данные и разногласие.
4. Проверьте, что каждое утверждение подписано правильным человеком и агент не выдумал согласие.

Диагностические команды:

```bash
openclaw skills info grill-us
openclaw skills check
openclaw channels status --probe
openclaw logs --follow
```

Если бот не видит сообщения без упоминания, проверьте `requireMention`, Privacy Mode, списки доступа и повторное добавление бота после изменения Privacy Mode. Если сообщения видны, но ответа нет, проверьте доступ агента к инструменту `message`.
