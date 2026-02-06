# 実験記録の自動化：足りないのはツールではなく、「デフォルトの動作」だ

![イラスト](../images/06_logging_path.png)


## イントロダクション：3ヶ月後の「考古学」

![コード考古学](../images/comics/06_archaeology.png)

論文が採択されました。しかし、査読者から補足資料として、表4のある実験の具体的な設定を説明するよう求められました。あなたはコードリポジトリを開き、「考古学」を始めます。

**ステップ1：ログを探す**

その実験を走らせたのは3ヶ月前だったはずです。`outputs/` ディレクトリを開くと、日付の名前がついたフォルダが山ほどあります。問題は、正確な日付を覚えていないことです。あなたは一つずつ開き、中身を見てその実験の結果かどうかを確認するしかありません。

**ステップ2：設定を探す**

ようやく結果ファイルを見つけましたが、設定（ハイパーパラメータ）が記録されていません。コードの履歴をさかのぼり、当時使っていた超パラメータを探しようとします。あるコミットにそれらしい設定を見つけましたが、それが最終バージョンかどうか確信が持てません —— 当時、学習率を一時的に書き換えた記憶がありますが、いくらにしたか覚えていないのです。

**ステップ3：データを探す**

コード内にはデータのパスが `data/v2/` と書かれていますが、現在のデータディレクトリは `data/v3/` です。当時、データのバージョンを差し替えたのかどうかも思い出せません。チャット履歴で「データ」と検索し、手がかりを探します。

**ステップ4：諦める**

午後の時間を丸一日潰した挙げ句、あなたは実験を再実行することに決めました。しかし、パラメータが不確実なため、再実行の結果が論文で報告した数値と一致しません。結局、補足資料にはこう書くしかありませんでした。「時間が経過したため、一部の実験の詳細に差異がある可能性があります。」

**査読者の返信**：「著者が自分たちの結果を再現できない論文を受理することはできません。」

### この悲劇は、防げたはずです。

実験が終わった直後に **2分** かけて鍵となる情報を記録していれば、3ヶ月後の悪夢は避けられたでしょう。

問題はツール（MLflow、W&B、TensorBoardなどはどれも優秀です）が足りないことではなく、**「記録する」というデフォルトの動作が欠けていること**です。多くの人が「今回はちょっと試すだけだから記録は不要」と考え、試行錯誤を繰り返すうちに記録を忘れ、最終的に価値のある実験の痕跡すら残らなくなってしまうのです。

## 2層ログ戦略：機械の正確さと人間の簡潔さ

![2層ログ](../images/comics/06_two_layer_logging.png)

実験記録における最大の課題は、2つのニーズのバランスを取ることにあります。

- **機械には完全で正確な情報が必要**（再現や自動分析のため）

- **人間には簡潔で読みやすい要約が必要**（素早い振り返りや意思決定のため）

機械用のログ（JSONなど）しかない場合、人間が「この実験で結局何を検証したかったのか」を即座に理解するのは困難です。一方で、人間用のログ（メモなど）しかない場合、機械による自動再現や比較は不可能です。

**解決策：2つの層に分け、それぞれに役割を持たせる。**

### 第1層：機械用ログ（run.json）

![06 08 run json structure](../images/comics/06_08_run_json_structure.png)

**目的**：再現と自動化のために、完全で構造化された情報を提供する。

**原則**：

- **自動生成**：人間の入力に頼らず、スクリプトで自動的に収集する。

- **構造化**：プログラムで解析や照会が容易な JSON 形式にする。

- **完全性**：再現に必要なすべての重要情報を含める。

**最小限のフィールドセット**（そのままコピーして使えます）：

