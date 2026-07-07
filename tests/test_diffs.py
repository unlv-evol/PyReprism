"""Tests for unified/git diff processing."""
import io
import json

import pytest

from PyReprism import diffs
from PyReprism.cli import main
from PyReprism.diffs import LineKind

GIT_DIFF = '''diff --git a/src/app.py b/src/app.py
index 1234567..89abcde 100644
--- a/src/app.py
+++ b/src/app.py
@@ -1,5 +1,6 @@
 import os
-x = 1
+x = 2  # changed value
+# a brand new comment

 def main():
     pass
diff --git a/logo.png b/logo.png
index aaa..bbb 100644
Binary files a/logo.png and b/logo.png differ
'''


# --------------------------------------------------------------------- parsing
def test_parse_basic_structure():
    d = diffs.parse(GIT_DIFF)
    assert len(d) == 2
    app, logo = d.files
    assert app.new_path == 'src/app.py'
    assert app.language.__name__ == 'Python'
    assert logo.is_binary is True
    assert logo.language is None


def test_parse_line_kinds_and_numbers():
    app = diffs.parse(GIT_DIFF).files[0]
    added = [dl for h in app.hunks for dl in h.lines if dl.kind is LineKind.ADDED]
    removed = [dl for h in app.hunks for dl in h.lines if dl.kind is LineKind.REMOVED]
    assert [dl.text for dl in added] == ['x = 2  # changed value', '# a brand new comment']
    assert [dl.text for dl in removed] == ['x = 1']
    assert added[0].new_lineno == 2       # tracked against the new file
    assert removed[0].old_lineno == 2


def test_parse_plain_unified_without_git_header():
    text = '--- a/y.py\n+++ b/y.py\n@@ -1 +1 @@\n-x=1\n+x = 1\n'
    d = diffs.parse(text)
    assert len(d) == 1 and d.files[0].new_path == 'y.py'


def test_parse_new_and_deleted_files():
    text = ('diff --git a/new.py b/new.py\nnew file mode 100644\n--- /dev/null\n'
            '+++ b/new.py\n@@ -0,0 +1 @@\n+import os\n'
            'diff --git a/gone.py b/gone.py\ndeleted file mode 100644\n'
            '--- a/gone.py\n+++ /dev/null\n@@ -1 +0,0 @@\n-old = 1\n')
    new, gone = diffs.parse(text).files
    assert new.is_new and new.old_path is None and new.new_path == 'new.py'
    assert gone.is_deleted and gone.new_path is None and gone.old_path == 'gone.py'


# -------------------------------------------------------------- reconstruction
def test_reconstruction_text():
    app = diffs.parse(GIT_DIFF).files[0]
    assert app.added_text() == 'x = 2  # changed value\n# a brand new comment'
    assert app.removed_text() == 'x = 1'
    assert 'import os' in app.new_text() and 'x = 2' in app.new_text()
    assert 'x = 1' in app.old_text()


def test_language_aware_change_ops():
    app = diffs.parse(GIT_DIFF).files[0]
    assert app.extract_comments('added') == ['# changed value', '# a brand new comment']
    assert 'VAR1' in app.normalize('added')      # identifiers renamed
    assert app.tokenize('added')                 # non-empty token list


# ---------------------------------------------------------------------- churn
def test_diff_stats_splits_code_comment_blank():
    report = diffs.diff_stats(diffs.parse(GIT_DIFF))
    app = report.files[0]
    assert app.added_code == 1 and app.added_comment == 1
    assert app.removed_code == 1
    totals = report.totals()
    assert totals['files'] == 2
    assert totals['added_code'] == 1 and totals['added_comment'] == 1


def test_diff_report_json_and_csv():
    report = diffs.diff_stats(diffs.parse(GIT_DIFF))
    data = json.loads(report.to_json())
    assert data['totals']['files'] == 2
    assert report.to_csv().splitlines()[0].startswith('path,language,added_code')


# ------------------------------------------------------------------- cosmetic
def test_cosmetic_comment_only_change():
    text = '--- a/x.py\n+++ b/x.py\n@@ -1,2 +1,2 @@\n x = 1\n-# old\n+# new\n'
    assert diffs.is_cosmetic_change(diffs.parse(text).files[0]) is True


def test_cosmetic_whitespace_only_change():
    text = '--- a/x.py\n+++ b/x.py\n@@ -1 +1 @@\n-x=1\n+x = 1\n'
    assert diffs.is_cosmetic_change(diffs.parse(text).files[0]) is True


def test_real_change_is_not_cosmetic():
    text = '--- a/x.py\n+++ b/x.py\n@@ -1 +1 @@\n-x = 1\n+x = 99\n'
    assert diffs.is_cosmetic_change(diffs.parse(text).files[0]) is False


def test_cosmetic_files_helper():
    two = ('--- a/a.py\n+++ b/a.py\n@@ -1,2 +1,2 @@\n x = 1\n-# old\n+# new\n'
           '--- a/b.py\n+++ b/b.py\n@@ -1 +1 @@\n-y = 1\n+y = 2\n')
    cosmetic = diffs.cosmetic_files(diffs.parse(two))
    assert [f.path for f in cosmetic] == ['a.py']


# ------------------------------------------------------------------ full-file
def test_full_file_mode_reclassifies_block_comment():
    text = ('--- a/c.js\n+++ b/c.js\n@@ -2,2 +2,3 @@\n'
            '   line inside comment\n'
            '+  another inside the block comment\n'
            '   more comment text\n')
    f = diffs.parse(text).files[0]
    # fragment mode: the added line looks like code
    frag = diffs._side_counts(f, 'added')
    assert frag['code'] == 1 and frag['comment'] == 0
    # full-file mode: accurate classification as comment
    f.new_source = ('/*\n  line inside comment\n  another inside the block comment\n'
                    '  more comment text\n*/\ncode = 1\n')
    accurate = diffs._side_counts(f, 'added')
    assert accurate['comment'] == 1 and accurate['code'] == 0


# ------------------------------------------------------------------------ CLI
def test_cli_diff_text_report(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(GIT_DIFF))
    assert main(['diff', '--per-file']) == 0
    out = capsys.readouterr().out
    assert 'src/app.py' in out and '2 files' in out


def test_cli_diff_json(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(GIT_DIFF))
    assert main(['diff', '--json']) == 0
    data = json.loads(capsys.readouterr().out)
    assert data['totals']['added_comment'] == 1


def test_cli_diff_cosmetic(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin',
                        io.StringIO('--- a/x.py\n+++ b/x.py\n@@ -1,2 +1,2 @@\n x = 1\n-# old\n+# new\n'))
    assert main(['diff', '--cosmetic']) == 0
    assert capsys.readouterr().out.strip() == 'x.py'
