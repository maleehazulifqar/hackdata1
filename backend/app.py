import html
import inspect
import io
import json
import time

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="HackDataV2", page_icon="✨", layout="wide")

# ---------------------------------------------------------------- styling
st.markdown("""
<style>
.stApp{background:#fafaf8}
.block-container{padding:1.2rem 1.6rem 2rem;max-width:100%}
[data-testid="stToolbar"],[data-testid="stDecoration"],.stDeployButton{display:none}
header[data-testid="stHeader"]{background:transparent;height:2.2rem}
h1,h2,h3,h4{letter-spacing:0}
/* ---------- sidebar */
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f1b2e 30%,#1f3d55)}
[data-testid="stSidebar"][aria-expanded="true"]{min-width:240px!important;width:240px!important}
section[data-testid="stSidebar"] *{color:#dbe4ee}
section[data-testid="stSidebar"] h2{font-size:17px;color:#fff;margin:0}
section[data-testid="stSidebar"] .stButton button{background:transparent;border:0;box-shadow:none;height:auto;
  padding:.5rem .7rem;justify-content:flex-start;text-align:left;flex-wrap:wrap;gap:.1rem .55rem;border-radius:10px}
section[data-testid="stSidebar"] .stButton button:hover{background:rgba(255,255,255,.07)}
section[data-testid="stSidebar"] .stButton button p{font-weight:600;font-size:14px}
section[data-testid="stSidebar"] .stButton button::after{flex:0 0 100%;font-size:11px;opacity:.65;padding-left:1.75rem;margin-top:-2px}
section[data-testid="stSidebar"] button[kind="primary"],section[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"]{
  background:linear-gradient(90deg,#1b9a85,#2bb39c);box-shadow:0 0 0 2px #fff inset}
section[data-testid="stSidebar"] button[kind="primary"] *,section[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] *{color:#fff}
.st-key-nav_tabular button::after{content:"One table, custom columns"}
.st-key-nav_relational button::after{content:"Linked tables with keys"}
.st-key-nav_documents button::after{content:"Invoices and statements"}
/* ---------- page header, segmented controls */
.pt{font-size:16px;font-weight:700;margin:0}.ps{font-size:12px;color:#6b7686;margin:2px 0 0}
.st-key-viewmode div[role="radiogroup"],.st-key-sample div[role="radiogroup"]{display:inline-flex;gap:0;background:#fff;
  border:1px solid #e4e6e3;border-radius:10px;padding:3px}
.st-key-viewmode div[role="radiogroup"]{float:right}
.st-key-viewmode label,.st-key-sample label{margin:0;padding:4px 16px;border-radius:8px;cursor:pointer}
.st-key-viewmode label>div:first-child,.st-key-sample label>div:first-child,.st-key-explorer label>div:first-child,
[class*="st-key-fmt_"] label>div:first-child{display:none}
.st-key-viewmode label:has(input:checked),.st-key-sample label:has(input:checked){background:#1a9c85}
.st-key-viewmode label:has(input:checked) *,.st-key-sample label:has(input:checked) *{color:#fff}
/* ---------- cards & tables */
.card{background:#fff;border:1px solid #e4e6e3;border-radius:12px;padding:14px 16px}
.card small{color:#6b7686}.card b{display:block;font-size:26px;margin:2px 0}
.tbl{background:#fff;border:1px solid #e4e6e3;border-radius:12px;overflow:auto;max-width:100%}
.tbl table{border-collapse:collapse;width:100%;font-size:13px}
.tbl th{background:#eef1ee;text-align:left;padding:10px 14px;font-weight:600;white-space:nowrap;border-bottom:1px solid #e4e6e3}
.tbl td{padding:9px 14px;border-bottom:1px solid #eef0ee;white-space:nowrap}
.tbl tr:last-child td{border-bottom:0}.tbl .r{text-align:right}.tbl .mut,.mut{color:#6b7686}
.tbl tbody tr:hover{background:#f6f9f7}.null{color:#9aa4b2}
.bar{display:inline-block;width:80px;height:6px;border-radius:9px;background:#e0e4e1;vertical-align:middle;margin-right:6px;overflow:hidden}
.bar i{display:block;height:100%;background:#1a9c85}
.chip{background:#fff4dd;color:#a4670b;padding:1px 9px;border-radius:99px;font-size:11px;margin-left:6px}
.cap{font-size:12px;color:#6b7686;margin-top:8px}
.h3{font-size:14px;font-weight:700;margin:18px 0 4px}
.sec{font-size:12px;font-weight:700;color:#127a68;border-left:3px solid #1a9c85;padding-left:8px;margin:14px 0 6px}
.doc{background:#fff;border:1px solid #e4e6e3;border-radius:14px;padding:22px 26px;max-width:780px}
.doc .tot{text-align:right;color:#6b7686;line-height:1.8}.doc .tot b{color:#127a68;font-size:18px}
.rc{background:#fff;border:1px solid #e4e6e3;border-radius:14px;overflow:hidden}
.rc .rb{height:70px;background:#c5ece6;display:grid;place-items:center;font-size:26px;color:#127a68}
.rc .rt{padding:12px 14px;font-size:13px;line-height:1.7}.rc .k{background:#eceeed;border-radius:99px;padding:1px 9px;font-size:11px}
/* ---------- explorer, tabs, format cards */
.st-key-explorer label{border:1px solid #e4e6e3;border-radius:10px;padding:10px 12px;background:#fff;width:100%;margin:0 0 6px}
.st-key-explorer label:has(input:checked){border-color:#1a9c85;box-shadow:0 0 0 1px #1a9c85}
.stTabs [data-baseweb="tab-list"]{gap:8px;border:0}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none}
.stTabs button[role="tab"]{background:#eceeed;border-radius:99px;height:2rem;padding:0 14px}
.stTabs button[role="tab"][aria-selected="true"]{background:#14213a}
.stTabs button[role="tab"][aria-selected="true"] *{color:#fff}
[class*="st-key-fmt_"] div[role="radiogroup"]{display:grid;grid-template-columns:1fr 1fr;gap:8px}
[class*="st-key-fmt_"] label{border:1px solid #e4e6e3;border-radius:10px;padding:8px 10px;margin:0;flex-direction:column;align-items:flex-start;background:#fff}
[class*="st-key-fmt_"] label:has(input:checked){border-color:#1a9c85;background:#eef8f5}
[class*="st-key-fmt_"] label p{font-weight:600;font-size:13px}
[class*="st-key-fmt_"] label::after{font-size:10px;color:#6b7686}
[class*="st-key-fmt_"] label:nth-child(1)::after{content:"Plain text, opens anywhere"}
.st-key-fmt_Relational label:nth-child(1)::after{content:"Tables and inserts"}
[class*="st-key-fmt_"] label:nth-child(2)::after{content:"Workbook with sheets"}
[class*="st-key-fmt_"] label:nth-child(3)::after{content:"Structured data"}
/* ---------- config panel & buttons */
div[data-testid="stColumn"]:has(.cfg-anchor){position:sticky;top:2.6rem;align-self:flex-start}
.stDownloadButton button{background:#1a9c85!important;border:0!important;height:2.8rem}
.stDownloadButton button *{color:#fff!important;font-weight:600}
.stDownloadButton button:hover{background:#127a68!important}
.stMain .stButton button{border:1px solid #e4e6e3;background:#fff;border-radius:10px;font-weight:600}
@media(max-width:900px){div[data-testid="stColumn"]:has(.cfg-anchor){position:static}.block-container{padding:1rem}}
</style>
""", unsafe_allow_html=True)

