"""Module for SpaczzRuler."""
from __future__ import annotations

from collections import defaultdict, OrderedDict
from pathlib import Path
from typing import Any, DefaultDict, Iterable, Optional, Union
import warnings

from spacy.language import Language
from spacy.tokens import Doc, Span
import srsly

from ..exceptions import PatternTypeWarning
from ..matcher import FuzzyMatcher, RegexMatcher, TokenMatcher
from ..util import ensure_path, read_from_disk, write_to_disk


DEFAULT_ENT_ID_SEP = "||"


class SpaczzRuler:
    """The SpaczzRuler adds fuzzy and multi-token regex matches to spaCy `Doc.ents`.

    It can be combined with other spaCy NER components like the statistical
    EntityRecognizer and/or the EntityRuler to boost accuracy.
    After initialization, the component is typically added to the pipeline
    using `nlp.add_pipe()`.

    Attributes:
        nlp: The shared nlp object to pass the vocab to the matchers
            (not currently used by spaczz matchers) and process fuzzy patterns.
        fuzzy_patterns:
            Patterns added to the fuzzy matcher.
        regex_patterns:
            Patterns added to the regex matcher.
        token_patterns:
            Patterns added to the token matcher
        defaults: Default matching settings for their respective matchers.
            Details to be updated.
        fuzzy_matcher: The `FuzzyMatcher` instance
            the spaczz ruler will use for fuzzy phrase matching.
        regex_matcher: The `RegexMatcher` instance
            the spaczz ruler will use for regex phrase matching.
        token_matcher: The `TokenMatcher` instance
            the spaczz ruler will use for token matching.
    """

    name = "spaczz_ruler"

    def __init__(self: SpaczzRuler, nlp: Language, **cfg: Any) -> None:
        """Initialize the spaczz ruler with a Language object and cfg parameters.

        All spaczz ruler cfg parameters are prepended with `"spaczz_"`.
        If `spaczz_patterns` is supplied here, they need to be a list of
        spaczz patterns: dictionaries with "label", "pattern", and "type" keys,
        and if the patterns are fuzzy or regex phrase patterns they can
        include the optional "kwargs" keys.
        For example, a fuzzy phrase pattern:
        {'label': 'ORG', 'pattern': 'Apple', 'type': 'fuzzy', 'kwargs': {'min_r2': 90}}
        Or, a token pattern:
        {'label': 'ORG', 'pattern': [{'TEXT': {'FUZZY': 'Apple'}}], 'type': 'token'}


        Args:
            nlp: The shared `Language` object to pass the vocab to the matchers
                and process fuzzy patterns.
            **cfg: Other config parameters. The SpaczzRuler makes heavy use
                of cfg to pass additional parameters down to the matchers.
                spaczz config parameters start with "spaczz_" to keep them
                from colliding with other cfg components.
                SpaczzRuler cfg components include (with "spaczz_" prepended to them):
                    `overwrite_ents` (bool): Whether to overwrite exisiting Doc.ents
                        with new matches. Default is False.
                    `ent_id_sep` (str): String to separate entity labels and ids on.
                    `fuzzy_defaults` (dict[str, Any]): Modified default parameters to
                        use with the fuzzy matcher. Default is an empty dictionary -
                        utilizing defaults.
                    `regex_defaults` (dict[str, Any]): Modified default parameters to
                        use with the regex matcher. Default is an empty dictionary -
                        utilizing defaults.
                    `token_defaults` (dict[str, Any]): Modified default parameters to
                        use with the spaczz matcher. Default is an empty dictionary -
                        utilizing defaults.
                    `regex_config` (Union[str, RegexConfig]): Config to use with the
                        regex matcher. Default is "default".
                        See RegexMatcher/RegexSearcher documentation for available
                        parameter details.
                    `patterns` (Iterable[dict[str, Any]]): Patterns to initialize
                        the ruler with. Default is None.
                If the spaczz ruler is loaded as part of a model pipeline,
                cfg will include all keyword arguments passed to `spacy.load()`.

        Raises:
            TypeError: If spaczz_{name}_defaults passed are not dictionaries.
        """
        self.nlp = nlp
        self.fuzzy_patterns: DefaultDict[str, DefaultDict[str, Any]] = defaultdict(
            lambda: defaultdict(list)
        )
        self.regex_patterns: DefaultDict[str, DefaultDict[str, Any]] = defaultdict(
            lambda: defaultdict(list)
        )
        self.token_patterns: DefaultDict[str, list[list[dict[str, Any]]]] = defaultdict(
            list
        )
        self.ent_id_sep = cfg.get("spaczz_ent_id_sep", DEFAULT_ENT_ID_SEP)
        self._ent_ids: dict[Any, Any] = defaultdict(dict)
        self.overwrite = cfg.get("spaczz_overwrite_ents", False)
        default_names = (
            "spaczz_fuzzy_defaults",
            "spaczz_regex_defaults",
            "spacy_token_defaults",
        )
        self.defaults = {}
        for name in default_names:
            if name in cfg:
                if isinstance(cfg[name], dict):
                    self.defaults[name] = cfg[name]
                else:
                    raise TypeError(
                        (
                            "Defaults must be a dictionary of keyword arguments,",
                            f"not {type(cfg[name])}.",
                        )
                    )
        self.fuzzy_matcher = FuzzyMatcher(
            nlp.vocab, **self.defaults.get("spaczz_fuzzy_defaults", {}),
        )
        self.regex_matcher = RegexMatcher(
            nlp.vocab,
            cfg.get("spaczz_regex_config", "default"),
            **self.defaults.get("spaczz_regex_defaults", {}),
        )
        self.token_matcher = TokenMatcher(
            nlp.vocab, **self.defaults.get("spaczz_token_defaults", {})
        )
        patterns = cfg.get("spaczz_patterns")
        if patterns is not None:
            self.add_patterns(patterns)

    def __call__(self: SpaczzRuler, doc: Doc) -> Doc:
        """Find matches in document and add them as entities.

        Args:
            doc: The Doc object in the pipeline.

        Returns:
            The Doc with added entities, if available.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> doc = nlp.make_doc("My name is Anderson, Grunt")
            >>> ruler.add_patterns([{"label": "NAME", "pattern": "Grant Andersen",
                "type": "fuzzy", "kwargs": {"fuzzy_func": "token_sort"}}])
            >>> doc = ruler(doc)
            >>> "Anderson, Grunt" in [ent.text for ent in doc.ents]
            True
        """
        fuzzy_matches = []
        ratio_lookup: dict[tuple[str, int, int], int] = {}
        for fuzzy_match in self.fuzzy_matcher(doc):
            fuzzy_matches.append(fuzzy_match[:3])
            current_ratio = fuzzy_match[3]
            best_ratio = ratio_lookup.get(fuzzy_match[:3], 0)
            if current_ratio > best_ratio:
                ratio_lookup[fuzzy_match[:3]] = current_ratio
        regex_matches = []
        counts_lookup: dict[tuple[str, int, int], tuple[int, int, int]] = {}
        for regex_match in self.regex_matcher(doc):
            regex_matches.append(regex_match[:3])
            current_counts = regex_match[3]
            best_counts = counts_lookup.get(regex_match[:3])
            if not best_counts or sum(current_counts) < sum(best_counts):
                counts_lookup[regex_match[:3]] = current_counts
        token_matches = []
        details_lookup: dict[tuple[str, int, int], int] = {}
        for token_match in self.token_matcher(doc):
            token_matches.append(token_match[:3])
            details_lookup[token_match[:3]] = 1
        matches = fuzzy_matches + regex_matches + token_matches
        unique_matches = set(
            [(match_id, start, end) for match_id, start, end in matches if start != end]
        )
        sorted_matches = sorted(
            unique_matches, key=lambda m: (m[2] - m[1], m[1]), reverse=True
        )
        entities = list(doc.ents)
        new_entities = []
        seen_tokens: set[int] = set()
        for match_id, start, end in sorted_matches:
            if any(t.ent_type for t in doc[start:end]) and not self.overwrite:
                continue
            # check for end - 1 here because boundaries are inclusive
            if start not in seen_tokens and end - 1 not in seen_tokens:
                if match_id in self._ent_ids:
                    label, ent_id = self._ent_ids[match_id]
                    span = Span(doc, start, end, label=label)
                    if ent_id:
                        for token in span:
                            token.ent_id_ = ent_id
                else:
                    span = Span(doc, start, end, label=match_id)
                span = self._update_custom_attrs(
                    span,
                    match_id,
                    start,
                    end,
                    ratio_lookup,
                    counts_lookup,
                    details_lookup,
                )
                new_entities.append(span)
                entities = [
                    e for e in entities if not (e.start < end and e.end > start)
                ]
                seen_tokens.update(range(start, end))
        doc.ents = entities + new_entities
        return doc

    def __contains__(self: SpaczzRuler, label: str) -> bool:
        """Whether a label is present in the patterns."""
        return (
            label in self.fuzzy_patterns
            or label in self.regex_patterns
            or label in self.token_patterns
        )

    def __len__(self: SpaczzRuler) -> int:
        """The number of all patterns added to the ruler."""
        n_fuzzy_patterns = sum(len(p["patterns"]) for p in self.fuzzy_patterns.values())
        n_regex_patterns = sum(len(p["patterns"]) for p in self.regex_patterns.values())
        n_token_patterns = sum(len(p) for p in self.token_patterns.values())
        return n_fuzzy_patterns + n_regex_patterns + n_token_patterns

    @property
    def ent_ids(self: SpaczzRuler) -> tuple[Optional[str], ...]:
        """All entity ids present in the match patterns id properties.

        Returns:
            The unique string entity ids as a tuple.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy", "id": "BEAT"}])
            >>> ruler.ent_ids
            ('BEAT',)
        """
        keys = set(self.fuzzy_patterns.keys())
        keys.update(self.regex_patterns.keys())
        keys.update(self.token_patterns.keys())
        all_ent_ids = set()

        for k in keys:
            if self.ent_id_sep in k:
                _, ent_id = self._split_label(k)
                all_ent_ids.add(ent_id)
        all_ent_ids_tuple = tuple(all_ent_ids)
        return all_ent_ids_tuple

    @property
    def labels(self: SpaczzRuler) -> tuple[str, ...]:
        """All labels present in the ruler.

        Returns:
            The unique string labels as a tuple.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> ruler.labels
            ('AUTHOR',)
        """
        keys = set(self.fuzzy_patterns.keys())
        keys.update(self.regex_patterns.keys())
        keys.update(self.token_patterns.keys())
        all_labels = set()
        for k in keys:
            if self.ent_id_sep in k:
                label, _ = self._split_label(k)
                all_labels.add(label)
            else:
                all_labels.add(k)
        return tuple(all_labels)

    @property
    def patterns(self: SpaczzRuler) -> list[dict[str, Any]]:
        """Get all patterns and kwargs that were added to the ruler.

        Returns:
            The original patterns and kwargs, one dictionary for each combination.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "STREET", "pattern": "street_addresses",
                "type": "regex", "kwargs": {"predef": True}}])
            >>> ruler.patterns == [
                {
                    "label": "STREET",
                    "pattern": "street_addresses",
                    "type": "regex",
                    "kwargs": {"predef": True},
                    },
                    ]
            True
        """
        all_patterns = []
        for label, fuzzy_patterns in self.fuzzy_patterns.items():
            for fuzzy_pattern, fuzzy_kwargs in zip(
                fuzzy_patterns["patterns"], fuzzy_patterns["kwargs"]
            ):
                ent_label, ent_id = self._split_label(label)
                p = {"label": ent_label, "pattern": fuzzy_pattern.text, "type": "fuzzy"}
                if fuzzy_kwargs:
                    p["kwargs"] = fuzzy_kwargs
                if ent_id:
                    p["id"] = ent_id
                all_patterns.append(p)
        for label, regex_patterns in self.regex_patterns.items():
            for regex_pattern, regex_kwargs in zip(
                regex_patterns["patterns"], regex_patterns["kwargs"]
            ):
                ent_label, ent_id = self._split_label(label)
                p = {"label": ent_label, "pattern": regex_pattern, "type": "regex"}
                if regex_kwargs:
                    p["kwargs"] = regex_kwargs
                if ent_id:
                    p["id"] = ent_id
                all_patterns.append(p)
        for label, token_patterns in self.token_patterns.items():
            for token_pattern in token_patterns:
                ent_label, ent_id = self._split_label(label)
                p = {"label": ent_label, "pattern": token_pattern, "type": "token"}
                if ent_id:
                    p["id"] = ent_id
                all_patterns.append(p)
        return all_patterns

    def add_patterns(self: SpaczzRuler, patterns: Iterable[dict[str, Any]],) -> None:
        """Add patterns to the ruler.

        A pattern must be a spaczz pattern:
        {label (str), pattern (str or list), type (str),
        optional kwargs (dict[str, Any]), and optional id (str)}.
        For example, a fuzzy phrase pattern:
        {'label': 'ORG', 'pattern': 'Apple', 'type': 'fuzzy', 'kwargs': {'min_r2': 90}}
        Or, a token pattern:
        {'label': 'ORG', 'pattern': [{'TEXT': {'FUZZY': 'Apple'}}], 'type': 'token'}

        To utilize regex flags, use inline flags.

        Kwarg details to be updated.

        Args:
            patterns: The spaczz patterns to add.

        Raises:
            TypeError: If patterns is not an iterable of dictionaries.
            ValueError: If one or more patterns do not conform
                the spaczz pattern structure.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> "AUTHOR" in ruler.labels
            True
        """
        # disable the nlp components after this one
        # in case they haven't been initialized / deserialised yet
        try:
            current_index = self.nlp.pipe_names.index(self.name)
            subsequent_pipes = [
                pipe for pipe in self.nlp.pipe_names[current_index + 1 :]
            ]
        except ValueError:
            subsequent_pipes = []

        with self.nlp.disable_pipes(subsequent_pipes):
            token_patterns = []
            fuzzy_pattern_labels = []
            fuzzy_pattern_texts = []
            fuzzy_pattern_kwargs = []
            fuzzy_pattern_ids = []
            regex_pattern_labels = []
            regex_pattern_texts = []
            regex_pattern_kwargs = []
            regex_pattern_ids = []

            for entry in patterns:
                try:
                    if isinstance(entry, dict):
                        if entry["type"] == "fuzzy":
                            fuzzy_pattern_labels.append(entry["label"])
                            fuzzy_pattern_texts.append(entry["pattern"])
                            fuzzy_pattern_kwargs.append(entry.get("kwargs", {}))
                            fuzzy_pattern_ids.append(entry.get("id"))
                        elif entry["type"] == "regex":
                            regex_pattern_labels.append(entry["label"])
                            regex_pattern_texts.append(entry["pattern"])
                            regex_pattern_kwargs.append(entry.get("kwargs", {}))
                            regex_pattern_ids.append(entry.get("id"))
                        elif entry["type"] == "token":
                            token_patterns.append(entry)
                        else:
                            warnings.warn(
                                f"""Spaczz pattern "type" must be "fuzzy", "regex",
                                or "token", not {entry["type"]}. Skipping this pattern.
                                """,
                                PatternTypeWarning,
                            )
                    else:
                        raise TypeError(
                            ("Patterns must either be an iterable of dicts.")
                        )
                except KeyError:
                    raise ValueError(
                        (
                            "One or more patterns do not conform",
                            "to spaczz pattern structure: ",
                            "{label (str), pattern (str or list), type (str),",
                            "optional kwargs (dict[str, Any]),",
                            "and optional id (str)}.",
                        )
                    )

            fuzzy_patterns = []
            for label, pattern, kwargs, ent_id in zip(
                fuzzy_pattern_labels,
                self.nlp.pipe(fuzzy_pattern_texts),
                fuzzy_pattern_kwargs,
                fuzzy_pattern_ids,
            ):
                fuzzy_pattern = {
                    "label": label,
                    "pattern": pattern,
                    "kwargs": kwargs,
                    "type": "fuzzy",
                }
                if ent_id:
                    fuzzy_pattern["id"] = ent_id
                fuzzy_patterns.append(fuzzy_pattern)

            regex_patterns = []
            for label, pattern, kwargs, ent_id in zip(
                regex_pattern_labels,
                regex_pattern_texts,
                regex_pattern_kwargs,
                regex_pattern_ids,
            ):
                regex_pattern = {
                    "label": label,
                    "pattern": pattern,
                    "kwargs": kwargs,
                    "type": "regex",
                }
                if ent_id:
                    regex_pattern["id"] = ent_id
                regex_patterns.append(regex_pattern)

            self._add_patterns(fuzzy_patterns, regex_patterns, token_patterns)

    def from_bytes(
        self: SpaczzRuler, patterns_bytes: bytes, **kwargs: Any
    ) -> SpaczzRuler:
        """Load the spaczz ruler from a bytestring.

        Args:
            patterns_bytes : The bytestring to load.
            **kwargs: Other config paramters, mostly for consistency.

        Returns:
            The loaded spaczz ruler.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> ruler_bytes = ruler.to_bytes()
            >>> new_ruler = SpaczzRuler(nlp)
            >>> new_ruler = new_ruler.from_bytes(ruler_bytes)
            >>> "AUTHOR" in new_ruler
            True
        """
        cfg = srsly.msgpack_loads(patterns_bytes)
        if isinstance(cfg, dict):
            self.add_patterns(cfg.get("spaczz_patterns", cfg))
            self.defaults = cfg.get("spaczz_defaults", {})
            self.overwrite = cfg.get("spaczz_overwrite", False)
            self.ent_id_sep = cfg.get("spaczz_ent_id_sep", DEFAULT_ENT_ID_SEP)
        else:
            self.add_patterns(cfg)
        return self

    def to_bytes(self: SpaczzRuler, **kwargs: Any) -> bytes:
        """Serialize the spaczz ruler patterns to a bytestring.

        Args:
            **kwargs: Other config paramters, mostly for consistency.

        Returns:
            The serialized patterns.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> ruler_bytes = ruler.to_bytes()
            >>> isinstance(ruler_bytes, bytes)
            True
        """
        serial = OrderedDict(
            (
                ("spaczz_overwrite", self.overwrite),
                ("spaczz_ent_id_sep", self.ent_id_sep),
                ("spaczz_patterns", self.patterns),
                ("spaczz_defaults", self.defaults),
            )
        )
        return srsly.msgpack_dumps(serial)

    def from_disk(
        self: SpaczzRuler, path: Union[str, Path], **kwargs: Any
    ) -> SpaczzRuler:
        """Load the spaczz ruler from a file.

        Expects a file containing newline-delimited JSON (JSONL)
        with one entry per line.

        Args:
            path: The JSONL file to load.
            **kwargs: Other config paramters, mostly for consistency.

        Returns:
            The loaded spaczz ruler.

        Example:
            >>> import os
            >>> import tempfile
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> with tempfile.TemporaryDirectory() as tmpdir:
            >>>     ruler.to_disk(f"{tmpdir}/ruler")
            >>>     new_ruler = SpaczzRuler(nlp)
            >>>     new_ruler = new_ruler.from_disk(f"{tmpdir}/ruler")
            >>> "AUTHOR" in new_ruler
            True
        """
        path = ensure_path(path)
        depr_patterns_path = path.with_suffix(".jsonl")
        if depr_patterns_path.is_file():
            patterns = srsly.read_jsonl(depr_patterns_path)
            self.add_patterns(patterns)
        else:
            cfg = {}
            deserializers_patterns = {
                "spaczz_patterns": lambda p: self.add_patterns(
                    srsly.read_jsonl(p.with_suffix(".jsonl"))
                )
            }
            deserializers_cfg = {"cfg": lambda p: cfg.update(srsly.read_json(p))}
            read_from_disk(path, deserializers_cfg, {})
            self.overwrite = cfg.get("spaczz_overwrite", False)
            self.defaults = cfg.get("spaczz_defaults", {})
            self.ent_id_sep = cfg.get("spaczz_ent_id_sep", DEFAULT_ENT_ID_SEP)
            read_from_disk(path, deserializers_patterns, {})
        return self

    def to_disk(self: SpaczzRuler, path: Union[str, Path], **kwargs: Any) -> None:
        """Save the spaczz ruler patterns to a directory.

        The patterns will be saved as newline-delimited JSON (JSONL).

        Args:
            path: The JSONL file to save.
            **kwargs: Other config paramters, mostly for consistency.

        Example:
            >>> import os
            >>> import tempfile
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> with tempfile.TemporaryDirectory() as tmpdir:
            >>>     ruler.to_disk(f"{tmpdir}/ruler")
            >>>     isdir = os.path.isdir(f"{tmpdir}/ruler")
            >>> isdir
            True
        """
        path = ensure_path(path)
        cfg = {
            "spaczz_overwrite": self.overwrite,
            "spaczz_defaults": self.defaults,
            "spaczz_ent_id_sep": self.ent_id_sep,
        }
        serializers = {
            "spaczz_patterns": lambda p: srsly.write_jsonl(
                p.with_suffix(".jsonl"), self.patterns
            ),
            "cfg": lambda p: srsly.write_json(p, cfg),
        }
        if path.suffix == ".jsonl":  # user wants to save only JSONL
            srsly.write_jsonl(path, self.patterns)
        else:
            write_to_disk(path, serializers, {})

    def _add_patterns(
        self: SpaczzRuler,
        fuzzy_patterns: list[dict[str, Any]],
        regex_patterns: list[dict[str, Any]],
        token_patterns: list[dict[str, Any]],
    ) -> None:
        """Helper function for add_patterns."""
        for entry in fuzzy_patterns + regex_patterns + token_patterns:
            label = entry["label"]
            if "id" in entry:
                ent_label = label
                label = self._create_label(label, entry["id"])
                self._ent_ids[label] = (ent_label, entry["id"])
            pattern = entry["pattern"]
            if isinstance(pattern, Doc):
                self.fuzzy_patterns[label]["patterns"].append(pattern)
                self.fuzzy_patterns[label]["kwargs"].append(entry["kwargs"])
            elif isinstance(pattern, str):
                self.regex_patterns[label]["patterns"].append(pattern)
                self.regex_patterns[label]["kwargs"].append(entry["kwargs"])
            elif isinstance(pattern, list):
                self.token_patterns[label].append(pattern)
            else:
                raise ValueError(
                    (
                        "One or more patterns do not conform",
                        "to spaczz pattern structure:",
                        "{label (str), pattern (str or list), type (str),",
                        "optional kwargs (dict[str, Any]),",
                        "and optional id (str)}.",
                    )
                )
        for label, patterns in self.fuzzy_patterns.items():
            self.fuzzy_matcher.add(label, patterns["patterns"], patterns["kwargs"])
        for label, patterns in self.regex_patterns.items():
            self.regex_matcher.add(label, patterns["patterns"], patterns["kwargs"])
        for label, _token_patterns in self.token_patterns.items():
            self.token_matcher.add(label, _token_patterns)

    def _create_label(self: SpaczzRuler, label: str, ent_id: Union[str, None]) -> str:
        """Join Entity label with ent_id if the pattern has an id attribute.

        Args:
            label: The entity label.
            ent_id: The optional entity id.

        Returns:
            The label and ent_id joined with configured ent_id_sep.
        """
        if isinstance(ent_id, str):
            label = "{}{}{}".format(label, self.ent_id_sep, ent_id)
        return label

    def _split_label(self: SpaczzRuler, label: str) -> tuple[str, Union[str, None]]:
        """Split Entity label into ent_label and ent_id if it contains self.ent_id_sep.

        Args:
            label: The value of label in a pattern entry

        Returns:
            The separated ent_label and optional ent_id.
        """
        if self.ent_id_sep in label:
            ent_label, ent_id = label.rsplit(self.ent_id_sep, 1)
            return ent_label, ent_id
        else:
            ent_label = label
            return ent_label, None

    @staticmethod
    def _update_custom_attrs(
        span: Span,
        match_id: str,
        start: int,
        end: int,
        ratio_lookup: dict[tuple[str, int, int], int],
        counts_lookup: dict[tuple[str, int, int], tuple[int, int, int]],
        details_lookup: dict[tuple[str, int, int], int],
    ) -> Span:
        """Update custom attributes for matches."""
        ratio = ratio_lookup.get((match_id, start, end), None)
        counts = counts_lookup.get((match_id, start, end), None)
        details = details_lookup.get((match_id, start, end), None)
        for token in span:
            token._.spaczz_token = True
            token._.spaczz_ratio = ratio
            token._.spaczz_counts = counts
            token._.spaczz_details = details
        return span
