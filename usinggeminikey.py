# --- 0) Install dependencies ---
!pip install google-generativeai --quiet

import os, json, subprocess, re
import google.generativeai as genai

# ---------- 1) Install node + node-sql-parser ----------
print("Installing nodejs + npm...")
subprocess.run(["apt-get", "update"], check=True, stdout=subprocess.DEVNULL)
subprocess.run(["apt-get", "install", "-y", "nodejs", "npm"], check=True, stdout=subprocess.DEVNULL)

project_dir = "/content/node_sql_parser_demo"
os.makedirs(project_dir, exist_ok=True)
os.chdir(project_dir)

print("Installing node-sql-parser...")
subprocess.run(["npm", "init", "-y"], check=True, stdout=subprocess.DEVNULL)
subprocess.run(["npm", "install", "node-sql-parser@latest"], check=True, stdout=subprocess.DEVNULL)

# ---------- 2) Node helper ----------
node_helper = """
const { Parser } = require('node-sql-parser');
const parser = new Parser();
const sql = process.argv.slice(2).join(" ");
try {
  const ast = parser.astify(sql);
  console.log(JSON.stringify(ast, null, 2));
} catch (err) {
  console.error(JSON.stringify({error: err.message}));
  process.exit(2);
}
"""
with open("node_parse.js", "w") as f:
    f.write(node_helper)

def parse_with_node(sql: str):
    """Call node-sql-parser and return AST as dict"""
    cmd = ["node", "node_parse.js", sql]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(proc.stdout)
    except subprocess.CalledProcessError as e:
        try:
            return json.loads(e.stderr)
        except Exception:
            return {"error": e.stderr.strip()}

# ---------- 3) Few-shot examples ----------
examples = [
    "SELECT id, name FROM users WHERE age > 30 ORDER BY id DESC;",
    "SELECT COUNT(*) as cnt FROM orders WHERE status = 'shipped';",
    "INSERT INTO accounts (id, balance) VALUES (1, 1000);"
]

dataset = [{"sql": sql, "ast": parse_with_node(sql)} for sql in examples]

examples_text = ""
for ex in dataset[:2]:
    examples_text += f"SQL:\n{ex['sql']}\n\nAST (node-sql-parser JSON):\n"
    examples_text += json.dumps(ex["ast"], separators=(',', ':'), ensure_ascii=False) + "\n\n---\n\n"

system_msg = """You are a JSON-only generator. 
Given an SQL query, produce a JSON AST that matches the `node-sql-parser` npm package.
Rules:
1) Output must be valid JSON only.
2) Use the same keys/nesting as node-sql-parser AST.
3) If you cannot parse, return {"error": "..."}.
"""

# ---------- 4) Configure Gemini ----------
GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY", None) or "YOUR_GEMINI_API_KEY"
if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
    print("⚠️ Set your Gemini API key: os.environ['GOOGLE_API_KEY'] = '...' ")

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

def call_llm_to_generate_ast_gemini(sql_query: str):
    prompt = f"{system_msg}\n\n{examples_text}\nSQL:\n{sql_query}\n\nAST (node-sql-parser JSON):\n"
    resp = gemini_model.generate_content(prompt)
    content = resp.text.strip()
    # Remove accidental markdown fences
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)
    return json.loads(content)

# ---------- 5) Accuracy Scoring ----------
def compare_json(gold, pred):
    """Recursively compare JSON and count matches/total keys"""
    matches, total = 0, 0
    if isinstance(gold, dict) and isinstance(pred, dict):
        for k in gold:
            total += 1
            if k in pred:
                sub_m, sub_t = compare_json(gold[k], pred[k])
                matches += sub_m
                total += sub_t
        return matches, total
    elif isinstance(gold, list) and isinstance(pred, list):
        for g, p in zip(gold, pred):
            sub_m, sub_t = compare_json(g, p)
            matches += sub_m
            total += sub_t
        total += abs(len(gold) - len(pred))  # count unmatched
        return matches, total
    else:
        total += 1
        if gold == pred:
            matches += 1
        return matches, total

def score_accuracy(gold, pred):
    if gold == pred:
        return {"exact_match": 1, "match_percent": 100.0}
    matches, total = compare_json(gold, pred)
    return {
        "exact_match": 0,
        "match_percent": round((matches/total)*100, 2) if total > 0 else 0.0,
        "matches": matches,
        "total": total
    }

# ---------- 6) Batch Testing ----------
test_sqls = [
    "UPDATE products SET price = price * 1.1 WHERE category = 'books';",
    "DELETE FROM logs WHERE created_at < '2024-01-01';",
    "SELECT u.id, COUNT(o.id) FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.id;",
    "CREATE TABLE employees (id INT PRIMARY KEY, name VARCHAR(100), salary DECIMAL);",
    "INSERT INTO students (id, name, grade) VALUES (1, 'Alice', 'A');",
    "ALTER TABLE accounts ADD COLUMN last_login TIMESTAMP;",
    "DROP TABLE temp_data;",
    "SELECT * FROM customers WHERE city IN ('Paris', 'London');",
    "SELECT name, SUM(amount) FROM sales GROUP BY name HAVING SUM(amount) > 5000;",
    "SELECT DISTINCT country FROM customers;"
]

results = []
for sql in test_sqls:
    gold_ast = parse_with_node(sql)
    try:
        llm_ast = call_llm_to_generate_ast_gemini(sql)
        score = score_accuracy(gold_ast, llm_ast)
    except Exception as e:
        score = {"error": str(e), "exact_match": 0, "match_percent": 0.0}
    results.append({"sql": sql, "score": score})

# Report
print("\n--- Batch Accuracy Report ---")
total_exact = sum(r["score"].get("exact_match", 0) for r in results)
avg_match = sum(r["score"].get("match_percent", 0) for r in results) / len(results)
print(f"Exact Matches: {total_exact}/{len(results)}")
print(f"Average Structural Match: {avg_match:.2f}%\n")

for r in results:
    print(f"SQL: {r['sql']}")
    print("Score:", r["score"])
    print("---")