FIRST = ["Ahmed", "Lucas", "Omar", "Emily", "Hannah", "Daniel", "James", "Priya", "Maria", "Ali", "Sara", "Chen"]
LAST = ["Kim", "Raza", "Garcia", "Brooks", "Osei", "Patel", "Chen", "Miller", "Ivanova"]
STATUS = ["active", "paused", "churned"]
SYMBOL = {"USD": "$", "EUR": "€", "GBP": "£", "PKR": "Rs "}
ITEMS = ["API access - Pro tier", "Data storage add-on", "Support plan", "Seat license", "Analytics module"]
COMPANIES = ["Northwind Supplies Ltd.", "Contoso Traders", "Fabrikam Inc.", "Adventure Works"]

st.session_state.setdefault("recent", [])
st.session_state.setdefault("seed", 42)


# works on old and new Streamlit versions
STRETCH = {"width": "stretch"} if "width" in inspect.signature(st.button).parameters else {"use_container_width": True}


HAS_ICON = "icon" in inspect.signature(st.button).parameters


def show(df, **kw):
    return st.dataframe(df, **STRETCH, **kw)


def new_seed():
    st.session_state.seed = int(np.random.randint(0, 999999))


DEFAULT_COLS = pd.DataFrame([
    {"name": "id", "type": "id", "min": 1, "max": 5000, "nulls %": 0.0, "outliers %": 0.0, "categories": ""},
    {"name": "name", "type": "name", "min": 0, "max": 0, "nulls %": 0.0, "outliers %": 0.0, "categories": ""},
    {"name": "email", "type": "email", "min": 0, "max": 0, "nulls %": 0.0, "outliers %": 0.0, "categories": ""},
    {"name": "signup", "type": "date", "min": 0, "max": 0, "nulls %": 0.0, "outliers %": 0.0, "categories": ""},
    {"name": "balance", "type": "numeric", "min": 100, "max": 3000, "nulls %": 1.0, "outliers %": 0.0, "categories": ""},
    {"name": "status", "type": "category", "min": 0, "max": 0, "nulls %": 0.0, "outliers %": 0.0,
     "categories": "active, paused, churned"},
])


