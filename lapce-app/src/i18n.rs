//! Lightweight UI string localization.
//!
//! Locale catalogs live in `lapce-app/locales/<lang>.toml` as flat `key = "string"`
//! maps. The active language is fixed at startup from `core.language` (restart
//! to pick up changes). Missing keys fall back to `en-US`, then to the key itself.

use std::collections::HashMap;
use std::sync::{OnceLock, RwLock};

use include_dir::{include_dir, Dir};
use tracing::error;

static LOCALES_DIR: Dir<'_> = include_dir!("$CARGO_MANIFEST_DIR/locales");

static LANG: OnceLock<String> = OnceLock::new();
static CATALOG: OnceLock<RwLock<HashMap<String, String>>> = OnceLock::new();

/// Languages shipped with the editor. Values are BCP-47-style tags stored in
/// `core.language`.
pub const SUPPORTED_LANGUAGES: &[&str] = &["en-US", "zh-CN"];

fn catalog() -> &'static RwLock<HashMap<String, String>> {
    CATALOG.get_or_init(|| RwLock::new(HashMap::new()))
}

fn parse_locale_toml(content: &str) -> HashMap<String, String> {
    // Minimal flat TOML string map parser (keys and values, no nesting needed).
    // Falls back to the `toml` crate when present via config, but we keep this
    // dependency-free by accepting only `key = "value"` lines.
    let mut map = HashMap::new();
    for line in content.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') || line.starts_with('[') {
            continue;
        }
        let Some((key, value)) = line.split_once('=') else {
            continue;
        };
        let key = key.trim().trim_matches('"').to_string();
        let value = value.trim();
        let value = value
            .strip_prefix('"')
            .and_then(|v| v.strip_suffix('"'))
            .unwrap_or(value)
            .to_string();
        // Unescape common sequences.
        let value = value
            .replace("\\\"", "\"")
            .replace("\\n", "\n")
            .replace("\\t", "\t")
            .replace("\\\\", "\\");
        map.insert(key, value);
    }
    map
}

fn load_catalog(lang: &str) -> Option<HashMap<String, String>> {
    let path = format!("{lang}.toml");
    let file = LOCALES_DIR.get_file(&path)?;
    let content = file.contents_utf8()?;
    Some(parse_locale_toml(content))
}

fn normalize_lang(language: &str) -> &'static str {
    let trimmed = language.trim();
    for supported in SUPPORTED_LANGUAGES {
        if trimmed.eq_ignore_ascii_case(supported) {
            return supported;
        }
    }
    // Also accept bare language codes.
    match trimmed.to_ascii_lowercase().as_str() {
        "zh" | "zh-cn" | "zh_cn" | "zh-hans" | "chinese" => "zh-CN",
        "en" | "en-us" | "en_us" | "english" => "en-US",
        _ => "en-US",
    }
}

/// Load the locale for `language`. Safe to call once at startup; later calls
/// replace the active catalog when the process has not locked LANG yet.
pub fn init(language: &str) {
    let lang = normalize_lang(language);
    let fallback = load_catalog("en-US").unwrap_or_default();
    let active = if lang == "en-US" {
        fallback.clone()
    } else {
        let mut active = fallback.clone();
        if let Some(localized) = load_catalog(lang) {
            active.extend(localized);
        } else {
            error!("missing locale catalog for {lang}, falling back to en-US");
        }
        active
    };

    if LANG.set(lang.to_string()).is_err() {
        // Already initialized (e.g. config reload). Keep first language until restart.
        return;
    }
    *catalog().write().unwrap() = active;
}

/// Translate `key`. Unknown keys return the key string so call sites stay visible.
pub fn t(key: &str) -> String {
    let map = catalog().read().unwrap();
    map.get(key).cloned().unwrap_or_else(|| key.to_string())
}

/// Translate `key`, returning `fallback` when the key is missing.
pub fn t_or(key: &str, fallback: &str) -> String {
    let map = catalog().read().unwrap();
    map.get(key).cloned().unwrap_or_else(|| fallback.to_string())
}

/// Active language tag (`en-US` / `zh-CN`).
pub fn lang() -> &'static str {
    LANG.get().map(|s| s.as_str()).unwrap_or("en-US")
}

/// Whether `language` is a supported UI language tag.
pub fn is_supported(language: &str) -> bool {
    let trimmed = language.trim();
    SUPPORTED_LANGUAGES
        .iter()
        .any(|l| trimmed.eq_ignore_ascii_case(l))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn normalize_defaults_to_english() {
        assert_eq!(normalize_lang("fr-FR"), "en-US");
        assert_eq!(normalize_lang("zh-CN"), "zh-CN");
        assert_eq!(normalize_lang("ZH"), "zh-CN");
    }

    #[test]
    fn parse_flat_toml() {
        let map = parse_locale_toml("a = \"hello\"\n# comment\nb = \"world\"\n");
        assert_eq!(map.get("a").unwrap(), "hello");
        assert_eq!(map.get("b").unwrap(), "world");
    }
}