```json
{
  "run_id": "2026-02-01_1630_ablation_lr",
  "timestamp": {
    "start": "2026-02-01T16:30:45",
    "end": "2026-02-01T18:45:12"
  },
  "git": {
    "commit": "a1b2c3d4e5f6",
    "dirty": false,
    "branch": "exp/ablation-lr",
    "remote": "git@github.com:user/project.git"
  },
  "config": {
    "path": "configs/ablation_lr.yaml",
    "hash": "sha256:abcd1234...",
    "resolved": {
      "model": "transformer",
      "learning_rate": 3e-4,
      "batch_size": 32,
      ...
    }
  },
  "data": {
    "name": "dataset_v3",
    "path": "/data/project/v3",
    "hash": "sha256:ef567890...",
    "split": {
      "train": 8000,
      "val": 1000,
      "test": 1000
    }
  },
  "environment": {
    "python": "3.11.7",
    "cuda": "12.1",
    "platform": "Linux-5.15.0-x86_64",
    "gpu": "NVIDIA A100-SXM4-40GB",
    "pip_freeze_hash": "sha256:12345678..."
  },
  "random": {
    "seed": 42,
    "torch_seed": 42,
    "numpy_seed": 42,
    "python_seed": 42
  },
  "metrics": {
    "val_loss": 0.123,
    "val_acc": 0.943,
    "test_loss": 0.145,
    "test_acc": 0.931,
    "training_time_hours": 2.25
  },
  "artifacts": {
    "model": "outputs/2026-02-01_1630_ablation_lr/model.pt",
    "logs": "outputs/2026-02-01_1630_ablation_lr/train.log",
    "predictions": "outputs/2026-02-01_1630_ablation_lr/predictions.json",
    "plots": "outputs/2026-02-01_1630_ablation_lr/plots/"
  }
}
```

#### 重要フィールドの解説：

- **run_id**：一意の識別子。第2章で述べたように、「タイムスタンプ + 短い説明」を推奨します。

- **git.commit**：コードのバージョン。`git rev-parse HEAD` で取得します。

- **git.dirty**：コミットされていない変更があるかどうか。`git diff-index --quiet HEAD --` でチェックします。もし `true` なら、`git diff > changes.patch` でその差異を保存しておくのが得策です。

- **config.resolved**：デフォルト値も含めて、最終的に適用されたすべての設定値。コードが更新されるとデフォルト値も変わる可能性があるため、この記録は非常に重要です。

- **data.hash**：データのバージョンのハッシュ値。データが完全に同一であることを保証します。ディレクトリ全体のハッシュを `sha256sum` で計算するか、DVC などのツールを使用します。

- **environment.pip_freeze_hash**：依存ライブラリのバージョンのハッシュ。`pip freeze | sha256sum` で計算します。`pip freeze` の出力をそのまま保存すると長すぎるため、ハッシュ値と元のファイルパスだけを記録します。

- **random.seed**：すべての乱数シード。PyTorch、NumPy、Python 標準의 random すべてにシードを設定してください。

### 第2層：人間用ログ（run.md）

![06 09 run md template](../images/comics/06_09_run_md_template.png)

**目的**：人間（未来の自分を含む）のために、実験内容を即座に理解するための要約を提供する。

**原則**：

- **簡潔**：10行以内。核心的な情報が一目でわかるようにする。

- **構造化**：固定された「5つの要素」で構成する。

- **手書き**：主観的な判断や洞察を含めることを許容する。

**5つの要素テンプレート**（5行で十分です）：

```markdown
# Run: 2026-02-01_1630_ablation_lr

## 仮説 (Hypothesis)
学習率が収束速度と最終的な性能に与える影響をテストする。予想：小さめの学習率 (1e-4) の方が安定する。

## 変更点 (Change)
ベースライン (lr=3e-4) と比較して、学習率を 1e-4 に下げた。他のハイパーパラメータは変更なし。

## 結論 (Result)
- 収束が遅くなった (50 epoch から 80 epoch へ)
- 最終性能はわずかに向上した (val_acc: 0.943 vs 0.938)
- 訓練はより安定し、loss 曲線に目立った振動はない

## 次のステップ (Next)
中間値の 2e-4 を試す。速度と性能のバランスが取れる可能性がある。
Learning rate warmup 戦略を検討する。

## リスク/異常 (Risk)
目立った異常なし。データ拡張については、現在の固定設定から調整が必要かもしれない。
```

#### なぜ「わずか5行」なのか？

- **記録のハードルを下げる**：長い文書を書こうとすると後回しにしがちですが、5行なら2分で終わります。

- **核心を抽出させる**：単なる日記ではなく、「この実験で結局何がわかったのか」を強制的に考えさせます。

- **素早い振り返り**：数ヶ月後に見返したとき、完全なログよりも5行の要約の方がはるかに役に立ちます。