def gen_tabular(spec, n, seed, mask):
    rng = np.random.default_rng(seed)
    people = gen_customers(n, rng, mask)
    out = {}
    for _, c in spec.dropna(subset=["name"]).iterrows():
        t, name = c["type"], str(c["name"])
        if t == "id":
            col = pd.Series(range(int(c["min"] or 1), int(c["min"] or 1) + n))
        elif t == "name":
            col = people["name"]
        elif t == "email":
            col = people["email"]
        elif t == "date":
            col = people["signup"]
        elif t == "numeric":
            lo, hi = float(c["min"]), float(c["max"])
            hi = max(hi, lo + 1)
            col = pd.Series(np.clip(lo + rng.lognormal(0, .7, n) * (hi - lo) / 4, lo, hi).round(2))
            k = int(n * float(c["outliers %"]) / 100)
            if k:
                col.iloc[rng.choice(n, k, replace=False)] = (hi * rng.uniform(1.5, 3, k)).round(2)
        else:
            cats = [x.strip() for x in str(c["categories"] or "a, b, c").split(",") if x.strip()]
            col = pd.Series(rng.choice(cats, n))
        col = col.astype(object if t in ("category", "name", "email", "date") else float if t == "numeric" else int)
        k = int(round(n * float(c["nulls %"]) / 100))
        if k and t != "id":
            col = col.astype(object) if t != "numeric" else col
            col.iloc[rng.choice(n, k, replace=False)] = np.nan
        out[name] = col.reset_index(drop=True)
    return pd.DataFrame(out)


# ---------------------------------------------------------------- generators
def mask_name(n):
    return " ".join(w[0] + "***" for w in n.split())


def mask_email(e):
    return e[0] + "***@" + e.split("@")[1]


