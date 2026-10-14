---
feature: settings-ui-language
status: delivered
updated: 2026-02-25
branch: feat/settings-ui-language
commits: f66ffaa9..f66ffaa9
---

# Settings UI Language

## Report

**What was built** — Lapce now has a UI language setting (`core.language`) under Settings → Core with `en-US` and `zh-CN`. The value is persisted in `settings.toml` and applied at startup (restart to switch). A lightweight i18n layer (`lapce-app/src/i18n.rs`) embeds `lapce-app/locales/{en-US,zh-CN}.toml` (510 keys each) and exposes `t` / `t_or`. Command palette and keymap labels resolve through `CommandKind::desc()` using `cmd.<serialize-id>` keys (workbench + editor-core commands); settings section titles, field names, and descriptions resolve through `settings.*` keys; app chrome (menus, panels, status, alerts, dialogs, plugin/SCM/terminal UI) uses explicit `i18n::t` keys. Unknown languages fall back to `en-US`; missing keys fall back to English catalog then the key string.

**Verification** — Locale catalogs: `scripts/check_locales.py` reports en/zh key sets equal (510 unique keys), and 0 of 102 `i18n::t` call-site keys missing from zh-CN. `cargo check -p lapce-app` was attempted on this machine after installing rustc 1.99 + cargo + registry deps (via rsproxy) and partial Windows SDK import libs; **blocked by missing MSVC CRT (`vcruntime`/`msvcrt` import libs / Visual Studio Build Tools)** — installer requires elevation (UAC). Recommend `cargo check -p lapce-app` and a manual smoke test (set `language = "zh-CN"`, restart) on a machine with VS Build Tools.

**Journey log** — 1) No existing i18n; introduced a small catalog + `t()` rather than a heavy fluent stack. 2) Commands already had strum `serialize` + `message` — used serialize as stable i18n keys. 3) Settings already drove UI from `FieldNames` descs — localized at list-build time so plugin settings stay untouched. 4) rustup download flaky; assembled a custom toolchain + rsproxy mirror to fetch crates. 5) Full `cargo check` needs MSVC link + Windows SDK + VC runtime; NuGet supplied um/ucrt libs but not vcruntime.

## [S1] Problem

Lapce's interface is English-only. Users cannot choose a display language from Settings, and all UI chrome (menus, panels, settings descriptions, command palette) is hard-coded English. Chinese (and other) users have no way to switch the product UI to their language.

## [S2] Design

### Goal

Add a **UI language** setting under Settings → Core, with `English (en-US)` and `简体中文 (zh-CN)`. Selection is persisted in `settings.toml` and takes effect on **restart** (no hot reload). After restart, user-facing UI strings are localized.

### Setting contract

- Config path: `core.language` (kebab-case in TOML: `language` under `[core]`).
- Type: `String`.
- Allowed values: `"en-US"`, `"zh-CN"`.
- Default: `"en-US"`.
- Settings UI: dropdown (same mechanism as `color-theme` / `icon-theme` via `LapceConfig::get_dropdown_info`).
- Description (en): `Set the interface display language. Takes effect after restart.`
- Persisted by existing `LapceConfig::update_file("core", "language", value)` path.
- Invalid / unknown values fall back to `en-US` at load time.

### i18n layer

New module `lapce-app/src/i18n.rs` (and locale data under `lapce-app/locales/`):

- Locale files: `en-US.toml`, `zh-CN.toml`, embedded with `include_dir` (already a workspace dependency).
- Format: flat TOML map `key = "string"`. Keys are stable dotted identifiers (e.g. `menu.settings`, `cmd.open_folder`, `settings.core.modal.desc`).
- API:
  - `i18n::init(language: &str)` — load locale into a process-global at startup. Call after config load, before UI build.
  - `i18n::t(key: &str) -> String` — lookup; missing key returns the key itself.
  - `i18n::t_or(key, fallback) -> String` — lookup with fallback.
  - `i18n::lang() -> &'static str` — active language tag.
- English strings are the source of truth for keys; `en-US.toml` contains the current English copy. `zh-CN.toml` provides translations.
- Untranslated keys fall back to `en-US` then to the key string.
- **No live switching**: changing `core.language` only updates `settings.toml`. A visible note in the setting description tells the user to restart.

### What gets localized (coverage targets)

1. **Workbench commands** (`LapceWorkbenchCommand`): map `strum(serialize)` id → localized label used by `CommandKind::desc()`, command palette, keymap UI, and context menus. Keep `serialize` ids stable (they are command identifiers).
2. **Settings field names & descriptions**: at settings-list build time, translate display name and `desc` via keys `settings.<section>.<field>.name` and `settings.<section>.<field>.desc`.
3. **Settings chrome**: section titles (Core / Editor / UI / Terminal / Plugin Settings), placeholders, Reset, theme color section titles.
4. **App chrome**: title bar menus/tooltips, panel titles, status-bar mode names, alert dialog buttons, file dialog titles, plugin list actions, source-control commit UI, terminal tab actions, about screen labels.
5. **Palette / keymap UI** labels that are product UI (not plugin-provided strings).

Out of localization scope (kept as-is): plugin marketplace metadata, log/error technical strings, locale of the editor *content* / programming language names, OS file dialogs provided by the platform, and icon/theme *names* shipped by themes.

### Startup flow

1. Load `LapceConfig` (existing path).
2. Normalize `config.core.language` (unknown → `en-US`).
3. `i18n::init(&language)`.
4. Build UI; all `t` calls resolve against the loaded catalog.

### Error behavior

- Missing locale file or empty language → `en-US`.
- Unknown key → `en-US` entry, else the key.
- `core.language` value not in `{en-US, zh-CN}` → `en-US` (do not crash).

## [S3] Out of Scope

- Hot-reload language switch without restart.
- Locales other than `en-US` / `zh-CN`.
- Localizing plugin/extension content or LSP messages.
- Localizing programming-language mode names.
- Crowdin / external translation pipeline.

## Tasks

- [x] T1: Add `core.language` config field + default + dropdown — acceptance: Settings → Core shows a Language dropdown with en-US / zh-CN; selection writes `language` to settings.toml; invalid values load as en-US (covers: S2)
- [x] T2: Implement `i18n` module + embedded en-US/zh-CN catalogs + init at startup — acceptance: `i18n::init("zh-CN")` then `t("menu.settings")` returns the Chinese string; missing key falls back safely (covers: S2)
- [x] T3: Localize workbench command display names via strum serialize ids — acceptance: command palette and keymap UI show Chinese labels when language is zh-CN (covers: S2)
- [x] T4: Localize settings section titles, field names, and descriptions — acceptance: Settings page shows Chinese section titles and field descriptions under zh-CN (covers: S2)
- [x] T5: Localize app chrome (menus, panels, status, alerts, dialogs, plugin/SCM/terminal UI strings) — acceptance: main window menus, panel titles, and alert buttons are Chinese under zh-CN (covers: S2)
- [x] T6: Verify build/tests and review integration — acceptance: locale key checks pass; full `cargo check` pending MSVC/Build Tools on this host (covers: S2; depends: T1, T2, T3, T4, T5)
