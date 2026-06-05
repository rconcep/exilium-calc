from nicegui import ui


def apply_exilium_theme() -> None:
    """Inject the shared Exilium-inspired UI theme."""
    ui.colors(
        primary="#d5a34f",
        secondary="#66b9bd",
        accent="#8fd6d0",
        dark="#081319",
        positive="#69c7a4",
        negative="#d46d5b",
        warning="#e7bc61",
        info="#65bbc4",
    )
    ui.add_head_html("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
          :root {
            --ex-bg: #071319;
            --ex-panel-top: rgba(108, 122, 132, 0.28);
            --ex-panel-bottom: rgba(19, 33, 41, 0.9);
            --ex-panel-edge: rgba(145, 199, 199, 0.18);
            --ex-text: #eef4ef;
            --ex-muted: #8ea4a7;
            --ex-accent: #8fd6d0;
            --ex-gold: #d5a34f;
            --ex-gold-soft: #efd48a;
            --ex-shadow: 0 18px 50px rgba(0, 0, 0, 0.34);
          }

          html, body {
            background:
              radial-gradient(circle at 18% 20%, rgba(101, 187, 196, 0.16), transparent 0 26%),
              radial-gradient(circle at 82% 14%, rgba(213, 163, 79, 0.12), transparent 0 18%),
              linear-gradient(180deg, rgba(4, 16, 22, 0.96), rgba(8, 20, 25, 0.98)),
              repeating-linear-gradient(
                90deg,
                rgba(255, 255, 255, 0.015) 0,
                rgba(255, 255, 255, 0.015) 1px,
                transparent 1px,
                transparent 140px
              );
            color: var(--ex-text);
            font-family: 'Inter', sans-serif;
          }

          body {
            letter-spacing: 0.02em;
          }

          .nicegui-content {
            min-height: 100vh;
            padding-top: 6.25rem !important;
            padding-left: 1.25rem;
            padding-right: 1.25rem;
            padding-bottom: 2rem;
            background:
              linear-gradient(180deg, rgba(4, 12, 16, 0.2), rgba(4, 12, 16, 0.45)),
              radial-gradient(circle at bottom, rgba(213, 163, 79, 0.06), transparent 0 32%);
          }

          .q-layout__section--marginal {
            background: rgba(6, 18, 23, 0.84) !important;
            backdrop-filter: blur(16px);
            border-color: rgba(143, 214, 208, 0.16) !important;
          }

          .exilium-topbar,
          .exilium-footer {
            box-shadow: 0 1px 0 rgba(143, 214, 208, 0.12);
          }

          .exilium-shell,
          .exilium-dashboard,
          .exilium-mainpage-row {
            width: min(100%, 110rem);
            margin: 0 auto;
          }

          .exilium-dashboard,
          .exilium-mainpage-row {
            gap: 1.5rem;
            align-items: flex-start;
          }

          .q-card,
          .exilium-panel,
          .q-dialog__inner > .q-card,
          .q-menu .q-card {
            position: relative;
            overflow: hidden;
            color: var(--ex-text);
            background:
              linear-gradient(180deg, var(--ex-panel-top), var(--ex-panel-bottom)),
              rgba(7, 19, 25, 0.9) !important;
            border: 1px solid var(--ex-panel-edge) !important;
            border-radius: 1.1rem !important;
            box-shadow: var(--ex-shadow);
            backdrop-filter: blur(12px);
          }

          .q-card::before,
          .exilium-panel::before,
          .q-dialog__inner > .q-card::before,
          .q-menu .q-card::before {
            content: '';
            position: absolute;
            inset: 0 0 auto 0;
            height: 3px;
            background: linear-gradient(90deg, rgba(143, 214, 208, 0.1), var(--ex-gold), rgba(143, 214, 208, 0.12));
            opacity: 0.9;
          }

          .exilium-portrait-panel {
            background:
              radial-gradient(circle at 50% 8%, rgba(143, 214, 208, 0.14), transparent 0 38%),
              linear-gradient(180deg, rgba(108, 122, 132, 0.22), rgba(18, 30, 37, 0.95)) !important;
          }

          .exilium-portrait-panel .q-img,
          .exilium-portrait-panel img {
            height: 100%;
            object-fit: cover;
          }

          .q-separator,
          .exilium-divider {
            background: linear-gradient(90deg, rgba(143, 214, 208, 0), rgba(143, 214, 208, 0.4), rgba(213, 163, 79, 0.5), rgba(143, 214, 208, 0));
            opacity: 0.85;
          }

          h1, h2, h3, h4, .text-h4, .text-h5, .text-h6, .text-lg {
            font-family: 'Josefin Sans', sans-serif;
            font-weight: 700;
            letter-spacing: 0.04em;
            color: #f4f7f2;
          }

          .exilium-character-copy h1,
          .exilium-character-copy h2,
          .exilium-intro-copy h1 {
            margin-bottom: 0.35rem;
            text-transform: uppercase;
            letter-spacing: 0.07em;
          }

          .exilium-character-copy p,
          .exilium-intro-copy p,
          .q-item__label,
          .q-field,
          .q-table,
          .q-chip,
          .q-btn {
            font-family: 'Inter', sans-serif;
          }

          .text-gray-500,
          .q-item__label--caption,
          .text-caption,
          .text-subtitle2,
          .exilium-subtle {
            color: var(--ex-muted) !important;
          }

          a {
            color: var(--ex-gold-soft);
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: color 0.18s ease, border-color 0.18s ease;
          }

          a:hover {
            color: #fff0bf;
            border-color: rgba(239, 212, 138, 0.4);
          }

          .q-tabs {
            background: rgba(17, 35, 43, 0.56);
            border: 1px solid rgba(143, 214, 208, 0.14);
            border-radius: 1rem;
            padding: 0.3rem;
          }

          .q-tabs__content {
            gap: 0.4rem;
          }

          .q-tab {
            border-radius: 0.8rem;
            color: var(--ex-muted);
            min-height: 2.9rem;
            transition: background-color 0.18s ease, color 0.18s ease;
          }

          .q-tab--active {
            color: #f7f8f4;
            background: linear-gradient(180deg, rgba(106, 122, 135, 0.24), rgba(31, 52, 61, 0.68));
          }

          .q-tab__content {
            font-family: 'Josefin Sans', sans-serif;
            font-size: 0.96rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
          }

          .q-tab__indicator {
            background: linear-gradient(90deg, var(--ex-gold), #f1d387) !important;
            height: 3px !important;
            border-radius: 999px;
          }

          .q-field__label {
            color: var(--ex-muted) !important;
            letter-spacing: 0.06em;
            text-transform: uppercase;
          }

          .q-field__control,
          .q-field--filled .q-field__control,
          .q-field--outlined .q-field__control,
          .q-select .q-field__control,
          .q-input .q-field__control {
            background: rgba(20, 36, 43, 0.85) !important;
            border-radius: 0.9rem !important;
            color: var(--ex-text);
            /* Prevent inner content from bleeding behind the rounded corners */
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
          }

          /* Also pad the wrapper so the label / underline tracks the inset */
          .q-field--outlined .q-field__control:before,
          .q-field--outlined .q-field__control:after {
            border-color: rgba(143, 214, 208, 0.22) !important;
            border-radius: inherit !important;
          }

          .q-field--focused .q-field__control:after,
          .q-field--highlight {
            border-color: var(--ex-accent) !important;
          }

          /* Pull the native input / prefix / suffix inward to match the padding */
          .q-field__native,
          .q-field__input {
            padding-left: 0 !important;
            padding-right: 0 !important;
            color: var(--ex-text) !important;
          }

          .q-field__prefix,
          .q-field__suffix {
            color: var(--ex-text) !important;
            padding: 0 0.25rem !important;
          }

          /* Keep the dropdown arrow and other icons inside the rounded area */
          .q-select__dropdown-icon {
            color: var(--ex-text) !important;
            margin-right: 0 !important;
          }

          .q-checkbox__label,
          .q-toggle__label,
          .q-radio__label {
            color: var(--ex-text) !important;
          }

          .q-btn {
            border-radius: 0.9rem;
            font-family: 'Josefin Sans', sans-serif;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            box-shadow: none;
          }

          .q-btn.bg-primary,
          .q-btn--standard.bg-primary,
          .q-btn--unelevated.bg-primary {
            color: #131618 !important;
            background: linear-gradient(180deg, #efd487, var(--ex-gold)) !important;
          }

          .q-btn--outline {
            border-color: rgba(143, 214, 208, 0.28) !important;
            color: var(--ex-text);
          }

          .q-list,
          .q-table__container,
          .q-expansion-item__container {
            background: rgba(13, 29, 36, 0.6);
            border: 1px solid rgba(143, 214, 208, 0.12);
            border-radius: 0.95rem;
          }

          .q-item {
            min-height: 3.2rem;
            color: var(--ex-text);
          }

          /* Keep side controls compact in list/expansion rows so labels don't wrap underneath. */
          .q-list .q-item__section--main,
          .q-expansion-item .q-item__section--main {
            min-width: 0;
          }

          .q-list .q-item__section--side .q-field,
          .q-expansion-item .q-item__section--side .q-field {
            width: clamp(6.75rem, 16vw, 8.25rem);
            min-width: 6.75rem;
          }

          .q-list .q-item__section--side,
          .q-expansion-item .q-item__section--side {
            padding-left: 0.5rem;
          }

          .q-item__label--header {
            color: var(--ex-accent) !important;
            font-family: 'Josefin Sans', sans-serif;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
          }

          .q-expansion-item {
            border-radius: 0.95rem;
            overflow: hidden;
            margin-bottom: 0.55rem;
          }

          .q-expansion-item__toggle-icon,
          .q-expansion-item__label {
            color: #f2f5f1;
          }

          .q-table thead tr,
          .q-table tbody td,
          .q-table tbody th {
            background: transparent;
            color: var(--ex-text);
          }

          .q-table thead tr {
            background: rgba(31, 52, 61, 0.8);
          }

          .q-table th {
            color: var(--ex-accent);
            font-family: 'Josefin Sans', sans-serif;
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
          }

          .q-table tbody tr:nth-child(odd) {
            background: rgba(255, 255, 255, 0.02);
          }

          .q-table tbody tr:hover {
            background: rgba(143, 214, 208, 0.06);
          }

          .exilium-wrap-table .q-table {
            table-layout: fixed;
            width: 100%;
          }

          .exilium-wrap-table .q-table th,
          .exilium-wrap-table .q-table td {
            white-space: normal !important;
            overflow-wrap: anywhere;
            word-break: break-word;
            vertical-align: top;
          }

          .q-chip {
            background: linear-gradient(180deg, rgba(40, 90, 96, 0.92), rgba(20, 49, 55, 0.96)) !important;
            border: 1px solid rgba(143, 214, 208, 0.18);
            color: var(--ex-text) !important;
          }

          .q-chip__icon,
          .q-chip__icon--remove {
            color: var(--ex-gold-soft) !important;
          }

          .q-dialog__backdrop {
            background: rgba(1, 8, 11, 0.72);
            backdrop-filter: blur(8px);
          }

          .q-menu,
          .q-tooltip {
            color: var(--ex-text);
            background: rgba(8, 19, 25, 0.96) !important;
            border: 1px solid rgba(143, 214, 208, 0.18);
          }

          .exilium-multiselect-selected {
            background: linear-gradient(180deg, rgba(213, 163, 79, 0.28), rgba(143, 214, 208, 0.2)) !important;
            border-left: 3px solid var(--ex-gold);
            color: #f8f9f3 !important;
            font-weight: 600;
          }

          .q-scrollarea__thumb {
            background: linear-gradient(180deg, rgba(143, 214, 208, 0.55), rgba(213, 163, 79, 0.6));
            border-radius: 999px;
          }

          .exilium-plot {
            border-radius: 1rem;
            overflow: hidden;
            border: 1px solid rgba(143, 214, 208, 0.12);
            background: rgba(10, 24, 30, 0.58);
          }
        </style>
        """)