def gen_customers(n, rng, mask, id_col="id"):
    names = [f"{rng.choice(FIRST)} {rng.choice(LAST)}" for _ in range(n)]
    emails = [
        f"{nm.split()[0][0].lower()}.{nm.split()[1].lower()}{rng.integers(1, 99) if rng.random() < .4 else ''}@example.com"
        for nm in names
    ]
    if mask:
        names, emails = [mask_name(x) for x in names], [mask_email(x) for x in emails]
    start = pd.Timestamp("2023-01-01")
    signup = (start + pd.to_timedelta(rng.integers(0, 1100, n), unit="D")).strftime("%Y-%m-%d")
    balance = np.clip(rng.lognormal(6.3, .7, n), 110, 2968).round(2)
    balance[rng.random(n) < .01] = np.nan
    return pd.DataFrame({id_col: range(1, n + 1), "name": names, "email": emails,
                         "signup": signup, "balance": balance, "status": rng.choice(STATUS, n)})


def gen_relational(rows, seed, mask):
    rng = np.random.default_rng(seed)
    nc = max(1, round(rows / 5))
    cust = gen_customers(nc, rng, mask, "customer_id")[["customer_id", "name", "email"]]
    no = round(nc * 2.2)
    orders = pd.DataFrame({
        "order_id": range(1, no + 1),
        "customer_id": rng.integers(1, nc + 1, no),
        "order_date": (pd.Timestamp("2023-01-01") + pd.to_timedelta(rng.integers(0, 1100, no), unit="D")).strftime("%Y-%m-%d"),
        "total": (rng.random(no) * 900).round(2)})
    items = pd.DataFrame({
        "item_id": range(1, rows + 1),
        "order_id": rng.integers(1, no + 1, rows),
        "sku": [f"SKU-{x}" for x in rng.integers(1000, 1090, rows)],
        "qty": rng.integers(1, 5, rows),
        "price": (5 + rng.random(rows) * 300).round(2)})
    return {"customers": cust, "orders": orders, "order_items": items}


def gen_documents(count, seed):
    rng = np.random.default_rng(seed)
    docs = []
    for i in range(count):
        lines = []
        for _ in range(int(rng.integers(2, 4))):
            q, p = int(rng.integers(1, 5)), round(float(50 + rng.random() * 1100), 2)
            lines.append({"item": rng.choice(ITEMS), "qty": q, "price": p, "amount": round(q * p, 2)})
        sub = round(sum(l["amount"] for l in lines), 2)
        tax = round(sub * .08, 2)
        issued = pd.Timestamp("2025-08-30") - pd.Timedelta(days=int(rng.integers(0, 40)))
        docs.append({"no": f"INV-{10432 + i}", "to": rng.choice(COMPANIES), "from": "Synth Data Co.",
                     "issued": issued.strftime("%b %d, %Y"),
                     "due": (issued + pd.Timedelta(days=30)).strftime("%b %d, %Y"),
                     "lines": lines, "subtotal": sub, "tax": tax, "total": round(sub + tax, 2)})
    return docs


def docs_to_df(docs):
    return pd.DataFrame([{"invoice": d["no"], "billed_to": d["to"], **l} for d in docs for l in d["lines"]])


# ---------------------------------------------------------------- helpers
def profile(df):
    out = []
    for c in df.columns:
        s = df[c]
        num = pd.api.types.is_numeric_dtype(s)
        if num:
            typ = "integer" if pd.api.types.is_integer_dtype(s) else "float"
        elif s.astype(str).str.fullmatch(r"\d{4}-\d\d-\d\d").all():
            typ = "date"
        elif c == "name":
            typ = "name"
        elif c == "email":
            typ = "email"
        else:
            typ = "category" if s.nunique() <= 6 else "text"
        out.append({"Column": c, "Type": typ, "Missing %": round(s.isna().mean() * 100, 1),
                    "Unique": s.nunique(), "Min": s.min() if num else None,
                    "Max": s.max() if num else None, "Mean": round(s.mean(), 1) if num else None})
    return pd.DataFrame(out)


def size_kb(tables):
    return sum(len(t.to_csv(index=False)) for t in tables.values()) / 1024