## 自動化ツール：記録を「コストゼロ」の行動にする

![自動記録](../images/comics/06_auto_logging.png)

**核心的な考え方**：記録は「忘れずにやること」ではなく、「自動的に行われること」であるべきです。

### 訓練スクリプトでの run.json 自動生成

#### 実装例 (Python)：

```python
import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime

def log_run(run_id, config, metrics, output_dir):
    """
    実験情報を run.json に自動的に記録する

    Args:
        run_id: 実験の一意の識別子
        config: 設定辞書（解決済み）
        metrics: 最終的な指標辞書
        output_dir: 出力ディレクトリのパス
    """
    run_info = {
        "run_id": run_id,
        "timestamp": {
            "start": datetime.now().isoformat(),
        },
        "git": get_git_info(),
        "config": {
            "resolved": config,
            "hash": hash_dict(config),
        },
        "data": get_data_info(config.get("data_path")),
        "environment": get_env_info(),
        "random": get_random_seeds(config),
        "metrics": metrics,
        "artifacts": {
            "model": str(output_dir / "model.pt"),
            "logs": str(output_dir / "train.log"),
        }
    }

    # ファイルに保存
    run_file = output_dir / "run.json"
    with open(run_file, "w") as f:
        json.dump(run_info, f, indent=2)

    print(f"Run info logged to {run_file}")

def get_git_info():
    """git 情報を取得する"""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"]
        ).decode().strip()

        # 未コミットの変更があるかチェック
        subprocess.check_call(
            ["git", "diff-index", "--quiet", "HEAD", "--"]
        )
        dirty = False
    except subprocess.CalledProcessError:
        dirty = True

    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    ).decode().strip()

    remote = subprocess.check_output(
        ["git", "config", "--get", "remote.origin.url"]
    ).decode().strip()

    return {
        "commit": commit,
        "dirty": dirty,
        "branch": branch,
        "remote": remote
    }

def get_data_info(data_path):
    """データ情報を取得する"""
    data_path = Path(data_path)

    # データディレクトリのハッシュ計算（簡略版、実際は DVC 等を推奨）
    return {
        "name": data_path.name,
        "path": str(data_path.absolute()),
    }

def get_env_info():
    """環境情報を取得する"""
    import sys
    import platform

    env = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }

    # CUDA バージョンの取得（利用可能な場合）
    try:
        import torch
        env["cuda"] = torch.version.cuda
        env["pytorch"] = torch.__version__
        if torch.cuda.is_available():
            env["gpu"] = torch.cuda.get_device_name(0)
    except ImportError:
        pass

    # pip freeze を別ファイルに保存
    pip_freeze = subprocess.check_output(
        ["pip", "freeze"]
    ).decode()
    pip_file = Path("requirements_freeze.txt")
    pip_file.write_text(pip_freeze)

    env["pip_freeze_hash"] = hashlib.sha256(
        pip_freeze.encode()
    ).hexdigest()[:16]

    return env

def get_random_seeds(config):
    """ランダムシードを抽出する"""
    return {
        "seed": config.get("seed", None),
        "torch_seed": config.get("torch_seed", None),
        "numpy_seed": config.get("numpy_seed", None),
    }

def hash_dict(d):
    """辞書のハッシュを計算する"""
    import json
    return hashlib.sha256(
        json.dumps(d, sort_keys=True).encode()
    ).hexdigest()[:16]
```

#### 訓練スクリプトでの使用法：

```python
# train.py

import argparse
from pathlib import Path
from run_logger import log_run  # 上記のツール

def main():
    args = parse_args()

    # run_id と出力ディレクトリの作成
    run_id = f"{datetime.now().strftime('%Y-%m-%d_%H%M')}_{args.exp_name}"
    output_dir = Path("outputs") / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    # 設定のロードと展開
    config = load_config(args.config)
    config = resolve_config(config, args)  # デフォルト値をすべて展開

    # ランダムシードの設定
    set_random_seeds(config["seed"])

    # モデルの訓練
    model, metrics = train_model(config, output_dir)

    # 実験情報の自動記録
    log_run(
        run_id=run_id,
        config=config,
        metrics=metrics,
        output_dir=output_dir
    )

    # run.md の記入を促す
    print(f"\n{'='*60}")
    print(f"[OK] Experiment completed: {run_id}")
    print(f"[NOTE] Please write a brief summary in:")
    print(f"    {output_dir / 'run.md'}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
```

