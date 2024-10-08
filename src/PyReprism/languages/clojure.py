import re
from PyReprism.utils import extension


class Clojure:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.clojure

    @staticmethod
    def keywords() -> list:
        # keyword = 'def|if|do|let|\.\.|quote|var|->>|->|fn|loop|recur|throw|try|monitor-enter|\.|new|set!|def\-|defn|defn\-|defmacro|defmulti|defmethod|defstruct|defonce|declare|definline|definterface|defprotocol|==|defrecord|>=|deftype|<=|defproject|ns|\*|\+|\-|\/|<|=|>|accessor|agent|agent-errors|aget|alength|all-ns|alter|and|append-child|apply|array-map|aset|aset-boolean|aset-byte|aset-char|aset-double|aset-float|aset-int|aset-long|aset-short|assert|assoc|await|await-for|bean|binding|bit-and|bit-not|bit-or|bit-shift-left|bit-shift-right|bit-xor|boolean|branch|butlast|byte|cast|char|children|class|clear-agent-errors|comment|commute|comp|comparator|complement|concat|conj|cons|constantly|cond|if-not|construct-proxy|contains|count|create-ns|create-struct|cycle|dec|deref|difference|disj|dissoc|distinct|doall|doc|dorun|doseq|dosync|dotimes|doto|double|down|drop|drop-while|edit|end|ensure|eval|every|false|ffirst|file-seq|filter|find|find-doc|find-ns|find-var|first|float|flush|for|fnseq|frest|gensym|get-proxy-class|get|hash-map|hash-set|identical|identity|if-let|import|in-ns|inc|index|insert-child|insert-left|insert-right|inspect-table|inspect-tree|instance|int|interleave|intersection|into|into-array|iterate|join|key|keys|keyword|keyword|last|lazy-cat|lazy-cons|left|lefts|line-seq|list\*|list|load|load-file|locking|long|loop|macroexpand|macroexpand-1|make-array|make-node|map|map-invert|map|mapcat|max|max-key|memfn|merge|merge-with|meta|min|min-key|name|namespace|neg|new|newline|next|nil|node|not|not-any|not-every|not=|ns-imports|ns-interns|ns-map|ns-name|ns-publics|ns-refers|ns-resolve|ns-unmap|nth|nthrest|or|parse|partial|path|peek|pop|pos|pr|pr-str|print|print-str|println|println-str|prn|prn-str|project|proxy|proxy-mappings|quot|rand|rand-int|range|re-find|re-groups|re-matcher|re-matches|re-pattern|re-seq|read|read-line|reduce|ref|ref-set|refer|rem|remove|remove-method|remove-ns|rename|rename-keys|repeat|replace|replicate|resolve|rest|resultset-seq|reverse|rfirst|right|rights|root|rrest|rseq|second|select|select-keys|send|send-off|seq|seq-zip|seq|set|short|slurp|some|sort|sort-by|sorted-map|sorted-map-by|sorted-set|special-symbol|split-at|split-with|str|string|struct|struct-map|subs|subvec|symbol|symbol|sync|take|take-nth|take-while|test|time|to-array|to-array-2d|tree-seq|true|union|up|update-proxy|val|vals|var-get|var-set|var|vector|vector-zip|vector|when|when-first|when-let|when-not|with-local-vars|with-meta|with-open|with-out-str|xml-seq|xml-zip|zero|zipmap|zipper|true|false|nil'.split('|')
        pass
        # return keyword

    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>;.*?$)|(?P<noncomment>[^;]*)', re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b[0-9A-Fa-f]+\b')
        return pattern

    @staticmethod
    def operator_regex():
        pattern = re.compile(r"(?:::|[:|'])\b[a-z][\w*+!?-]*\b")
        return pattern

    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Clojure.keywords()) + r')\b')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Clojure.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Clojure.keywords_regex()), '', source)