def to_sql(tables):
    parts = []
    for name, df in tables.items():
        parts.append(f"CREATE TABLE {name} ({', '.join(df.columns)});")
        for row in df.itertuples(index=False):
            vals = ", ".join("NULL" if pd.isna(v) else (str(v) if isinstance(v, (int, float, np.number)) else "'" + str(v).replace("'", "''") + "'") for v in row)
            parts.append(f"INSERT INTO {name} VALUES ({vals});")
        parts.append("")
    return "\n".join(parts)


def export_bytes(tables, fmt):
    if fmt == "CSV":
        return next(iter(tables.values())).to_csv(index=False).encode(), "text/csv", "csv"
    if fmt == "JSON":
        return json.dumps({k: v.where(v.notna(), None).to_dict("records") for k, v in tables.items()}, indent=2, default=str).encode(), "application/json", "json"
    if fmt == "SQL dump":
        return to_sql(tables).encode(), "text/plain", "sql"
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xw:
        for k, v in tables.items():
            v.to_excel(xw, sheet_name=k[:31], index=False)
    return buf.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "xlsx"


def save_recent(page, tables, seed, fmt):
    total = sum(t.size for t in tables.values())
    miss = int(sum(t.isna().sum().sum() for t in tables.values()))
    first = next(iter(tables.values()))
    st.session_state.recent.insert(0, {
        "name": f"{next(iter(tables))} (seed {seed})", "page": page, "fmt": fmt, "at": time.time(),
        "rows": len(first), "cols": first.shape[1], "kb": round(size_kb(tables), 1),
        "miss": miss, "cells": total})


def open_recent(page):
    st.session_state.nav = page


# ---------------------------------------------------------------- html helpers
def fmt_val(v, is_num):
    if pd.isna(v):
        return "<i class='null'>null</i>"
    if is_num and isinstance(v, (float, np.floating)):
        return ("%.2f" % v).rstrip("0").rstrip(".")
    return html.escape(str(v))


def html_table(df, index_from=None):
    cols = list(df.columns)
    num = {c: pd.api.types.is_numeric_dtype(df[c]) for c in cols}
    head = ("<th>#</th>" if index_from is not None else "") + "".join(
        f"<th class='{'r' if num[c] else ''}'>{html.escape(str(c))}</th>" for c in cols)
    rows = []
    for i, (_, r) in enumerate(df.iterrows()):
        cells = f"<td class='mut'>{index_from[i]}</td>" if index_from is not None else ""
        cells += "".join(f"<td class='{'r' if num[c] else ''}'>{fmt_val(r[c], num[c])}</td>" for c in cols)
        rows.append(f"<tr>{cells}</tr>")
    st.markdown(f"<div class='tbl'><table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>",
                unsafe_allow_html=True)


def profile_table(df):
    fmt = lambda v: "–" if v is None or pd.isna(v) else f"{v:,.2f}".rstrip("0").rstrip(".")
    rows = ""
    for p in profile(df).itertuples():
        rows += (f"<tr><td>{p.Column}</td><td class='mut'>{p.Type}</td>"
                 f"<td><span class='bar'><i style='width:{100 - p._3}%'></i></span><small class='mut'>{p._3:g}% missing</small></td>"
                 f"<td class='r'>{p.Unique}</td><td class='r'>{fmt(p.Min)}</td><td class='r'>{fmt(p.Max)}</td>"
                 f"<td class='r'>{fmt(p.Mean)}</td></tr>")
    st.markdown("<div class='tbl'><table><thead><tr><th>Column</th><th>Type</th><th>Valid / missing</th>"
                "<th class='r'>Unique</th><th class='r'>Min</th><th class='r'>Max</th><th class='r'>Mean</th></tr></thead>"
                f"<tbody>{rows}</tbody></table></div>", unsafe_allow_html=True)


def ago(t):
    m = int((time.time() - t) / 60)
    return "just now" if m < 1 else f"{m} min ago" if m < 60 else f"{m // 60} hr ago"