### テンプレートによる run.md 記入の簡略化

出力ディレクトリに `run.md` のテンプレートを自動生成します：

```python
def create_run_md_template(output_dir, run_id):
    """run.md のテンプレートを作成する"""
    template = f"""# Run: {run_id}

## 仮説 (Hypothesis)
[この実験で何を検証したいか？ 予想される結果は？]

## 変更点 (Change)
[以前の実験と比較して、何を変えたか？]

## 結論 (Result)
[実験結果はどうだったか？ 意外な発見はあったか？]

## 次のステップ (Next)
[今回の結果をもとに、次は何をする予定か？]

## リスク/異常 (Risk)
[注目すべき異常やリスクはあるか？]
"""

    md_file = output_dir / "run.md"
    if not md_file.exists():
        md_file.write_text(template)
        print(f"[NOTE] run.md template created at {md_file}")
```

これにより、実験が終わるたびに白紙から書き始める必要がなくなり、空欄を埋めるだけで済みます。

## 既存ツールとの統合

### MLflow との統合

![06 10 mlflow integration](../images/comics/06_10_mlflow_integration.png)

すでに MLflow を使用している場合は、`run.json` の情報を MLflow に同期できます：

```python
import mlflow

def log_to_mlflow(run_info):
    """run.json の情報を MLflow に記録する"""
    with mlflow.start_run(run_name=run_info["run_id"]):
        # パラメータの記録
        mlflow.log_params(run_info["config"]["resolved"])

        # 指標の記録
        mlflow.log_metrics(run_info["metrics"])

        # 環境情報の記録
        mlflow.log_dict(run_info["environment"], "environment.json")

        # git 情報の記録
        mlflow.set_tag("git.commit", run_info["git"]["commit"])
        mlflow.set_tag("git.branch", run_info["git"]["branch"])
        mlflow.set_tag("git.dirty", run_info["git"]["dirty"])

        # 成果物の記録
        mlflow.log_artifact(run_info["artifacts"]["model"])
```

### Weights & Biases との統合

```python
import wandb

def log_to_wandb(run_info):
    """run.json の情報を W&B に記録する"""
    wandb.init(
        project="my-research",
        name=run_info["run_id"],
        config=run_info["config"]["resolved"],
        tags=[run_info["git"]["branch"]]
    )

    # 指標の記録
    wandb.log(run_info["metrics"])

    # 環境と git 情報の記録
    wandb.config.update({
        "git_commit": run_info["git"]["commit"],
        "git_dirty": run_info["git"]["dirty"],
        "python_version": run_info["environment"]["python"],
    })

    # モデルの保存
    wandb.save(run_info["artifacts"]["model"])
```

**重要なポイント**：ツールは補助に過ぎません。核心は **「記録の規範（ルール）」** です。MLflow や W&B がなくても、`run.json` と `run.md` があれば十分です。

## ログのクエリと分析

構造化された `run.json` があれば、実験の結果を素早く検索し、比較することができます。

### 最良の実験を見つける

```python
# find_best_run.py

import json
from pathlib import Path

def find_best_runs(metric="test_acc", top_k=5):
    """指標が最も良い実験を探す"""
    runs = []

    for run_dir in Path("outputs").iterdir():
        if not run_dir.is_dir():
            continue

        run_json = run_dir / "run.json"
        if not run_json.exists():
            continue

        with open(run_json) as f:
            run_info = json.load(f)

        if metric in run_info.get("metrics", {}):
            runs.append({
                "run_id": run_info["run_id"],
                metric: run_info["metrics"][metric],
                "config": run_info["config"]["resolved"]
            })

    # ソート
    runs.sort(key=lambda x: x[metric], reverse=True)

    print(f"Top {top_k} runs by {metric}:")
    for i, run in enumerate(runs[:top_k], 1):
        print(f"{i}. {run['run_id']}: {run[metric]:.4f}")
        print(f"   Config: lr={run['config'].get('learning_rate')}, "
              f"bs={run['config'].get('batch_size')}")

    return runs[:top_k]

if __name__ == "__main__":
    find_best_runs()
```

