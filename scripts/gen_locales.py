#!/usr/bin/env python3
"""Generate lapce-app/locales/{en-US,zh-CN}.toml for settings UI language support."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCALES = ROOT / "lapce-app" / "locales"
LOCALES.mkdir(parents=True, exist_ok=True)

# cmd.<serialize_id> = message
COMMANDS = {
    "enable_modal_editing": ("Enable Modal Editing", "启用模态编辑"),
    "disable_modal_editing": ("Disable Modal Editing", "禁用模态编辑"),
    "open_folder": ("Open Folder", "打开文件夹"),
    "close_folder": ("Close Folder", "关闭文件夹"),
    "open_file": ("Open File", "打开文件"),
    "show_call_hierarchy": ("Show Call Hierarchy", "显示调用层级"),
    "find_references": ("Find References", "查找引用"),
    "go_to_implementation": ("Go to Implementation", "转到实现"),
    "reveal_in_panel": ("Reveal in Panel", "在面板中显示"),
    "source_control_open_active_file_remote_url": ("Source Control: Open Remote File Url", "源代码管理：打开远程文件 URL"),
    "reveal_in_file_explorer": ("Reveal in System File Explorer", "在系统文件管理器中显示"),
    "run_in_terminal": ("Run in Terminal", "在终端中运行"),
    "reveal_active_file_in_file_explorer": ("Reveal Active File in File Explorer", "在文件管理器中显示当前文件"),
    "file_explorer.rename": ("Rename File", "重命名文件"),
    "file_explorer.trash": ("Trash File", "删除文件"),
    "open_ui_inspector": ("Open Internal UI Inspector", "打开内部 UI 检查器"),
    "show_env": ("Show Environment", "显示环境变量"),
    "change_color_theme": ("Change Color Theme", "更改颜色主题"),
    "change_icon_theme": ("Change Icon Theme", "更改图标主题"),
    "open_settings": ("Open Settings", "打开设置"),
    "open_settings_file": ("Open Settings File", "打开设置文件"),
    "open_settings_directory": ("Open Settings Directory", "打开设置目录"),
    "open_theme_color_settings": ("Open Theme Color Settings", "打开主题颜色设置"),
    "open_keyboard_shortcuts": ("Open Keyboard Shortcuts", "打开键盘快捷键"),
    "open_keyboard_shortcuts_file": ("Open Keyboard Shortcuts File", "打开快捷键配置文件"),
    "open_log_file": ("Open Log File", "打开日志文件"),
    "open_logs_directory": ("Open Logs Directory", "打开日志目录"),
    "open_proxy_directory": ("Open Proxy Directory", "打开代理目录"),
    "open_themes_directory": ("Open Themes Directory", "打开主题目录"),
}

# Parse remaining commands from command.rs
cmd_rs = (ROOT / "lapce-app" / "src" / "command.rs").read_text(encoding="utf-8")
ser = None
for line in cmd_rs.splitlines():
    if 'strum(serialize = "' in line:
        ser = line.split('strum(serialize = "')[1].split('"')[0]
    elif 'strum(message = "' in line and ser:
        msg = line.split('strum(message = "')[1].split('"')[0]
        COMMANDS.setdefault(ser, (msg, msg))
        ser = None

# Settings descriptions from config sources
SETTINGS_DESC = {
    ("core", "modal"): ("Enable modal editing (Vim like)", "启用模态编辑（Vim 风格）"),
    ("core", "color-theme"): ("Set the color theme of Lapce", "设置 Lapce 的颜色主题"),
    ("core", "icon-theme"): ("Set the icon theme of Lapce", "设置 Lapce 的图标主题"),
    ("core", "language"): (
        "Set the interface display language. Takes effect after restart.",
        "设置界面显示语言。重启后生效。",
    ),
    ("core", "custom-titlebar"): (
        "Enable customised titlebar and disable OS native one (Linux, BSD, Windows)",
        "启用自定义标题栏并禁用系统原生标题栏（Linux、BSD、Windows）",
    ),
    ("core", "file-explorer-double-click"): (
        "Only allow double-click to open files in the file explorer",
        "在文件管理器中仅允许双击打开文件",
    ),
    ("core", "auto-reload-plugin"): (
        "Enable auto-reload for the plugin when its configuration changes.",
        "插件配置变更时自动重新加载插件。",
    ),
    ("editor", "font-family"): ("Set the editor font family", "设置编辑器字体"),
    ("editor", "font-size"): ("Set the editor font size", "设置编辑器字号"),
    ("editor", "code-glance-font-size"): ("Set the font size in the code glance", "设置代码预览字号"),
    ("editor", "line-height"): (
        "Set the editor line height. If less than 5.0, line height will be a multiple of the font size.",
        "设置编辑器行高。小于 5.0 时，行高为字号的倍数。",
    ),
    ("editor", "smart-tab"): (
        "If enabled, when you input a tab character, it will insert indent that's detected based on your files.",
        "启用后，输入制表符时将根据文件检测并插入缩进。",
    ),
    ("editor", "tab-width"): ("Set the tab width", "设置制表符宽度"),
    ("editor", "show-tab"): ("If opened editors are shown in a tab", "是否在标签页中显示已打开的编辑器"),
    ("editor", "show-bread-crumbs"): ("If navigation breadcrumbs are shown for the file", "是否显示文件导航面包屑"),
    ("editor", "scroll-beyond-last-line"): ("If the editor can scroll beyond the last line", "编辑器是否可滚动到最后一行之后"),
    ("editor", "cursor-surrounding-lines"): (
        "Set the minimum number of visible lines above and below the cursor",
        "设置光标上下最少可见行数",
    ),
    ("editor", "wrap-style"): ("The kind of wrapping to perform", "换行方式"),
    ("editor", "wrap-column"): ("The number of columns to wrap at", "按列数换行"),
    ("editor", "wrap-width"): ("The number of pixels to wrap at", "按像素宽度换行"),
    ("editor", "sticky-header"): (
        "Show code context like functions and classes at the top of editor when scroll",
        "滚动时在编辑器顶部显示函数、类等代码上下文",
    ),
    ("editor", "completion-width"): ("The number of pixels to show completion", "补全列表显示宽度（像素）"),
    ("editor", "completion-show-documentation"): (
        "If the editor should show the documentation of the current completion item",
        "是否显示当前补全项的文档",
    ),
    ("editor", "completion-item-show-detail"): (
        "Should the completion item use the `detail` field to replace the label `field`?",
        "补全项是否使用 `detail` 字段替换 `label` 字段",
    ),
    ("editor", "show-signature"): (
        "If the editor should show the signature of the function as the parameters are being typed",
        "输入参数时是否显示函数签名",
    ),
    ("editor", "signature-label-code-block"): (
        "If the signature view should put the codeblock into a label. This might not work nicely for LSPs which provide invalid code for their labels.",
        "签名视图是否将代码块放入标签。对于标签代码无效的 LSP 可能显示不佳。",
    ),
    ("editor", "auto-closing-matching-pairs"): (
        "Whether the editor should enable automatic closing of matching pairs",
        "是否自动闭合匹配括号",
    ),
    ("editor", "auto-surround"): (
        "Whether the editor should automatically surround selected text when typing quotes or brackets",
        "输入引号或括号时是否自动环绕选中文本",
    ),
    ("editor", "hover-delay"): (
        "How long (in ms) it should take before the hover information appears",
        "悬停提示出现前的延迟（毫秒）",
    ),
    ("editor", "modal-mode-relative-line-numbers"): (
        "If modal mode should have relative line numbers (though, not in insert mode)",
        "模态模式是否使用相对行号（插入模式除外）",
    ),
    ("editor", "format-on-save"): (
        "Whether it should format the document on save (if there is an available formatter)",
        "保存时是否格式化文档（若有可用格式化器）",
    ),
    ("editor", "normalize-line-endings"): (
        "Whether newlines should be automatically converted to the current line ending",
        "是否自动将换行符转换为当前行尾格式",
    ),
    ("editor", "highlight-matching-brackets"): ("If matching brackets are highlighted", "是否高亮匹配括号"),
    ("editor", "highlight-scope-lines"): ("If scope lines are highlighted", "是否高亮作用域线"),
    ("editor", "enable-inlay-hints"): ("If inlay hints should be displayed", "是否显示内联提示"),
    ("editor", "inlay-hint-font-family"): (
        "Set the inlay hint font family. If empty, it uses the editor font family.",
        "设置内联提示字体。留空则使用编辑器字体。",
    ),
    ("editor", "inlay-hint-font-size"): (
        "Set the inlay hint font size. If less than 5 or greater than editor font size, it uses the editor font size.",
        "设置内联提示字号。小于 5 或大于编辑器字号时使用编辑器字号。",
    ),
    ("editor", "enable-error-lens"): ("If diagnostics should be displayed inline", "是否内联显示诊断信息"),
    ("editor", "only-render-error-styling"): (
        "Only render the styling without displaying messages, provided that `Enable ErrorLens` is enabled",
        "启用 ErrorLens 后仅渲染样式而不显示消息",
    ),
    ("editor", "error-lens-end-of-line"): (
        "Whether error lens should go to the end of view line, or only to the end of the diagnostic",
        "错误透镜是否延伸到视图行末，还是仅到诊断末尾",
    ),
    ("editor", "error-lens-multiline"): (
        "Whether error lens should extend over multiple lines. If false, it will have newlines stripped.",
        "错误透镜是否跨多行显示。为 false 时将去掉换行。",
    ),
    ("editor", "error-lens-font-family"): (
        "Set error lens font family. If empty, it uses the inlay hint font family.",
        "设置错误透镜字体。留空则使用内联提示字体。",
    ),
    ("editor", "error-lens-font-size"): (
        "Set the error lens font size. If 0 it uses the inlay hint font size.",
        "设置错误透镜字号。为 0 时使用内联提示字号。",
    ),
    ("editor", "enable-completion-lens"): (
        "If the editor should display the completion item as phantom text",
        "是否将补全项显示为幻影文本",
    ),
    ("editor", "enable-inline-completion"): (
        "If the editor should display inline completions",
        "是否显示内联补全",
    ),
    ("editor", "completion-lens-font-family"): (
        "Set completion lens font family. If empty, it uses the inlay hint font family.",
        "设置补全透镜字体。留空则使用内联提示字体。",
    ),
    ("editor", "completion-lens-font-size"): (
        "Set the completion lens font size. If 0 it uses the inlay hint font size.",
        "设置补全透镜字号。为 0 时使用内联提示字号。",
    ),
    ("editor", "blink-interval"): (
        "Set the cursor blink interval (in milliseconds). Set to 0 to completely disable.",
        "设置光标闪烁间隔（毫秒）。设为 0 可完全禁用。",
    ),
    ("editor", "multicursor-case-sensitive"): (
        "Whether the multiple cursor selection is case sensitive.",
        "多光标选择是否区分大小写。",
    ),
    ("editor", "multicursor-whole-words"): (
        "Whether the multiple cursor selection only selects whole words.",
        "多光标选择是否仅选中完整单词。",
    ),
    ("editor", "render-whitespace"): (
        "How the editor should render whitespace characters.\nOptions: none, all, boundary, trailing.",
        "编辑器如何渲染空白字符。\n选项：none、all、boundary、trailing。",
    ),
    ("editor", "show-indent-guide"): ("Whether the editor show indent guide.", "是否显示缩进参考线。"),
    ("editor", "autosave-interval"): (
        "Set the auto save delay (in milliseconds), Set to 0 to completely disable",
        "设置自动保存延迟（毫秒）。设为 0 可完全禁用。",
    ),
    ("editor", "format-on-autosave"): (
        "Whether the document should be formatted when an autosave is triggered (required Format on Save)",
        "自动保存时是否格式化文档（需启用保存时格式化）",
    ),
    ("editor", "atomic-soft-tabs"): (
        "If enabled the cursor treats leading soft tabs as if they are hard tabs.",
        "启用后，光标将前导软制表符视为硬制表符。",
    ),
    ("editor", "double-click"): (
        "Use a double click to interact with the file explorer.\nOptions: single (default), file or all.",
        "使用双击与文件管理器交互。\n选项：single（默认）、file 或 all。",
    ),
    ("editor", "move-focus-while-search"): (
        "Move the focus as you type in the global search box",
        "在全局搜索框输入时移动焦点",
    ),
    ("editor", "diff-context-lines"): (
        "Set the default number of visible lines above and below the diff block (-1 for infinite)",
        "设置差异块上下默认可见行数（-1 为无限）",
    ),
    ("editor", "bracket-pair-colorization"): ("Whether the editor colorizes brackets", "是否为括号着色"),
    ("editor", "bracket-colorization-limit"): ("Bracket colorization Limit", "括号着色上限"),
    ("editor", "files-exclude"): (
        "Glob patterns for excluding files and folders (in file explorer)",
        "用于排除文件和文件夹的 Glob 模式（文件管理器）",
    ),
    ("ui", "scale"): ("Set the UI scale. Defaults to 1.0", "设置界面缩放。默认 1.0"),
    ("ui", "font-family"): (
        "Set the UI font family. If empty, it uses system default.",
        "设置界面字体。留空则使用系统默认。",
    ),
    ("ui", "font-size"): ("Set the UI base font size", "设置界面基础字号"),
    ("ui", "icon-size"): ("Set the icon size in the UI", "设置界面图标大小"),
    ("ui", "header-height"): (
        "Set the header height for panel header and editor tab header",
        "设置面板与编辑器标签页标题高度",
    ),
    ("ui", "status-height"): ("Set the height for status line", "设置状态栏高度"),
    ("ui", "tab-min-width"): ("Set the minimum width for editor tab", "设置编辑器标签最小宽度"),
    ("ui", "tab-separator-height"): (
        "Set whether the editor tab separator should be full height or the height of the content",
        "设置编辑器标签分隔符为全高还是内容高度",
    ),
    ("ui", "scroll-width"): ("Set the width for scroll bar", "设置滚动条宽度"),
    ("ui", "drop-shadow-width"): ("Controls the width of drop shadow in the UI", "控制界面投影宽度"),
    ("ui", "palette-width"): ("Controls the width of the command palette", "控制命令面板宽度"),
    ("ui", "hover-font-family"): (
        "Set the hover font family. If empty, it uses the UI font family",
        "设置悬停字体。留空则使用界面字体",
    ),
    ("ui", "hover-font-size"): ("Set the hover font size. If 0, uses the UI font size", "设置悬停字号。为 0 时使用界面字号"),
    ("ui", "trim-search-results-whitespace"): ("Trim whitespace from search results", "去除搜索结果两端空白"),
    ("ui", "list-line-height"): ("Set the line height for list items", "设置列表项行高"),
    ("ui", "tab-close-button"): ("Set position of the close button in editor tabs", "设置编辑器标签关闭按钮位置"),
    ("ui", "open-editors-visible"): ("Display the Open Editors section in the explorer", "在文件管理器中显示“打开的编辑器”区域"),
    ("terminal", "font-family"): (
        "Set the terminal font family. If empty, it uses editor font family.",
        "设置终端字体。留空则使用编辑器字体。",
    ),
    ("terminal", "font-size"): (
        "Set the terminal font size, If 0, it uses editor font size.",
        "设置终端字号。为 0 时使用编辑器字号。",
    ),
    ("terminal", "line-height"): (
        "Set the terminal line height, If 0, it uses editor line height",
        "设置终端行高。为 0 时使用编辑器行高",
    ),
}

# Field title-cased English names (fallback) — we also provide explicit names
FIELD_NAMES_EN = {
    ("core", "modal"): "Modal",
    ("core", "color-theme"): "Color Theme",
    ("core", "icon-theme"): "Icon Theme",
    ("core", "language"): "Language",
    ("core", "custom-titlebar"): "Custom Titlebar",
    ("core", "file-explorer-double-click"): "File Explorer Double Click",
    ("core", "auto-reload-plugin"): "Auto Reload Plugin",
}

FIELD_NAMES_ZH = {
    ("core", "modal"): "模态编辑",
    ("core", "color-theme"): "颜色主题",
    ("core", "icon-theme"): "图标主题",
    ("core", "language"): "界面语言",
    ("core", "custom-titlebar"): "自定义标题栏",
    ("core", "file-explorer-double-click"): "文件管理器双击打开",
    ("core", "auto-reload-plugin"): "自动重载插件",
    ("editor", "font-family"): "编辑器字体",
    ("editor", "font-size"): "编辑器字号",
    ("editor", "code-glance-font-size"): "代码预览字号",
    ("editor", "line-height"): "行高",
    ("editor", "smart-tab"): "智能制表符",
    ("editor", "tab-width"): "制表符宽度",
    ("editor", "show-tab"): "显示标签页",
    ("editor", "show-bread-crumbs"): "显示面包屑",
    ("editor", "scroll-beyond-last-line"): "滚动越过末行",
    ("editor", "cursor-surrounding-lines"): "光标周围可见行",
    ("editor", "wrap-style"): "换行样式",
    ("editor", "wrap-column"): "换行列数",
    ("editor", "wrap-width"): "换行宽度",
    ("editor", "sticky-header"): "粘性标题",
    ("editor", "completion-width"): "补全宽度",
    ("editor", "completion-show-documentation"): "显示补全文档",
    ("editor", "completion-item-show-detail"): "补全项显示详情",
    ("editor", "show-signature"): "显示签名",
    ("editor", "signature-label-code-block"): "签名标签代码块",
    ("editor", "auto-closing-matching-pairs"): "自动闭合括号",
    ("editor", "auto-surround"): "自动环绕",
    ("editor", "hover-delay"): "悬停延迟",
    ("editor", "modal-mode-relative-line-numbers"): "模态相对行号",
    ("editor", "format-on-save"): "保存时格式化",
    ("editor", "normalize-line-endings"): "规范化换行符",
    ("editor", "highlight-matching-brackets"): "高亮匹配括号",
    ("editor", "highlight-scope-lines"): "高亮作用域线",
    ("editor", "enable-inlay-hints"): "启用内联提示",
    ("editor", "inlay-hint-font-family"): "内联提示字体",
    ("editor", "inlay-hint-font-size"): "内联提示字号",
    ("editor", "enable-error-lens"): "启用错误透镜",
    ("editor", "only-render-error-styling"): "仅渲染错误样式",
    ("editor", "error-lens-end-of-line"): "错误透镜行末显示",
    ("editor", "error-lens-multiline"): "错误透镜多行",
    ("editor", "error-lens-font-family"): "错误透镜字体",
    ("editor", "error-lens-font-size"): "错误透镜字号",
    ("editor", "enable-completion-lens"): "启用补全透镜",
    ("editor", "enable-inline-completion"): "启用内联补全",
    ("editor", "completion-lens-font-family"): "补全透镜字体",
    ("editor", "completion-lens-font-size"): "补全透镜字号",
    ("editor", "blink-interval"): "光标闪烁间隔",
    ("editor", "multicursor-case-sensitive"): "多光标区分大小写",
    ("editor", "multicursor-whole-words"): "多光标全词匹配",
    ("editor", "render-whitespace"): "渲染空白字符",
    ("editor", "show-indent-guide"): "显示缩进参考线",
    ("editor", "autosave-interval"): "自动保存间隔",
    ("editor", "format-on-autosave"): "自动保存时格式化",
    ("editor", "atomic-soft-tabs"): "原子软制表符",
    ("editor", "double-click"): "双击行为",
    ("editor", "move-focus-while-search"): "搜索时移动焦点",
    ("editor", "diff-context-lines"): "差异上下文行数",
    ("editor", "bracket-pair-colorization"): "括号对着色",
    ("editor", "bracket-colorization-limit"): "括号着色上限",
    ("editor", "files-exclude"): "排除文件模式",
    ("ui", "scale"): "界面缩放",
    ("ui", "font-family"): "界面字体",
    ("ui", "font-size"): "界面字号",
    ("ui", "icon-size"): "图标大小",
    ("ui", "header-height"): "标题栏高度",
    ("ui", "status-height"): "状态栏高度",
    ("ui", "tab-min-width"): "标签最小宽度",
    ("ui", "tab-separator-height"): "标签分隔符高度",
    ("ui", "scroll-width"): "滚动条宽度",
    ("ui", "drop-shadow-width"): "投影宽度",
    ("ui", "palette-width"): "命令面板宽度",
    ("ui", "hover-font-family"): "悬停字体",
    ("ui", "hover-font-size"): "悬停字号",
    ("ui", "trim-search-results-whitespace"): "去除搜索结果空白",
    ("ui", "list-line-height"): "列表行高",
    ("ui", "tab-close-button"): "标签关闭按钮位置",
    ("ui", "open-editors-visible"): "显示打开的编辑器",
    ("terminal", "font-family"): "终端字体",
    ("terminal", "font-size"): "终端字号",
    ("terminal", "line-height"): "终端行高",
}

# UI chrome keys: key -> (en, zh)
UI = {
    "settings.section.core": ("Core", "核心"),
    "settings.section.editor": ("Editor", "编辑器"),
    "settings.section.ui": ("UI", "界面"),
    "settings.section.terminal": ("Terminal", "终端"),
    "settings.search_placeholder": ("Search Settings", "搜索设置"),
    "settings.plugin_settings": ("Plugin Settings", "插件设置"),
    "settings.reset": ("Reset", "重置"),
    "settings.theme.base_colors": ("Base Colors", "基础颜色"),
    "settings.theme.syntax_colors": ("Syntax Colors", "语法颜色"),
    "settings.theme.ui_colors": ("UI Colors", "界面颜色"),
    "menu.menu": ("Menu", "菜单"),
    "menu.connect_remote": ("Connect to Remote", "连接到远程"),
    "menu.connect_ssh": ("Connect to SSH Host", "连接 SSH 主机"),
    "menu.disconnect_remote": ("Disconnect remote", "断开远程连接"),
    "menu.connect_wsl": ("Connect to WSL Host", "连接 WSL 主机"),
    "menu.jump_backward": ("Jump Backward", "向后跳转"),
    "menu.jump_forward": ("Jump Forward", "向前跳转"),
    "menu.open_folder": ("Open Folder", "打开文件夹"),
    "menu.open_recent_workspace": ("Open Recent Workspace", "打开最近的工作区"),
    "menu.run_and_debug": ("Run and Debug", "运行和调试"),
    "menu.settings": ("Settings", "设置"),
    "menu.command_palette": ("Command Palette", "命令面板"),
    "menu.open_settings": ("Open Settings", "打开设置"),
    "menu.open_keyboard_shortcuts": ("Open Keyboard Shortcuts", "打开键盘快捷键"),
    "menu.open_theme_color_settings": ("Open Theme Color Settings", "打开主题颜色设置"),
    "menu.no_update": ("No update available", "没有可用更新"),
    "menu.about": ("About Lapce", "关于 Lapce"),
    "menu.minimize": ("Minimize", "最小化"),
    "menu.maximize": ("Maximize", "最大化"),
    "menu.close_window": ("Close Window", "关闭窗口"),
    "menu.choose_folder": ("Choose a folder", "选择文件夹"),
    "menu.choose_file": ("Choose a file", "选择文件"),
    "menu.save_file": ("Save File", "保存文件"),
    "panel.terminal": ("Terminal", "终端"),
    "panel.file_explorer": ("File Explorer", "文件管理器"),
    "panel.source_control": ("Source Control", "源代码管理"),
    "panel.plugin": ("Plugins", "插件"),
    "panel.search": ("Search", "搜索"),
    "panel.problem": ("Problems", "问题"),
    "panel.debug": ("Debug", "调试"),
    "panel.call_hierarchy": ("Call Hierarchy", "调用层级"),
    "panel.document_symbol": ("Document Symbol", "文档符号"),
    "panel.references": ("References", "引用"),
    "panel.implementation": ("Implementation", "实现"),
    "panel.open_editors": ("Open Editors", "打开的编辑器"),
    "panel.close": ("Close", "关闭"),
    "panel.new_terminal": ("New Terminal", "新建终端"),
    "panel.stop": ("Stop", "停止"),
    "panel.restart": ("Restart", "重启"),
    "panel.clear_all": ("Clear All", "全部清除"),
    "panel.commit_message": ("Commit Message", "提交信息"),
    "panel.commit": ("Commit", "提交"),
    "panel.changes": ("Changes", "变更"),
    "panel.discard_changes": ("Discard Changes", "丢弃更改"),
    "panel.installed": ("Installed", "已安装"),
    "panel.search_plugins": ("Search Plugins", "搜索插件"),
    "plugin.install": ("Install", "安装"),
    "plugin.installing": ("Installing", "安装中"),
    "plugin.uninstall": ("Uninstall", "卸载"),
    "plugin.enable": ("Enable", "启用"),
    "plugin.disable": ("Disable", "禁用"),
    "plugin.enable_workspace": ("Enable For Workspace", "在此工作区启用"),
    "plugin.disable_workspace": ("Disable For Workspace", "在此工作区禁用"),
    "plugin.upgrade": ("Upgrade Plugin", "升级插件"),
    "plugin.reload": ("Reload Plugin", "重载插件"),
    "plugin.loading_readme": ("Loading README", "正在加载 README"),
    "plugin.request_available": ("Request Available Plugins", "请求可用插件"),
    "status.normal": ("Normal", "普通"),
    "status.insert": ("Insert", "插入"),
    "status.visual": ("Visual", "可视"),
    "status.visual_line": ("Visual Line", "可视行"),
    "status.visual_block": ("Visual Block", "可视块"),
    "status.terminal": ("Terminal", "终端"),
    "status.toggle_left_panel": ("Toggle Left Panel", "切换左侧面板"),
    "status.toggle_bottom_panel": ("Toggle Bottom Panel", "切换底部面板"),
    "status.toggle_right_panel": ("Toggle Right Panel", "切换右侧面板"),
    "alert.cancel": ("Cancel", "取消"),
    "about.attributions": ("Attributions", "致谢"),
    "diff.expand_all": ("Expand All", "全部展开"),
    "diff.expand_up": ("Expand Up", "向上展开"),
    "diff.expand_down": ("Expand Down", "向下展开"),
    "palette.line": ("Go to Line", "转到行"),
    "palette.symbol": ("Go to Symbol", "转到符号"),
    "palette.workspace_symbol": ("Workspace Symbol", "工作区符号"),
    "palette.command": ("Command", "命令"),
    "palette.file": ("File", "文件"),
    "palette.help": ("Help", "帮助"),
    "keymap.title": ("Keyboard Shortcuts", "键盘快捷键"),
    "keymap.command": ("Command", "命令"),
    "keymap.key": ("Key", "按键"),
    "keymap.when": ("When", "生效条件"),
}


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def write_locale(path: Path, get_en_zh, collect_keys=False):
    lines = []
    seen = set()

    def add(key: str, value: str):
        if key in seen:
            return
        seen.add(key)
        lines.append(f'{key} = "{esc(value)}"')

    lines.append("# UI strings for Lapce. Keys are stable identifiers.")
    lines.append("")
    lines.append("# --- Commands ---")
    for cid, (en, zh) in sorted(COMMANDS.items()):
        add(f"cmd.{cid}", get_en_zh(en, zh))

    lines.append("")
    lines.append("# --- Settings ---")
    for section in ("core", "editor", "ui", "terminal"):
        en_sec, zh_sec = UI[f"settings.section.{section}"]
        add(f"settings.section.{section}", get_en_zh(en_sec, zh_sec))
        for (sec, field), (en, zh) in sorted(SETTINGS_DESC.items()):
            if sec != section:
                continue
            add(f"settings.{sec}.{field}.desc", get_en_zh(en, zh))
            name_en = FIELD_NAMES_ZH.get((sec, field), field.replace("-", " ").title())
            # English display name from title case of field
            name_en_default = field.replace("-", " ").title()
            name_zh = FIELD_NAMES_ZH.get((sec, field), name_en_default)
            add(f"settings.{sec}.{field}.name", get_en_zh(name_en_default, name_zh))

    lines.append("")
    lines.append("# --- UI chrome ---")
    for key, (en, zh) in sorted(UI.items()):
        add(key, get_en_zh(en, zh))

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {path} ({len(seen)} keys)")


write_locale(LOCALES / "en-US.toml", lambda en, zh: en)
write_locale(LOCALES / "zh-CN.toml", lambda en, zh: zh)

# Also dump command pairs for reference
out = ROOT / "command-pairs-full.tsv"
with out.open("w", encoding="utf-8") as f:
    for cid, (en, zh) in sorted(COMMANDS.items()):
        f.write(f"{cid}\t{en}\t{zh}\n")
print(f"commands: {len(COMMANDS)}")
print(f"settings descs: {len(SETTINGS_DESC)}")
print(f"ui keys: {len(UI)}")