def go(page):
    st.session_state.nav = page


def step_doc(delta, total):
    st.session_state.doc_i = (st.session_state.get("doc_i", 0) + delta) % total


# ---------------------------------------------------------------- sidebar
PAGES = {"Tabular": ":material/table_chart:", "Relational": ":material/account_tree:",
         "Documents": ":material/description:", "Recent datasets": ":material/history:"}
st.session_state.setdefault("nav", "Tabular")
nav = st.session_state.nav
with st.sidebar:
    st.markdown("## ✨ HackDataV2")
    st.caption("Synthetic data platform")
    st.write("")
    for p, icon in PAGES.items():
        if p == "Recent datasets":
            st.divider()
        label = p if p != "Recent datasets" else f"Recent datasets  ({len(st.session_state.recent)})"
        st.button(label, key="nav_" + p.split()[0].lower(), on_click=go, args=(p,),
                  type="primary" if nav == p else "secondary", **STRETCH, **({"icon": icon} if HAS_ICON else {}))

# ---------------------------------------------------------------- recent page
if nav == "Recent datasets":
    st.markdown("<p class='pt'>Recent datasets</p><p class='ps'>Datasets you exported or saved. "
                "Open one to see its overview.</p>", unsafe_allow_html=True)
    if not st.session_state.recent:
        st.info("Nothing saved yet. Use “Save to recent datasets” on any page.")
    cols = st.columns(3)
    for i, r in enumerate(st.session_state.recent):
        with cols[i % 3]:
            miss = f"<span class='chip'>{r['miss']} missing ({r['miss'] / r['cells'] * 100:.1f}%)</span>" if r["miss"] else ""
            st.markdown(f"<div class='rc'><div class='rb'>▦</div><div class='rt'><b>{r['name']}</b><br>"
                        f"<span class='mut'>{r['page']} · {ago(r['at'])} · {r.get('fmt', 'CSV')}</span><br>"
                        f"<span style='color:#127a68'>{r['rows']} rows × {r['cols']} columns</span><br>"
                        f"<span class='k'>{r['kb']} KB</span>{miss}</div></div>", unsafe_allow_html=True)
            st.button("Open", key=f"open{i}", on_click=go, args=(r["page"],), **STRETCH)
    st.stop()

# ---------------------------------------------------------------- layout
main, cfg = st.columns([3, 1.3], gap="medium")

# ---- configuration panel (runs first so the main area can use its values)
with cfg:
    with st.container(border=True):
        st.markdown("<span class='cfg-anchor'></span><p class='pt'>Configuration</p>", unsafe_allow_html=True)
        with st.container(height=330, border=False):
            st.markdown("<div class='sec'>Generation</div>", unsafe_allow_html=True)
            if nav == "Documents":
                n = st.number_input("Document count", 1, 50, 5)
            else:
                n = st.number_input("Root table rows" if nav == "Relational" else "Row count", 5, 5000, 100)
            seed = st.number_input("Random seed", 0, 999999, key="seed")
            st.button("Shuffle seed", on_click=new_seed, **STRETCH, **({"icon": ":material/shuffle:"} if HAS_ICON else {}))
            c1, c2 = st.columns(2)
            c1.selectbox("Locale", ["en-US", "en-GB", "de-DE", "fr-FR"])
            cur = c2.selectbox("Currency", list(SYMBOL))
            st.markdown("<div class='sec'>Privacy rules</div>", unsafe_allow_html=True)
            st.caption("Applied to every matching column. Keys are never altered, so relations stay intact.")
            mask = st.toggle("Masking", help="Keeps the shape of names, emails and phones, hides the rest.")
            spec = DEFAULT_COLS
            if nav == "Tabular":
                st.markdown("<div class='sec'>Columns</div>", unsafe_allow_html=True)
                with st.expander("Edit columns"):
                    spec = st.data_editor(
                        DEFAULT_COLS, num_rows="dynamic", hide_index=True, key="cols",
                        column_config={"type": st.column_config.SelectboxColumn(
                            "type", options=["id", "name", "email", "date", "numeric", "category"], required=True)})
                    if spec.empty:
                        spec = DEFAULT_COLS
        fmts = {"Relational": ["SQL dump", "Excel", "JSON"]}.get(nav, ["CSV", "Excel", "JSON"])
        fmt = st.radio("Format", fmts, key=f"fmt_{nav}", label_visibility="collapsed")