### 2つの実験の設定の差異を比較する

```python
# compare_runs.py

import json
from pathlib import Path

def compare_runs(run_id1, run_id2):
    """2つの実験の設定と結果を比較する"""
    run1 = load_run(run_id1)
    run2 = load_run(run_id2)

    print(f"Comparing {run_id1} vs {run_id2}\n")

    # 設定の比較
    config1 = run1["config"]["resolved"]
    config2 = run2["config"]["resolved"]

    print("Configuration differences:")
    for key in set(config1.keys()) | set(config2.keys()):
        val1 = config1.get(key, "N/A")
        val2 = config2.get(key, "N/A")
        if val1 != val2:
            print(f"  {key}: {val1} -> {val2}")

    # 指標の比較
    print("\nMetrics:")
    metrics1 = run1.get("metrics", {})
    metrics2 = run2.get("metrics", {})
    for key in set(metrics1.keys()) & set(metrics2.keys()):
        val1 = metrics1[key]
        val2 = metrics2[key]
        diff = val2 - val1
        print(f"  {key}: {val1:.4f} -> {val2:.4f} "
              f"({diff:+.4f}, {diff/val1*100:+.2f}%)")

def load_run(run_id):
    """実験情報をロードする"""
    run_json = Path("outputs") / run_id / "run.json"
    with open(run_json) as f:
        return json.load(f)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python compare_runs.py <run_id1> <run_id2>")
        sys.exit(1)

    compare_runs(sys.argv[1], sys.argv[2])
```

## よくある質問と解決策

### Q1：run.json が大きくなりすぎる場合は？

**問題**：モデル定義やデータの詳細プリプロセスなど、完全な設定を保存すると `run.json` が肥大化する可能性がある。

**解決策**：

- `run.json` には重要なハイパーパラメータ（学習率、バッチサイズなど）だけを保存する。

- 詳細な設定は `config_resolved.yaml` などの別ファイルに保存する。

- `run.json` にはその設定ファイルへのパスとハッシュ値だけを記録する。

### Q2：run.md を書くのを忘れたら？

**解決策**：

- Makefile や実行スクリプトにチェックを組み込む：

  ```bash
  if [ ! -f outputs/$RUN_ID/run.md ]; then
      echo "Warning: run.md not found for $RUN_ID"
      echo "Please write a summary before continuing."
  fi
  ```

- 定期的（たとえば毎週金曜日）に `run.md` が欠けている実験をチェックし、まとめて追记する。

- どうしても思い出せない場合は「忘失」とだけ書く。何もないよりはマシです。

### Q3：数据が大きすぎてハッシュ計算ができない場合は？

**解決策**：

- データバージョン管理ツール（DVC や Git LFS など）を使用する。

- あるいは、データの「目録ファイル（manifest）」だけを記録する：

  ```bash
  # 目録の生成
  find data/ -type f | xargs sha256sum > data_manifest.txt

  # 目録のハッシュを計算
  sha256sum data_manifest.txt
  ```

- `run.json` にはこの目録ファイルへのパスとハッシュ値を記録する。

## 10分間アクション：次の実験のために自動記録をセットアップする

今すぐできることが一つあるとすれば、自動記録の最小限のシステムを構築することです。

1.  **run_logger.py をコピーする**
    上記の `log_run` 関数を自分のプロジェクトにコピーします。

2.  **訓練スクリプトの最後で呼び出す**
    ```python
    # 訓練終了後
    log_run(run_id, config, metrics, output_dir)
    ```

3.  **run.md のテンプレートを作成する**
    ```python
    create_run_md_template(output_dir, run_id)
    ```

4.  **一度実験を走らせてテストする**
    実験を実行し、以下を確認します：
    - `outputs/<run_id>/run.json` が自動生成されているか。
    - `outputs/<run_id>/run.md` のテンプレートが生成されているか。
    - `run.json` の情報（git, config, env, metrics）が完全か。

5.  **run.md を記入する**
    2分かけて「5つの要素」テンプレートを埋めます。

次の実験から、記録は「自動的」で「コストゼロ」になります。あなたがすべき唯一のことは、たった2分、5行の要約を書くことだけです —— この投資は、3ヶ月後に100倍의 価値になって返ってくるはずです。