# ---- data
if nav == "Tabular":
    tables = {"customers": gen_tabular(spec, int(n), int(seed), mask)}
elif nav == "Relational":
    tables = gen_relational(int(n), int(seed), mask)
else:
    docs = gen_documents(int(n), int(seed))
    tables = {"invoices": docs_to_df(docs)}

with cfg:
    data, mime, ext = export_bytes(tables, fmt)
    st.download_button(f"⬇  Export {fmt}", data, f"synthetic_data.{ext}", mime, **STRETCH)
    if st.button("Save to recent datasets", key="save", **STRETCH):
        save_recent(nav, tables, int(seed), fmt)
        st.toast("Dataset saved to recent history")

# ---- main area
with main:
    title = {"Tabular": "Tabular preview", "Relational": "Relational preview", "Documents": "Document preview"}[nav]
    left, right = st.columns([2, 1], vertical_alignment="center")
    mode = "Preview"
    with left:
        overview = st.session_state.get("viewmode") == "Overview" and nav != "Documents"
        st.markdown(f"<p class='pt'>{'Dataset overview' if overview else title}</p><p class='ps'>"
                    f"{'Summary of the full dataset.' if overview else 'Updates as you change settings.'} "
                    f"Seed {int(seed)}.</p>", unsafe_allow_html=True)
    with right:
        if nav != "Documents":
            mode = st.radio("View", ["Preview", "Overview"], horizontal=True, key="viewmode", label_visibility="collapsed")
    st.write("")

    if nav == "Documents":
        total = len(docs)
        idx = st.session_state.get("doc_i", 0) % total
        cap, b1, b2 = st.columns([10, 1, 1], vertical_alignment="center")
        cap.caption(f"Document {idx + 1} of {total} in preview ({total} on export)")
        b1.button("‹", key="prev", on_click=step_doc, args=(-1, total))
        b2.button("›", key="next", on_click=step_doc, args=(1, total))
        d, sym = docs[idx], SYMBOL[cur]
        rows = "".join(f"<tr><td>{l['item']}</td><td class='r'>{l['qty']}</td><td class='r'>{sym}{l['price']:,.2f}</td>"
                       f"<td class='r'>{sym}{l['amount']:,.2f}</td></tr>" for l in d["lines"])
        st.markdown(f"""<div class='doc'>
<div style='display:flex;justify-content:space-between;font-size:18px;border-bottom:1px solid #e4e6e3;padding-bottom:10px'>
<span>Invoice</span><span style='font-size:12px;color:#6b7686'>#{d['no']}</span></div>
<div style='display:flex;justify-content:space-between;margin:14px 0;font-size:13px'>
<div><b style='color:#127a68'>Billed to</b><br>{d['to']}</div><div><b style='color:#127a68'>From</b><br>{d['from']}</div>
<div><b style='color:#127a68'>Issued / due</b><br>{d['issued']} / {d['due']}</div></div>
<div class='tbl' style='border:0'><table><thead><tr><th>Item</th><th class='r'>Qty</th><th class='r'>Price</th>
<th class='r'>Amount</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class='tot'>Subtotal {sym}{d['subtotal']:,.2f}<br>Sales tax (8.0%) {sym}{d['tax']:,.2f}<br>
<b>Total: {sym}{d['total']:,.2f}</b></div></div>""", unsafe_allow_html=True)

    elif mode == "Preview":
        if nav == "Tabular":
            df = tables["customers"]
            f1, f2 = st.columns([3, 1], vertical_alignment="center")
            q = f1.text_input("Search", placeholder="Search any column…", label_visibility="collapsed")
            k = f2.slider("Rows", 5, 50, 12, label_visibility="collapsed", help="Preview rows")
            if q:
                df = df[df.astype(str).apply(lambda r: r.str.contains(q, case=False, regex=False).any(), axis=1)]
            html_table(df.head(k))
            st.markdown(f"<p class='cap'>Showing {min(k, len(df))} of {len(df)} rows"
                        f"{f' matching “{html.escape(q)}”' if q else ''}.</p>", unsafe_allow_html=True)
        else:
            tabs = st.tabs([f"{k}  {len(v)}" for k, v in tables.items()])
            for tab, (k, v) in zip(tabs, tables.items()):
                with tab:
                    html_table(v.head(12))
                    st.markdown(f"<p class='cap'>Showing {min(12, len(v))} of {len(v)} rows.</p>", unsafe_allow_html=True)

    else:  # Overview
        first = next(iter(tables.values()))
        miss = int(sum(t.isna().sum().sum() for t in tables.values()))
        cells = sum(t.size for t in tables.values())
        plural = f"in {len(tables)} table{'s' if len(tables) > 1 else ''}"
        st.markdown("<div class='h3' style='margin-top:0'>Overview</div><p class='ps'>Full dataset for the current "
                    "settings, not just the preview. Nothing is saved until you export or save it.</p>", unsafe_allow_html=True)
        for col, (label, val, foot) in zip(st.columns(4), [
                ("Rows", len(first), plural), ("Columns", first.shape[1], plural),
                ("Missing values", miss, f"{miss / cells * 100:.1f}% of {cells} cells"),
                ("Size", f"{size_kb(tables):.1f} KB", "measured as CSV")]):
            col.markdown(f"<div class='card'><small>{label}</small><b>{val}</b><small>{foot}</small></div>", unsafe_allow_html=True)

        st.markdown("<div class='h3'>Data explorer</div>", unsafe_allow_html=True)
        el, er = st.columns([1, 4])
        with el:
            pick = st.radio("Table", list(tables), key="explorer", label_visibility="collapsed",
                            format_func=lambda k: f"{k}  ({len(tables[k])} × {tables[k].shape[1]})")
        df = tables[pick]
        with er:
            m = int(df.isna().sum().sum())
            chip = f"<span class='chip'>{m} missing ({m / df.size * 100:.1f}%)</span>" if m else ""
            st.markdown(f"<b>{pick}</b>{chip}", unsafe_allow_html=True)
            profile_table(df)
            view = st.session_state.get("sample", "Head")
            sample = df.head(5) if view == "Head" else df.tail(5) if view == "Tail" else df.sample(min(5, len(df)), random_state=int(seed))
            st.markdown(f"<div class='h3' style='margin:14px 0 6px'>{'First' if view == 'Head' else 'Last' if view == 'Tail' else 'Random'} "
                        f"{len(sample)} of {len(df)} rows</div>", unsafe_allow_html=True)
            st.radio("Sample", ["Head", "Tail", "Random"], horizontal=True, key="sample", label_visibility="collapsed")
            html_table(sample, index_from=[i + 1 for i in sample.index])
            st.markdown("<div class='h3'>Column distribution</div>", unsafe_allow_html=True)
            col = st.selectbox("Column", list(df.columns), label_visibility="collapsed")
            s_ = df[col].dropna()
            if s_.empty or (s_.nunique() == len(s_) and not pd.api.types.is_numeric_dtype(s_)):
                st.caption("Every value is unique, so there is no distribution to show.")
            elif pd.api.types.is_numeric_dtype(s_) and s_.nunique() > 10:
                counts, edges = np.histogram(s_, bins=15)
                st.bar_chart(pd.Series(counts, index=[f"{e:,.0f}" for e in edges[:-1]]), color="#1a9c85")
            else:
                st.bar_chart(s_.astype(str).value_counts(), color="#1a9c85")